"""The process of constantly monitoring a computer network"""

import time
import tkinter as tk
from tkinter import scrolledtext, ttk
from tkinter.ttk import *

import matplotlib.pyplot as plt
from pysnmp.entity import *
from pysnmp.entity.engine import SnmpEngine
from pysnmp.hlapi import *
from pysnmp.proto import rfc3411
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

# *


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
    root.update()

    try:

        oid = ObjectType(rfc1902.ObjectIdentity(oid))  #rfc1902.ObjectIdentity(oid)
        oid.resolveWithMib(mib_view)
    except:
        print("An exception occurred")
    return oid.prettyPrint()


# Зареждане на MIB файлове
mib_files = ['SNMPv2-MIB', 'Q-BRIDGE-MIB', 'IP-MIB', 'IF-MIB', 'TCP-MIB']  # Примерни MIB файлове
mib_view = load_mibs(mib_files)


def snmp_walk1(ip, oid, community):
    root.update()

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
        root.update()
        if start is not True: break
        if errorIndication:
            results.append(str(errorIndication))
            break
        elif errorStatus:
            results.append(f'{errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or "?"}')
            break
        else:
            for varBind in varBinds:
                root.update()
                if start is not True: break
                print(f'{varBind[0].prettyPrint()} = {varBind[1].prettyPrint()}')
                results.append(f'{varBind[0]} = {varBind[1].prettyPrint()}')
                #print(varBind[0])

    return results


def snmp_walk(ip, oid, community):
    root.update()

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
        root.update()
        if errorIndication:
            results.append(str(errorIndication))
            break
        elif errorStatus:
            results.append(f'{errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or "?"}')
            break
        else:
            for varBind in varBinds:
                root.update()
                if start is not True: break

                nom = str(varBind[0]).split(".")
                # print(nom[-1])
                #  print(varBind[1])
                results.append([nom, varBind[1]])
            # print(varBind[0])

    return results


def get_snmp_data(target, community, oid, port=161):
    root.update()
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
    root.update()
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
    root.update()
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
    root.update()
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
            root.update()
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


def run_scan():

    update_comboboxIP()
    root.update()
    global start
    start = True
    x = []
    x1 = []
    y = []
    y1 = []
    portsw = []
    In = []
    Out = []

    info_net_dev_oid = '1.3.6.1.2.1.1'  #'1.3.6.1.2.1.1'

    target = text_ip.get()  #'194.141.40.236'  # IP адрес на вашия суич
    community = text_community.get()  #'public'  # SNMP community string
    oid_ifInOctets = '1.3.6.1.2.1.2.2.1.10'  # OID за входящ трафик
    oid_ifOutOctets = '1.3.6.1.2.1.2.2.1.16'  # OID за изходящ трафик
    oid_portName = '1.3.6.1.2.1.2.2.1.2'
    oid_portStatus = '1.3.6.1.2.1.2.2.1.8'
    oid_vlan_id_onPort = '1.3.6.1.2.1.17.7.1.4.5.1.1'#1.3.6.1.2.1.17.7.1.4.5.1.1
    oid_port_outerr = '1.3.6.1.2.1.2.2.1.20'
    oid_port_inerr = '1.3.6.1.2.1.2.2.1.14'
    oid_ifAlias = '1.3.6.1.2.1.31.1.1.1.18'#
    oid_if_name= '1.3.6.1.2.1.31.1.1.1.1'
    try:
        portName = snmp_walk(target, oid_portName, community)
    # info_net_dev = snmp_walk1(target,info_net_dev_oid,community)
    except:
        print("Error snmp ....")
    rez = ''
    nom = 0

    rez = ''
    result_text.delete(1.0, tk.END)

    for port_nom, port in portName:  # Пример с 4 порта
        root.update()
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
        namePort=get_ifAlias(target, community, f'{oid_if_name}.{port_nom[-1]}')
        InMbit = bytes_to_megabits(in_octets1, in_octets2)
        OutMbit = bytes_to_megabits(out_octets1, out_octets2)
        result_text.delete(1.0, tk.END)

        if in_octets1 is not None and out_octets1 is not None and nom is not None and InMbit is not None and OutMbit is not None and in_err is not None and out_err is not None:

            portsw.append('(' + str(nom) + ')')
            In.append(InMbit)

            Out.append(OutMbit)

            y.append(in_err)

            y1.append(out_err)

            #
            # if in_err != 0.0:
            #     x.append('('+str(nom)+')')
            #     y.append(in_err)
            # if out_err != 0.0:
            #     x1.append('('+str(nom)+')')
            #     y1.append(out_err)
            if status == '2':

                print(
                    f"Port({nom}). {port}  ({ifAlias})  is DOWN : vlan ID ({vlan_id}): In={InMbit:.2f}  Mbps , Out={OutMbit:.2f} Mbps ,inError {in_err} ,outError {out_err}")
                rez += f"Port({nom}).  {port}  ({ifAlias})  is DOWN : vlan ID ({vlan_id}): In={InMbit:.2f}  Mbps , Out={OutMbit:.2f} Mbps ,inError {in_err},outError {out_err}" + '\n'
                result_text.insert(tk.END, rez)
                result_text.see("end")
                root.update()
            elif status == '1':

                print(
                    f"Port({nom}). {port}   ({ifAlias})  is UP : vlan ID ({vlan_id}): In={InMbit:.2f}  Mbps , Out={OutMbit:.2f} Mbps ,inError {in_err} ,outError {out_err}")
                rez += f"Port({nom}). {port}   ({ifAlias})  is UP : vlan ID ({vlan_id}): In={InMbit:.2f}  Mbps , Out={OutMbit:.2f} Mbps ,inError {in_err} ,outError {out_err}" + '\n'
                result_text.insert(tk.END, rez)
                result_text.see("end")
                root.update()
        else:
            print(f"Failed to get SNMP data for port {port}")
        #result_text.insert(tk.END, rez)
        #root.update()
    #result_text.insert(tk.END, rez + '\n')


    oid_SysName = '1.3.6.1.2.1.1.5'
    SysName = snmp_walk1(target, oid_SysName, community)
    Name = SysName

    print("SysName")
    #    print(errData)
    a = Name[0].split('=')
    print(a[1])
    f = lambda x: round(x, 3) if x != 0 else ' '

    plt.subplot(4, 1, 1)
    plt.bar(portsw, y, label='InError', color='blue')
    for i in range(len(y)):
        print(f(y[i]))
        plt.annotate(str(f(y[i])), xy=(portsw[i], y[i]), ha='center', va='bottom')
    # plt.subplot(4, 1, 1)
    plt.ylabel('Входящи  грешки')
    # plt.xlabel('Номер на порт')

    plt.title(f' {target} - ({a[1]})')
    plt.legend()
    plt.subplot(4, 1, 2)
    plt.bar(portsw, y1, label='OutError', color='skyblue')
    plt.ylabel('Изходящи грешки')

    for j in range(len(y1)):
        print(f(y1[j]))
        plt.annotate(str(f(y1[j])), xy=(portsw[j], y1[j]), ha='center', va='bottom')
    # plt.xlabel('Номер на порт')

    # plt.title(f'{target}')
    plt.legend()
    # plt.subplot(4, 1, 2)
    plt.subplot(4, 1, 3)
    plt.bar(portsw, In, label='InMbps', color='green')
    for k in range(len(In)):
        plt.annotate(str(f(In[k])), xy=(portsw[k], In[k]), ha='center', va='bottom')
    plt.ylabel('Входящ трафик (Mbps)')
    plt.legend()
    plt.subplot(4, 1, 4)
    # plt.subplot(4, 1, 3)
    plt.bar(portsw, Out, label='OutMbps', color='orange')

    for m in range(len(Out)):
        plt.annotate(str(f(Out[m])), xy=(portsw[m], Out[m]), ha='center', va='bottom')
    plt.xlabel('Номер на порт')
    plt.ylabel('Изходящ трафик (Mbps)')
    # plt.title(f'{target}')
    plt.legend()
    # defining the attributes

    plt.show()


def run_scanPortRange():
    # TODO: rez is the output
    update_comboboxIP()
    root.update()
    global start
    start = True
    fromP1 = int(fromP.get()) - 1
    ToP1 = int(ToP.get())
    x = []
    x1 = []
    y = []
    y1 = []
    portsw = []
    In = []
    Out = []

    info_net_dev_oid = '1.3.6.1.2.1.1'  #'1.3.6.1.2.1.1'

    target = text_ip.get()  #'194.141.40.236'  # IP адрес на вашия суич
    community = text_community.get()  #'public'  # SNMP community string
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
    # info_net_dev = snmp_walk1(target,info_net_dev_oid,community)
    except:
        print("Error snmp ....")
    rez = ''
    nom = fromP1

    rez = ''
    result_text.delete(1.0, tk.END)

    for port_nom, port in portName[fromP1:ToP1]:  # Пример с 4 порта
        root.update()
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
        result_text.delete(1.0, tk.END)

        if in_octets1 is not None and out_octets1 is not None and nom is not None and InMbit is not None and OutMbit is not None and in_err is not None and out_err is not None:

            portsw.append('(' + str(nom) + ')')
            In.append(InMbit)

            Out.append(OutMbit)

            y.append(in_err)

            y1.append(out_err)

            if status == '2':

                print(
                    f"Port({nom}). {port}  ({ifAlias})  is DOWN : vlan PVID ({vlan_id}): In={InMbit:.2f}  Mbps , Out={OutMbit:.2f} Mbps ,inError {in_err} ,outError {out_err}")
                rez += f"Port({nom}).  {port}  ({ifAlias})  is DOWN : vlan PVID ({vlan_id}): In={InMbit:.2f}  Mbps , Out={OutMbit:.2f} Mbps ,inError {in_err},outError {out_err}" + '\n'
                result_text.insert(tk.END, rez)
                result_text.see("end")
                root.update()
            elif status == '1':

                print(
                    f"Port({nom}). {port}  ({ifAlias})  is UP : vlan PVID ({vlan_id}): In={InMbit:.2f}  Mbps , Out={OutMbit:.2f} Mbps ,inError {in_err} ,outError {out_err}")
                rez += f"Port({nom}). {port}  ({ifAlias})  is UP : vlan PVID ({vlan_id}): In={InMbit:.2f}  Mbps , Out={OutMbit:.2f} Mbps ,inError {in_err} ,outError {out_err}" + '\n'
                result_text.insert(tk.END, rez)
                result_text.see("end")
                root.update()
        else:
            print(f"Failed to get SNMP data for port {port}")
        #result_text.insert(tk.END, rez)
        #root.update()
    #result_text.insert(tk.END, rez + '\n')
    return rez
    # oid_SysName = '1.3.6.1.2.1.1.5'
    # SysName = snmp_walk1(target, oid_SysName, community)
    # Name = SysName

    # print("SysName")
    # #    print(errData)
    # a = Name[0].split('=')
    # print(a[1])
    # f = lambda x: round(x, 3) if x != 0 else ' '

    # plt.subplot(4, 1, 1)
    # plt.bar(portsw, y, label='InError', color='blue')
    # for i in range(len(y)):
    #     print(f(y[i]))
    #     plt.annotate(str(f(y[i])), xy=(portsw[i], y[i]), ha='center', va='bottom')
    # #plt.subplot(4, 1, 1)
    # plt.ylabel('Входящи  грешки')
    # #plt.xlabel('Номер на порт')

    # plt.title(f' {target} - ({a[1]})')
    # plt.legend()
    # plt.subplot(4, 1, 2)
    # plt.bar(portsw, y1, label='OutError', color='skyblue')
    # plt.ylabel('Изходящи грешки')

    # for j in range(len(y1)):
    #     print(f(y1[j]))
    #     plt.annotate(str(f(y1[j])), xy=(portsw[j], y1[j]), ha='center', va='bottom')
    # #plt.xlabel('Номер на порт')

    # #plt.title(f'{target}')
    # plt.legend()
    # #plt.subplot(4, 1, 2)
    # plt.subplot(4, 1, 3)
    # plt.bar(portsw, In, label='InMbps', color='green')
    # for k in range(len(In)):
    #     plt.annotate(str(f(In[k])), xy=(portsw[k], In[k]), ha='center', va='bottom')
    # plt.ylabel('Входящ трафик (Mbps)')
    # plt.legend()
    # plt.subplot(4, 1, 4)
    # #plt.subplot(4, 1, 3)
    # plt.bar(portsw, Out, label='OutMbps', color='orange')

    # for m in range(len(Out)):
    #     plt.annotate(str(f(Out[m])), xy=(portsw[m], Out[m]), ha='center', va='bottom')
    # plt.xlabel('Номер на порт')
    # plt.ylabel('Изходящ трафик (Mbps)')
    # #plt.title(f'{target}')
    # plt.legend()
    # # defining the attributes

    # plt.show()


def stop():
    root.update()
    global start
    start = False
    #pass


# Setting up the Tkinter GUI
root = tk.Tk()
root.title("Софтуер за мрежови мониторинг ")
#logo=tk.PhotoImage(file = 'logo.png')
#root.iconphoto(False, logo)
root.resizable(True, True)
tk.Grid.rowconfigure(root, 3, weight=1)
tk.Grid.columnconfigure(root, 3, weight=1)
text_oid = tk.StringVar()
text_oid.set('1.3.6.1.2.1.1')
oid_entry = ttk.Combobox(root,textvariable=text_oid, width=24)#tk.Entry(root, textvariable=text_oid)
oid_entry.grid(row=0, column=3, padx=5, pady=5,sticky='nsew')
tk.Label(root, text="OID:").grid(row=0, column=2, pady=5, sticky='nsew')
# IP address input
text_ip = tk.StringVar()
fromP = tk.StringVar()
ToP = tk.StringVar()
disabledPort = tk.StringVar()
text_ip.set("194.141.37.238")
tk.Label(root, text="IP адрес :").grid(row=0, column=0, padx=10, pady=10,sticky='nsew')
ip_entry =ttk.Combobox(root,textvariable=text_ip, width=24) #tk.Entry(root, textvariable=text_ip)
ip_entry.grid(row=0, column=1, padx=5, pady=5,sticky='nsew')
text_community = tk.StringVar()
text_community.set("public")

# community input
tk.Label(root, text="community:").grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
community_entry = tk.Entry(root, textvariable=text_community)

community_entry.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
fromP_enttry = tk.Entry(root, textvariable=fromP).grid(row=2, column=2, padx=10, pady=10, sticky='nsew')
To_enttry = tk.Entry(root, textvariable=ToP).grid(row=2, column=3, padx=10, pady=10, sticky='nse')
# Submit button
submit_button = tk.Button(root, text="Сканиране на диапазон от портове", command=run_scanPortRange)  #run_scan
submit_button.grid(row=2, column=0, columnspan=2,padx=10, pady=10, sticky='nsew')
submit_button1 = tk.Button(root, text="Спиране на сканирането", command=stop)
submit_button1.grid(row=1, column=4, columnspan=1, padx=10, pady=10, sticky='nsew')
Info_button = tk.Button(root, text="Извеждане на информация за устройство", command=update_combobox)#show_info
Info_button.grid(row=0, column=4, columnspan=1, padx=10, pady=10, sticky='nsew')
submit_button3 = tk.Button(root, text="Сканиране на всички портове на у-во", command=run_scan)  #run_scan
submit_button3.grid(row=2, column=4, columnspan=2, padx=10, pady=10, sticky='nsew')
Port_enttry=tk.Entry(root,textvariable=disabledPort).grid(row=2, column=8,  padx=10, pady=10, sticky='nsew')
enable_button3 = tk.Button(root, text="Забраняване на порт", command=disablePort).grid(row=2, column=6,padx=10, pady=10, sticky='nsew')#
enable_button4 = tk.Button(root, text="Разрешаване на порт", command=enblePort).grid(row=2, column=7,padx=10, pady=10, sticky='nsew')
# Result display)
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=20)  #, width=100, height=20
result_text.grid(row=3, column=0, columnspan=5, sticky='nsew')#padx=10, pady=10,
result_text_info = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)  #, width=100, height=20
result_text_info.grid(row=3, column=5, columnspan=5,sticky='nsew')#, padx=10, pady=10

root.mainloop()
