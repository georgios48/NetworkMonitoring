# pylint: disable=global-statement, broad-exception-caught
# pylint: disable=import-error
"""The process of constantly monitoring a computer network"""

import logging
import time

import matplotlib.pyplot as plt
from models import DeviceInfoDTO, PortScanDTO
from pysnmp.hlapi import (CommunityData, ContextData, ObjectIdentity,
                          ObjectType, SnmpEngine, UdpTransportTarget, getCmd,
                          nextCmd, setCmd)
from pysnmp.proto.rfc1902 import Integer
from pysnmp.smi import builder, compiler, rfc1902, view
from pysnmp.smi.error import NoSuchObjectError

# *
# 1.3.6.1.2.1.2.2.1.2 port name

# 1-
# State of the port as defined by STP:
# Name : dot1dStpPortState
# OID : 1.3.6.1.2.1.17.2.15.1.3
# Value:
# 1 disabled
# 2 blocking
# 3 listening
# 4 learning
# 5 forwarding
# 6 broken

# 2-
# Name: dot1qVlanStaticUntaggedPorts
# Oid : 1.3.6.1.2.1.17.7.1.4.3.1.4
# *

# --------------------------------- Constants --------------------------------- #
OID_IN_OCTETS = '1.3.6.1.2.1.2.2.1.10'  # OID за входящ трафик
OID_OUT_OCTETS = '1.3.6.1.2.1.2.2.1.16'  # OID за изходящ трафик
OID_PORT_NAME = '1.3.6.1.2.1.2.2.1.2'
OID_PORT_STATUS = '1.3.6.1.2.1.2.2.1.8'
OID_VLAN_PORT = '1.3.6.1.2.1.17.7.1.4.5.1.1'
OID_PORT_OUTERR = '1.3.6.1.2.1.2.2.1.20'
OID_PORT_INERR = '1.3.6.1.2.1.2.2.1.14'
OID_IS_ALIAS = '1.3.6.1.2.1.31.1.1.1.18'

# --------------------------------- State management --------------------------------- #
START = True
LOADING = False
DEVICE_BUSY = False
PORT_SCAN_BUSYNESS = False

def start_loading(socketio):
    """start loading"""
    global LOADING
    LOADING = True
    socketio.emit("loading", {"loading": LOADING})

def stop_loading(socketio):
    """Stop loading"""
    global LOADING
    if LOADING:
        LOADING = False
    socketio.emit("loading", {"loading": LOADING})

def set_start():
    """Set start"""
    global START
    START = True

def send_clear_terminal(socketio, terminal):
    """Clear terminal"""

    # Terminal is either big/small
    socketio.emit("resetTerminal", {"terminal": terminal})

# --------------------------------- Endpoint Main functionalities --------------------------------- #

def stop(socketio):
    """Stop all process"""

    global START
    if START:
        START = False

        # Update UI loading status
        global LOADING
        if LOADING:
            LOADING = False
        socketio.emit("loading", {"loading": LOADING})

        # Clear busy status
        global DEVICE_BUSY
        if DEVICE_BUSY:
            DEVICE_BUSY = False
        global PORT_SCAN_BUSYNESS
        if PORT_SCAN_BUSYNESS:
            PORT_SCAN_BUSYNESS = False

    socketio.emit("process", {"process": "Process stopped"})


def get_device_info(oid, ip_target, community, socketio):
    """Scan device info"""
    global LOADING
    global DEVICE_BUSY
    if not DEVICE_BUSY:
        DEVICE_BUSY = True

        set_start()

        start_loading(socketio)

        send_clear_terminal(socketio, "small")

        try:
            info_net_dev = snmp_walk1(ip_target, oid, community)
            for result in info_net_dev:
                # Break scanning if stop button is pressed
                if START is False:
                    break

                device_info = result.split('=')
                device_model = device_info[1]
                system_oid = device_info[0]

                system_description = oid_to_description(socketio, system_oid)

                management_description = system_description.split('::')

                system_device_description = management_description[1].split('.')

                result = DeviceInfoDTO(
                    systemOID=system_oid,
                    systemDevice=system_device_description[0],
                    deviceModel=device_model,
                    )

                socketio.emit("displayDeviceInfo", result.to_dict())
                time.sleep(0.02)

                if LOADING:
                    LOADING = False
                socketio.emit("loading", {"loading": LOADING})
        except Exception as e:
            # Send info directly via webSocket
            socketio.emit("error", {"smallTerminalError": str(e)})
            LOADING = False
            socketio.emit("loading", {"loading": LOADING})
        finally:
            DEVICE_BUSY = False


def perform_port_range_scan(from_port, to_port, ip_target, community, socketio):
    """Perform port scan in a range or all ports, return detailed info"""
    global LOADING
    global PORT_SCAN_BUSYNESS
    if not PORT_SCAN_BUSYNESS:
        PORT_SCAN_BUSYNESS = True

        set_start()

        start_loading(socketio)

        send_clear_terminal(socketio, "big")

        # TODO: Used for matPlot
        in_errors = []
        out_errors = []
        portsw = []
        in_mbits = []
        out_mbits = []

        try:
            from_port = int(from_port) - 1
            to_port = int(to_port)

            port_name = snmp_walk(ip_target, OID_PORT_NAME, community)

            port_number = from_port

            for port_nom, port in port_name[from_port:to_port]:
                if not LOADING:
                    LOADING = True
                    socketio.emit("loading", {"loading": LOADING})

                if START is not True:
                    stop_loading(socketio)
                    break

                port_number += 1
                in_octets1 = get_snmp_data(ip_target, community, f'{OID_IN_OCTETS}.{port_nom[-1]}')
                time.sleep(1)
                in_octets2 = get_snmp_data(ip_target, community, f'{OID_IN_OCTETS}.{port_nom[-1]}')

                out_octets1 = get_snmp_data(ip_target, community, f'{OID_OUT_OCTETS}.{port_nom[-1]}')
                time.sleep(1)
                out_octets2 = get_snmp_data(ip_target, community, f'{OID_OUT_OCTETS}.{port_nom[-1]}')
                in_err = get_snmp_data(ip_target, community, f'{OID_PORT_INERR}.{port_nom[-1]}')
                out_err = get_snmp_data(ip_target, community, f'{OID_PORT_OUTERR}.{port_nom[-1]}')

                status = get_port_status(ip_target, community, f'{OID_PORT_STATUS}.{port_nom[-1]}')
                vlan_id = get_port_vlan(ip_target, community, f'{OID_VLAN_PORT}.{port_nom[-1]}')
                is_alias = get_alias(ip_target, community, f'{OID_IS_ALIAS}.{port_nom[-1]}')
                in_mbit = bytes_to_megabits(in_octets1, in_octets2)
                out_mbit = bytes_to_megabits(out_octets1, out_octets2)

                if all(v is not None for v in [in_octets1, out_octets1, port_number, in_mbit, out_mbit, in_err, out_err]):

                    portsw.append('(' + str(port_number) + ')')
                    in_mbits.append(in_mbit)

                    out_mbits.append(out_mbit)

                    in_errors.append(in_err)

                    out_errors.append(out_err)

                    send_port_scan_info(status, is_alias, port_number, port, vlan_id, in_mbit, out_mbit, in_err, out_err, socketio)
                else:
                    if START:
                        logging.error("Failed to get SNMP data for port %s", port)
                        # Send info directly via webSocket
                        socketio.emit("error", {"bigTerminalError": f"failed to get data for {port}"})

                    stop_loading(socketio)
        except ValueError:
            stop_loading(socketio)
            message = f"Invalid port range, numbers only: {from_port} - {to_port}"
            socketio.emit("error", {"bigTerminalError": message})
        except Exception as e:
            stop_loading(socketio)
            socketio.emit("error", {"bigTerminalError": str(e)})
        finally:
            PORT_SCAN_BUSYNESS = False

def disable_port(socketio, ip_target, community, port_to_disable):
    """Disable port switch by SNMP Setting"""

    set_start()

    start_loading(socketio)

    send_clear_terminal(socketio, "small")

    try:

        # OID for ifAdminStatus with given port ifIndex
        oid = f'1.3.6.1.2.1.2.2.1.7.{port_to_disable}'

        # Value for disabling the port switch (2 = down)
        value = Integer(2)

        # SNMP set operation
        error_indication, error_status, error_index, var_binds = next(
            setCmd(SnmpEngine(),
                CommunityData(community, mpModel=0),
                UdpTransportTarget((ip_target, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid), value))
        )

        if error_indication:
            socketio.emit("error", {"smallTerminalError": str(error_indication)})
        elif error_status:
            message = f"Error: {error_status.prettyPrint()} at {error_index and var_binds[int(error_index) - 1][0] or '?'}"
            socketio.emit("error", {"smallTerminalError": message})
        else:
            message = f"Port {port_to_disable} on {ip_target} has been disabled."
            socketio.emit("portAccess", message)

            display_port_status(socketio, ip_target, community)
    except NoSuchObjectError:
        stop_loading(socketio)
        message = f"Invalid port range, numbers only: {port_to_disable}"
        socketio.emit("error", {"smallTerminalError": message})
    except Exception as e:
        logging.error("An exception occurred", exc_info=True)
        socketio.emit("error", {"smallTerminalError": str(e)})
        stop_loading(socketio)


def enable_port(socketio, ip_target, community, port_to_enable):
    """Enable port switch by SNMP Setting"""

    set_start()

    start_loading(socketio)

    send_clear_terminal(socketio, "small")

    try:

        # OID for ifAdminStatus with given port ifIndex
        oid = f'1.3.6.1.2.1.2.2.1.7.{port_to_enable}'

        # Value for disabling the port switch (1 = Up)
        value = Integer(1)

        # SNMP set operation
        error_indication, error_status, error_index, var_binds = next(
            setCmd(SnmpEngine(),
                CommunityData(community, mpModel=0),
                UdpTransportTarget((ip_target, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid), value))
        )

        if error_indication:
            socketio.emit("error", {"smallTerminalError": str(error_indication)})
        elif error_status:
            message = f"Error: {error_status.prettyPrint()} at {error_index and var_binds[int(error_index) - 1][0] or '?'}"
            socketio.emit("error", {"smallTerminalError": message})
        else:
            message = f"Port {port_to_enable} on {ip_target} has been enabled."
            socketio.emit("portAccess", message)

            display_port_status(socketio, ip_target, community)
    except NoSuchObjectError:
        stop_loading(socketio)
        message = f"Invalid port range, numbers only: {port_to_enable}"
        socketio.emit("error", {"smallTerminalError": message})
    except Exception as e:
        logging.error("An exception occurred", exc_info=True)
        socketio.emit("error", {"smallTerminalError": str(e)})
        stop_loading(socketio)


# --------------------------------- Helper Functions --------------------------------- #
def get_admin_status(host, port, community):
    """Get the ifAdminStatus for all ports in the network switch"""

    result = []
    iterator = nextCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=0),
        UdpTransportTarget((host, port)),
        ContextData(),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.7')),
        lexicographicMode=False
    )

    for error_indicator, error_status, error_index, var_binds in iterator:
        if error_indicator:
            result.append(f"Error: {error_indicator}")
            break
        if error_status:
            result.append(
                f"Error: {error_status.prettyPrint()} at {error_index and var_binds[int(error_index) - 1][0] or '?'}")
            break

        for var_bind in var_binds:
            _, value = var_bind
            result.append(f" {value.prettyPrint()}")

    return result

def display_port_status(socketio, host, community):
    """Displays port status - enabled/disabled"""

    status_list = get_admin_status(host, 161, community)

    for i, status in enumerate(status_list):
        message = f"Port {str(i + 1)} is {status} - (1-enabled / 2-disabled)"
        socketio.emit("portAccess", message)


def load_mibs():
    """Load mibs"""
    mib_files = ['SNMPv2-MIB', 'Q-BRIDGE-MIB', 'IP-MIB', 'IF-MIB', 'TCP-MIB']
    mib_builder = builder.MibBuilder()
    compiler.addMibCompiler(mib_builder, sources=['http://mibs.snmplabs.com/asn1/@mib@',
                                                  'http://mibs.snmplabs.com/pysnmp/fulltexts/@mib@',
                                                  'http://mibs.snmplabs.com/pysnmp/notexts/@mib@'])
    mib_builder.loadModules(*mib_files)
    mib_view = view.MibViewController(mib_builder)

    return mib_view


def oid_to_description(socketio, oid):
    """Conveert OID into text"""
    try:
        mib_view = load_mibs()
        oid = ObjectType(rfc1902.ObjectIdentity(oid))  #rfc1902.ObjectIdentity(oid)
        oid.resolveWithMib(mib_view)
    except Exception as e:
        logging.error("An exception occurred", exc_info=True)
        socketio.emit("error", {"smallTerminalError": str(e)})

    return oid.prettyPrint()


def snmp_walk(ip, oid, community):
    """Iterate SNMP"""

    iterator = nextCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=0),  # Replace 'public' with your SNMP community string
        UdpTransportTarget((ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid)),
        lookupNames=True, lookupValues=True,
        lexicographicMode=False
    )

    results = []
    for error_indication, error_status, error_index, var_binds in iterator:
        if error_indication:
            results.append(str(error_indication))
            break
        if error_status:
            results.append(f'{error_status.prettyPrint()} at {error_index and var_binds[int(error_index) - 1][0] or "?"}')
            break

        for var_bind in var_binds:
            if START is not True:
                break

            nom = str(var_bind[0]).split(".")

            results.append([nom, var_bind[1]])

    return results


def iterate_snmp(community, target, port, oid, is_port):
    """Iterate SNMP"""

    iterator = getCmd(
        SnmpEngine(),
         CommunityData(community) if is_port else CommunityData(community, mpModel=0),
        UdpTransportTarget((target, port)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    error_indication, error_status, _, var_binds = next(iterator)

    if error_indication:
        logging.error("Error %s", error_indication)
        return None
    if error_status:
        logging.error("Error %s", error_status.prettyPrint())
        return None

    return var_binds

def get_snmp_data(target, community, oid, port=161):
    """Get SNMP data"""

    var_binds = iterate_snmp(community, target, port, oid, False)

    for var_bind in var_binds:
        if START is not True:
            break
        return int(var_bind[1])


def get_alias(target, community, oid, port=161):
    """Get ifAlias"""

    var_binds = iterate_snmp(community, target, port, oid, False)

    for var_bind in var_binds:
        if START is not True:
            break
        return var_bind[1]


def get_port_status(snmp_target, community, oid):
    """Get port status"""

    port = 161

    var_binds = iterate_snmp(community, snmp_target, port, oid, True)

    for var_bind in var_binds:
        if START is not True:
            break
        rez = var_bind.prettyPrint().split('=')[1].strip()

        return rez


def get_port_vlan(snmp_target, community, oid):
    """Get port VLAN"""

    port = 161

    var_binds = iterate_snmp(community, snmp_target, port, oid, True)

    for var_bind in var_binds:
        if START is not True:
            break
        return var_bind.prettyPrint().split('=')[1].strip()


def bytes_to_megabits(in_octets1, in_octets2):
    """Convert bytes to megabits"""

    rez = 0.0
    try:
        rez = ((in_octets2 - in_octets1) * 10) / 1048576 * 1
    except Exception as e:
        logging.error("Error %s", str(e))
    return rez

def snmp_walk1(ip, oid, community):
    """Iterates through a series of OIDs, retrieving all instances of the specified object type"""

    # Create SNMP iterator
    iterator = nextCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=0),
        UdpTransportTarget((ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid)),
        lookupNames=True, lookupValues=True,
        lexicographicMode=False
    )

    results = []
    for error_indicator, error_status, error_index, var_binds in iterator:
        if START is not True:
            break
        if error_indicator:
            results.append(str(error_indicator))
            break
        if error_status:
            results.append(f'{error_status.prettyPrint()} at {error_index and var_binds[int(error_index) - 1][0] or "?"}')
            break

        for var_bind in var_binds:
            if START is not True:
                break

            results.append(f'{var_bind[0]} = {var_bind[1].prettyPrint()}')

    return results

def send_port_scan_info(status, is_alias, port_number, port, vlan_id, in_mbit, out_mbit, in_err, out_err, socketio):
    """Check port status and send a message to WebSocket according to the status"""

    if status in ("1", "2"):
        alias_info = f"{is_alias.prettyPrint()} is UP" if status == "1" else f"{is_alias.prettyPrint()} is DOWN"

        new_info = PortScanDTO(
            number=port_number,
            port=port.prettyPrint(),
            ifAlias=alias_info,
            vlan=f"PVID ({vlan_id})",
            In=f"{in_mbit:.2f} Mbps",
            Out=f"{out_mbit:.2f} Mbps",
            inError=in_err,
            outError=out_err,
        )

        # Send info directly via webSocket
        socketio.emit("runScanPortRange", new_info.to_dict())

        stop_loading(socketio)