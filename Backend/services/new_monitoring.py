"""The process of constantly monitoring a computer network"""

import logging
import time
import tkinter as tk
from tkinter import scrolledtext, ttk
from tkinter.ttk import *

import matplotlib.pyplot as plt
from flask import abort
from pysnmp.entity import *
from pysnmp.entity.engine import SnmpEngine
from pysnmp.hlapi import *
from pysnmp.smi import *
from pysnmp.smi import builder, compiler, rfc1902, view

# *
# 1.3.6.1.2.1.2.2.1.2 port name

# 1-
# State of the port as defined by STP :
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

start = True

# *

def get_device_info(oid, ip_target, community, socketio):
    """Scan device info"""

    try:
        info_net_dev = snmp_walk1(ip_target, oid, community)
    except Exception as e:
        # Send info directly via webSocket
        socketio.emit("error", {"error": str(e)})

    try:
        for result in info_net_dev:
            # Break scanning if stop button is pressed
            if start is False:
                break

            device_info = result.split('=')
            device_model = device_info[1]
            system_oid = device_info[0]

            system_description = oid_to_description(system_oid, mib_view)

            management_description = system_description.split('::')

            system_device_description = management_description[1].split('.')

            # TODO: use DTO
            result = {"systemOID": system_oid, "systemDevice": system_device_description, "deviceModel": device_model}
            print(result)

            socketio.emit("displayDeviceInfo", result)
            time.sleep(0.02)
    except Exception as e:
        # Send info directly via webSocket
        socketio.emit("error", {"error": str(e)})


def snmp_walk1(ip, oid, community):
    """Iterates through a series of OIDs, retrieving all instances of the specified object type"""

    iterator = nextCmd(
        SnmpEngine(),
        # Replace 'public' with your SNMP community string
        CommunityData(community, mpModel=0),
        UdpTransportTarget((ip, 161)),

        ContextData(),

        ObjectType(ObjectIdentity(oid)),
        lookupNames=True, lookupValues=True,
        lexicographicMode=False
    )

    results = []
    for error_indicator, error_status, error_index, var_binds in iterator:
        if start is not True:
            break
        if error_indicator:
            results.append(str(error_indicator))
            break
        if error_status:
            results.append(f'{error_status.prettyPrint()} at {error_index and var_binds[int(error_index) - 1][0] or "?"}')
            break

        for var_bind in var_binds:
            if start is not True:
                break

            print(f'{var_bind[0].prettyPrint()} = {var_bind[1].prettyPrint()}')
            results.append(f'{var_bind[0]} = {var_bind[1].prettyPrint()}')

    return results

def run_scanPortRange(from_port, to_port, socketio):
    global start
    start = True
    from_port = (int(from_port) - 1)
    to_port = int(to_port)
    x = []
    x1 = []
    y = []
    y1 = []
    portsw = []
    In = []
    Out = []

    target = "194.141.37.238"  #'194.141.40.236'  # IP адрес на вашия суич
    community = "public"  #'public'  # SNMP community string
    oid_ifInOctets = '1.3.6.1.2.1.2.2.1.10'  # OID за входящ трафик
    oid_ifOutOctets = '1.3.6.1.2.1.2.2.1.16'  # OID за изходящ трафик
    oid_portName = '1.3.6.1.2.1.2.2.1.2'
    oid_portStatus = '1.3.6.1.2.1.2.2.1.8'
    oid_vlan_id_onPort = '1.3.6.1.2.1.17.7.1.4.5.1.1'
    oid_port_outerr = '1.3.6.1.2.1.2.2.1.20'
    oid_port_inerr = '1.3.6.1.2.1.2.2.1.14'
    oid_ifAlias = '1.3.6.1.2.1.31.1.1.1.18'
    try:
        portName = snmp_walk(target, oid_portName, community)
    except:
        print("Error snmp ....")
    rez = ''
    nom = from_port

    rez = {"scanResult": []}

    for port_nom, port in portName[from_port:to_port]:
        # root.update()
        if start is not True: break
        nom += 1
        in_octets1 = get_snmp_data(target, community, f'{oid_ifInOctets}.{port_nom[-1]}')
        time.sleep(1)
        in_octets2 = get_snmp_data(target, community, f'{oid_ifInOctets}.{port_nom[-1]}')

        out_octets1 = get_snmp_data(target, community, f'{oid_ifOutOctets}.{port_nom[-1]}')
        time.sleep(1)
        out_octets2 = get_snmp_data(target, community, f'{oid_ifOutOctets}.{port_nom[-1]}')
        in_err = get_snmp_data(target, community, f'{oid_port_inerr}.{port_nom[-1]}')
        out_err = get_snmp_data(target, community, f'{oid_port_outerr}.{port_nom[-1]}')
        # print(in_octets)
        status = get_port_status(target, community, f'{oid_portStatus}.{port_nom[-1]}')
        vlan_id = get_port_vlan(target, community, f'{oid_vlan_id_onPort}.{port_nom[-1]}')
        ifAlias = get_ifAlias(target, community, f'{oid_ifAlias}.{port_nom[-1]}')
        InMbit = bytes_to_megabits(in_octets1, in_octets2)
        OutMbit = bytes_to_megabits(out_octets1, out_octets2)

        if in_octets1 is not None and out_octets1 is not None and nom is not None and InMbit is not None and OutMbit is not None and in_err is not None and out_err is not None:

            portsw.append('(' + str(nom) + ')')
            In.append(InMbit)

            Out.append(OutMbit)

            y.append(in_err)

            y1.append(out_err)

            # TODO: map the output to a DTO for readability
            if status == '2':
                new_info = {
                        "number": nom,
                        "port": port.prettyPrint(),
                        "ifAlias": f"{ifAlias.prettyPrint()} is DOWN",
                        "vlan": f"PVID ({vlan_id})",
                        "In": f"{InMbit:.2f} Mbps",
                        "Out": f"{OutMbit:.2f} Mbps",
                        "inError": in_err,
                        "outError": out_err
                    }
                # Send info directly via webSocket
                socketio.emit("runScanPortRange", new_info)
            elif status == '1':
                new_info = {
                        "number": nom,
                        "port": port.prettyPrint(),
                        "ifAlias": f"{ifAlias.prettyPrint()} is UP",
                        "vlan": f"PVID ({vlan_id})",
                        "In": f"{InMbit:.2f} Mbps",
                        "Out": f"{OutMbit:.2f} Mbps",
                        "inError": in_err,
                        "outError": out_err
                    }
                rez["scanResult"].append(new_info)
                # Send info directly via webSocket
                socketio.emit("runScanPortRange", new_info)
        else:
            print(f"Failed to get SNMP data for port {port}")
            # Send info directly via webSocket
            socketio.emit("error", {"error": f"failed to get data for {port}"})

def update_combobox():
    new_value = oid_entry.get()
    values = list(oid_entry.cget("values")) or []
    if new_value not in values:
        values.append(new_value)
        oid_entry.configure(values=values)
    show_info()
def update_comboboxIP():
    new_value = ip_entry.get()
    values = list(ip_entry.cget("values")) or []
    if new_value not in values:
        values.append(new_value)
        ip_entry.configure(values=values)


def get_ifAdminStatus(host, port, community):
    """
    Връща ifAdminStatus за всички портове на мрежовия суич.

    :param host: IP адрес или хост на SNMP агента (суича)
    :param port: SNMP порт (обикновено 161)
    :param community: SNMP общност (community string)
    :return: Списък с ifAdminStatus за всеки интерфейс
    """
    result = []
    iterator = nextCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=0),
        UdpTransportTarget((host, port)),
        ContextData(),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.7')),
        lexicographicMode=False
    )

    for errorIndication, errorStatus, errorIndex, varBinds in iterator:
        if errorIndication:
            result.append(f"Error: {errorIndication}")
            break
        elif errorStatus:
            result.append(
                f"Error: {errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or '?'}")
            break
        else:
            for varBind in varBinds:
                oid, value = varBind
                result.append(f" {value.prettyPrint()}")

    return result


def display_ifAdminStatus():
    host = text_ip.get()
    port = 161
    community = text_community.get()
    i=0
    #statusP=''
    status_list = get_ifAdminStatus(host, port, community)

    result_text_info .delete(1.0, tk.END)
    for status in status_list:
        i+=1
        rez = status

        result_text_info.insert(tk.END, 'Port ' + str(i) + ' is  ' + status + '(1-разрешен / 2-забранен)'+'\n')
        root.update()


def disablePort():
    ip = text_ip.get()
    community = text_community.get()
    port = 161
    if_index=disabledPort.get()
    print(ip,community,port,if_index)
    """
        Забранява порт на суич чрез SNMP SET операция.

        :param host: IP адрес или хост на SNMP агента (суича)
        :param port: SNMP порт (обикновено 161)
        :param community: SNMP общност (community string)
        :param if_index: Индекс на интерфейса (порта), който трябва да бъде забранен
        :return: Резултат от SNMP SET операцията
        """
    # OID за ifAdminStatus с посочения ifIndex
    oid = f'1.3.6.1.2.1.2.2.1.7.{if_index}'

    # Стойност за забраняване на порта (2 = down)
    value = Integer(2)

    # Изпълняване на SNMP SET операция
    error_indication, error_status, error_index, var_binds = next(
        setCmd(SnmpEngine(),
               CommunityData(community, mpModel=0),
               UdpTransportTarget((ip, port)),
               ContextData(),
               ObjectType(ObjectIdentity(oid), value))
    )

    # Обработка на SNMP отговор
    if error_indication:
        print(f"Error: {error_indication}")
    elif error_status:
        print(f"Error: {error_status.prettyPrint()} at {error_index and var_binds[int(error_index) - 1][0] or '?'}")
    else:
        print(f"Port {if_index} on {ip} has been disabled.")
        display_ifAdminStatus()
        return var_binds


def enblePort():
    ip = text_ip.get()
    community = text_community.get()
    port = 161
    if_index = disabledPort.get()
    print(ip, community, port, if_index)
    """
        Забранява порт на суич чрез SNMP SET операция.

        :param host: IP адрес или хост на SNMP агента (суича)
        :param port: SNMP порт (обикновено 161)
        :param community: SNMP общност (community string)
        :param if_index: Индекс на интерфейса (порта), който трябва да бъде забранен
        :return: Резултат от SNMP SET операцията
        """
    # OID за ifAdminStatus с посочения ifIndex
    oid = f'1.3.6.1.2.1.2.2.1.7.{if_index}'

    # Стойност за забраняване на порта (2 = down)
    value = Integer(1)

    # Изпълняване на SNMP SET операция
    error_indication, error_status, error_index, var_binds = next(
        setCmd(SnmpEngine(),
               CommunityData(community, mpModel=0),
               UdpTransportTarget((ip, port)),
               ContextData(),
               ObjectType(ObjectIdentity(oid), value))
    )

    # Обработка на SNMP отговор
    if error_indication:
        print(f"Error: {error_indication}")
    elif error_status:
        print(f"Error: {error_status.prettyPrint()} at {error_index and var_binds[int(error_index) - 1][0] or '?'}")
    else:
        print(f"Port {if_index} on {ip} has been enabled.")
        display_ifAdminStatus()
        return var_binds


def load_mibs(mib_files):
    mib_builder = builder.MibBuilder()
    compiler.addMibCompiler(mib_builder, sources=['http://mibs.snmplabs.com/asn1/@mib@',
                                                  'http://mibs.snmplabs.com/pysnmp/fulltexts/@mib@',
                                                  'http://mibs.snmplabs.com/pysnmp/notexts/@mib@'])
    mib_builder.loadModules(*mib_files)
    mib_view = view.MibViewController(mib_builder)

    return mib_view


# Функция за конвертиране на OID в текстово описание
def oid_to_description(oid, mib_view):
    try:

        oid = ObjectType(rfc1902.ObjectIdentity(oid))  #rfc1902.ObjectIdentity(oid)
        oid.resolveWithMib(mib_view)
    except Exception:
        logging.error("An exception occurred", exc_info=True)
        abort(400, "An exception occurred")

    return oid.prettyPrint()


# Зареждане на MIB файлове
mib_files = ['SNMPv2-MIB', 'Q-BRIDGE-MIB', 'IP-MIB', 'IF-MIB', 'TCP-MIB']  # Примерни MIB файлове
mib_view = load_mibs(mib_files)


def snmp_walk(ip, oid, community):

    iterator = nextCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=0),  # Replace 'public' with your SNMP community string
        UdpTransportTarget((ip, 161)),

        ContextData(),

        #
        ObjectType(ObjectIdentity(oid)),
        lookupNames=True, lookupValues=True,
        lexicographicMode=False
    )

    results = []
    for errorIndication, errorStatus, errorIndex, varBinds in iterator:
        if errorIndication:
            results.append(str(errorIndication))
            break
        elif errorStatus:
            results.append(f'{errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or "?"}')
            break
        else:
            for varBind in varBinds:
                if start is not True: break

                nom = str(varBind[0]).split(".")
                # print(nom[-1])
                #  print(varBind[1])
                results.append([nom, varBind[1]])
            # print(varBind[0])

    return results


def get_snmp_data(target, community, oid, port=161):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=0),
        UdpTransportTarget((target, port)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(f"Error: {errorIndication}")
        return None
    elif errorStatus:
        print(f"Error: {errorStatus.prettyPrint()}")
        return None
    else:
        for varBind in varBinds:
            if start is not True: break
            return int(varBind[1])


def get_ifAlias(target, community, oid, port=161):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=0),
        UdpTransportTarget((target, port)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(f"Error: {errorIndication}")
        return None
    elif errorStatus:
        print(f"Error: {errorStatus.prettyPrint()}")
        return None
    else:
        for varBind in varBinds:
            if start is not True: break
            return varBind[1]


def get_port_status(snmp_target, community, oid):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((snmp_target, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(f"Error: {errorIndication}")
        return None
    elif errorStatus:
        print(f"Error: {errorStatus.prettyPrint()}")
        return None
    else:
        for varBind in varBinds:
            if start is not True: break
            rez = varBind.prettyPrint().split('=')[1].strip()
            #print(rez)
            return rez


def get_port_vlan(snmp_target, community, oid):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((snmp_target, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(f"Error: {errorIndication}")
        return None
    elif errorStatus:
        print(f"Error: {errorStatus.prettyPrint()}")
        return None
    else:
        for varBind in varBinds:
            if start is not True: break
            return varBind.prettyPrint().split('=')[1].strip()


def bytes_to_megabits(in_octets1, in_octets2):
    rez = 0.0
    try:
        rez = ((in_octets2 - in_octets1) * 10) / 1048576 * 1
    except:
        print('error ....')
    return rez


def show_info():
    result_text_info.delete(1.0, tk.END)
    root.update()
    global start
    start = True
    info_net_dev_oid = text_oid.get()  #'1.3.6.1.2.1.1'  # '1.3.6.1.2.1.1'
    target = text_ip.get()  # '194.141.40.236'  # IP адрес на вашия суич
    community = text_community.get()  # 'public'  # SNMP community string
    try:
        print(" snmp ....")
        info_net_dev = snmp_walk1(target, info_net_dev_oid, community)
        print(info_net_dev)
    except:
        print("Error snmp ....")
    rez = ''
    result_text_info.delete(1.0, tk.END)
    #info_net_dev = snmp_walk1(target, info_net_dev_oid, community)
    for result in info_net_dev:
        # root.update()
        if start is not True: break

        # print(a)
        # mib_files = ['SNMPv2-MIB', 'IF-MIB']  # Примерни MIB файлове
        # mib_view = load_mibs(mib_files)
        try:
            a = result.split('=')
            description = oid_to_description(a[0], mib_view)
            # value_snmp=oid_to_description(a[1],mib_view)
            b = description.split('::')
            b1 = b[1].split('.')
            # print(a[0] + description + a[1])
            result_text_info.insert(tk.END, a[0] + '|' + b1[0] + a[1] + '\n')
            result_text_info.see("end")
            root.update()
            rez += b1[0] + a[1] + '\n'
            time.sleep(0.02)
        # print(rez)

        except:
            print("Error in description ...")

        # print(a[0]+description+a[1])
        # rez+=b1[0]+a[1]+ '\n'
    # result_text_info.delete(1.0, tk.END)
    # result_text_info.insert(tk.END, rez + '\n')
    root.update()


def stop():
    root.update()
    global start
    start = False
    #pass
