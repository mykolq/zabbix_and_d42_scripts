#!/usr/bin/env python

#This script reads information from a csv file and fills in the inventory fields in zabbix hosts
#There is one command line argumen - path to csv file
#For example, run <<<d421.py "/home/vasia/log.csv">>>

import sys,csv
from pyzabbix import ZabbixAPI

#Fields from csv file
csv_hostname = ""
csv_rack = ""
csv_dc = ""

#List of founded zabbix hosts
zabbix_hostnames = []

#Get list of zabbix hosts
def Get_Zabbix_Hostnames():
    global zabbix
    zabbix = ZabbixAPI('http://localhost/zabbix', user='', password='')
    zabbix.session.verify = False
    hosts=zabbix.host.get(output=['hostid','name'])
    for host in hosts:
        zabbix_hostnames.append(str.lower((host['name']).encode('ascii','ignore')))


#Converts the names of domain controllers from a csv file to the names of the data centers in which they are located
def Get_DCName(DC):
    DC = str.lower(DC)
    if(DC == str.lower("Quebec")):
        return "DTL"
    elif(DC == str.lower("Modul-5")):
        return "SD2"
    elif(DC == str.lower("Modul-1-1")):
        return  "BST"
    elif(DC == str.lower("XLT_01-37")):
        return  "XLT"
    else:
        return "Unknown"


#Get the id of hosts depending on their name
def Get_Host_ID(name):
    hosts=zabbix.host.get(output=['name','hostid'],filter={"name": name})
    id_host = (hosts[0]['hostid'])
    return id_host


#Insert values from csv into Zabbix Inventory fields
def Update_Inv_Data():
    Get_Zabbix_Hostnames()
    with open(sys.argv[1], 'r') as myfile:
     inp_file = csv.reader(myfile, delimiter=',')
     for line in inp_file:
        csv_hostname = line[0]
        csv_rack = line[1]
        csv_dc = line[2]
        if(str.lower(csv_hostname) in zabbix_hostnames):
            zabbix.host.update(hostid=Get_Host_ID(csv_hostname), inventory_mode = "0",inventory={"location":Get_DCName(csv_dc),"site_rack": csv_rack})

Update_Inv_Data()











