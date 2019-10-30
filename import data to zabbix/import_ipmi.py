#!/usr/bin/env python

#This script reads information from a csv file and fills in the inventory fields in zabbix hosts
#There is one command line argument: path to csv file

import sys,csv
from pyzabbix import ZabbixAPI

#Fields from csv file
csv_hostname = ""
csv_ipmi = ""

#List of founded zabbix hosts
zabbix_hostnames = []

#macri nane to update
macroname='{$IPMIIP}'

#Get list of zabbix hosts
def Get_Zabbix_Hostnames():
    global zabbix
    zabbix = ZabbixAPI('http://localhost/zabbix', user='', password='')
    zabbix.session.verify = False
    hosts=zabbix.host.get(output=['hostid','name'])
    for host in hosts:
        zabbix_hostnames.append(str.lower((host['name']).encode('ascii','ignore')))
		
#Get the id of hosts depending on their name
def Get_Host_ID(name):
    hosts=zabbix.host.get(output=['name','hostid'],filter={"name": name})
    id_host = (hosts[0]['hostid'])
    return id_host
	
#Insert values from csv into Zabbix Inventory fields
def Update_ipmi():
    Get_Zabbix_Hostnames()
    with open(sys.argv[1], 'r') as myfile:
     inp_file = csv.reader(myfile, delimiter=',')
     for line in inp_file:
        csv_hostname = line[0]
        csv_ipmi = line[1]
        if(str.lower(csv_hostname) in zabbix_hostnames):
			macros=zabbix.usermacro.get(hostids=Get_Host_ID(csv_hostname), output=['value'], filter={'macro':macroname})
            zabbix.usermacro.update(hostmacroid=macros[0]['hostmacroid'],value=csv_ipmi)

Update_ipmi()