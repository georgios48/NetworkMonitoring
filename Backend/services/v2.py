# """The process of constantly monitoring a computer network"""
# # pylint: disable=global-statement

# import logging
# from time import sleep

# import error
# import matplotlib.pyplot as plt

# # *
# # 1.3.6.1.2.1.2.2.1.2 port name

# # 1-
# # State of the port as defined by STP :
# # Name : dot1dStpPortState
# # OID : 1.3.6.1.2.1.17.2.15.1.3
# # Value:
# # 1 disabled
# # 2 blocking
# # 3 listening
# # 4 learning
# # 5 forwarding
# # 6 broken

# # 2-
# # Name: dot1qVlanStaticUntaggedPorts
# # Oid : 1.3.6.1.2.1.17.7.1.4.3.1.4

# # *

# # Global scan variable, used to start/stop the scanning
# SCAN = True

# # TODO: placeholder
# def snmp_walk():
#     """Walk through SNMP"""

#     iterator = nextCmd(
#         SnmpEngine(),
#         CommunityData(community, mpModel=0),  # Replace 'public' with your SNMP community string
#         UdpTransportTarget((ip, 161)),

#         ContextData(),

#         #
#         ObjectType(ObjectIdentity(oid)),
#         lookupNames=True, lookupValues=True,
#         lexicographicMode=False
#     )

#     results = []
#     for errorIndication, errorStatus, errorIndex, varBinds in iterator:
#         root.update()
#         if errorIndication:
#             results.append(str(errorIndication))
#             break
#         elif errorStatus:
#             results.append(f'{errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or "?"}')
#             break
#         else:
#             for varBind in varBinds:
#                 root.update()
#                 if start is not True: break

#                 nom = str(varBind[0]).split(".")
#                 # print(nom[-1])
#                 #  print(varBind[1])
#                 results.append([nom, varBind[1]])
#             # print(varBind[0])

#     return results


# def get_snmp_data():
#     pass

# def round_or_empty(x):
#     """Rounds a number or returns empty string"""
#     return round(x, 3) if x != 0 else ' '

# def display_matplot(portsw, in_errors, target, out_errors, in_mbits, out_mbits, f, a):
#     """Displays windows with python matplot"""
#     plt.subplot(4, 1, 1)
#     plt.bar(portsw, in_errors, label='InError', color='blue')

#     for _, i in enumerate(in_errors):
#         plt.annotate(str(f(in_errors[i])), xy=(portsw[i], in_errors[i]), ha='center', va='bottom')

#     plt.ylabel('Входящи  грешки')
#     plt.title(f' {target} - ({a[1]})')
#     plt.legend()
#     plt.subplot(4, 1, 2)
#     plt.bar(portsw, out_errors, label='OutError', color='skyblue')
#     plt.ylabel('Изходящи грешки')

#     for _, j in enumerate(out_errors):
#         plt.annotate(str(f(out_errors[j])), xy=(portsw[j], out_errors[j]), ha='center', va='bottom')

#     plt.legend()
#     plt.subplot(4, 1, 3)
#     plt.bar(portsw, in_mbits, label='InMbps', color='green')

#     for _, k in enumerate(in_mbits):
#         plt.annotate(str(f(in_mbits[k])), xy=(portsw[k], in_mbits[k]), ha='center', va='bottom')

#     plt.ylabel('Входящ трафик (Mbps)')
#     plt.legend()
#     plt.subplot(4, 1, 4)
#     plt.bar(portsw, out_mbits, label='OutMbps', color='orange')

#     for _, m in enumerate(out_mbits):
#         plt.annotate(str(f(out_mbits[m])), xy=(portsw[m], out_mbits[m]), ha='center', va='bottom')

#     plt.xlabel('Номер на порт')
#     plt.ylabel('Изходящ трафик (Mbps)')
#     plt.legend()

#     plt.show()

# def scan_all_ports(target, community):
#     """Scan all the ports of the device"""

#     global SCAN
#     SCAN = True

#     # OID за входящ трафик
#     oid_in_octets = '1.3.6.1.2.1.2.2.1.10'
#     # OID за изходящ трафик
#     oid_out_octets = '1.3.6.1.2.1.2.2.1.16'
#     oid_port_name = '1.3.6.1.2.1.2.2.1.2'
#     oid_port_status = '1.3.6.1.2.1.2.2.1.8'
#     oid_vlan_id_on_port = '1.3.6.1.2.1.17.7.1.4.5.1.1'
#     oid_port_outerr = '1.3.6.1.2.1.2.2.1.20'
#     oid_port_inerr = '1.3.6.1.2.1.2.2.1.14'
#     oid_alias = '1.3.6.1.2.1.31.1.1.1.18'

#     in_errors = []
#     out_errors = []
#     portsw = []
#     in_mbits = []
#     out_mbits = []
#     x = []

#     try:
#         port_name = snmp_walk(target, oid_port_name, community)
#     except Exception as e:
#         logging.error("Error SNMP.. %s ", e)
#         raise error.GeneralCustomException(f"Error SNMP.. {e}") from e

#     result = ""
#     nom = 0

#     for port_nom, port in port_name:
#         if SCAN is not True:
#             break

#         nom += 1

#         in_octets1 = get_snmp_data(target, community, f'{oid_in_octets}.{port_nom[-1]}')
#         sleep(1)

#         in_octets2 = get_snmp_data(target, community, f'{oid_in_octets}.{port_nom[-1]}')
#         out_octets1 = get_snmp_data(target, community, f'{oid_out_octets}.{port_nom[-1]}')
#         sleep(1)

#         out_octets2 = get_snmp_data(target, community, f'{oid_out_octets}.{port_nom[-1]}')
#         in_err = get_snmp_data(target, community, f'{oid_port_inerr}.{port_nom[-1]}')
#         out_err = get_snmp_data(target, community, f'{oid_port_outerr}.{port_nom[-1]}')

#         status = get_port_status(target, community, f'{oid_port_status}.{port_nom[-1]}')
#         vlan_id = get_port_vlan(target, community, f'{oid_vlan_id_on_port}.{port_nom[-1]}')
#         if_alias = get_ifAlias(target, community, f'{oid_alias}.{port_nom[-1]}')
#         in_mbit = bytes_to_megabits(in_octets1, in_octets2)
#         out_mbit = bytes_to_megabits(out_octets1, out_octets2)


#         if any(var is None for var in (in_octets1, out_octets1, nom, in_mbit, out_mbit, in_err, out_err)):
#             logging.error("Failed to get SNMP Data for port - %s", port)
#             raise error.FailedToGetData(port)

#         portsw.append('(' + str(nom) + ')')
#         in_mbits.append(in_mbit)

#         out_mbits.append(out_mbit)

#         in_errors.append(in_err)

#         out_errors.append(out_err)

#         if status == '2':
#             print(
#                 f"Port({nom}). {port}  ({if_alias})  is DOWN : vlan ID ({vlan_id}): In={in_mbit:.2f}  Mbps , Out={out_mbit:.2f} Mbps ,inError {in_err} ,outError {out_err}")
#             result += f"Port({nom}).  {port}  ({if_alias}) is DOWN : vlan ID ({vlan_id}): In={in_mbit:.2f}  Mbps , Out={out_mbit:.2f} Mbps ,inError {in_err},outError {out_err}" + '\n'

#         elif status == '1':
#             print(
#                 f"Port({nom}). {port}   ({if_alias})  is UP : vlan ID ({vlan_id}): In={in_mbit:.2f}  Mbps , Out={out_mbit:.2f} Mbps ,inError {in_err} ,outError {out_err}")
#             result += f"Port({nom}).{port} ({if_alias})  is UP : vlan ID ({vlan_id}): In={in_mbit:.2f}  Mbps , Out={out_mbit:.2f} Mbps ,inError {in_err} ,outError {out_err}" + '\n'

#     oid_sys_name = '1.3.6.1.2.1.1.5'
#     sys_name = snmp_walk1(target, oid_sys_name, community)
#     name = sys_name

#     a = name[0].split('=')

#     f = round_or_empty(x)

#     display_matplot(portsw, in_errors, target, out_errors, in_mbits, out_mbits, f, a)
