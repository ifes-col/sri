#!/usr/bin/env python2

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

import os
import time

CLIENTS = 40
TIMEOUT = 50

def setIPaddr(host, iface, ipaddr):
    host_iface=host.name + '-' + iface
    info('%s: setting IP address %s at network interface %s\n' % (host.name, iface, ipaddr))
    host.cmd('ifconfig %s %s' % (host_iface, ipaddr))
    host.intf(host_iface).updateIP()

def _waitForanIP(host):
    info('%s waiting for an IP address' % host.name)
    i = 0
    while i < TIMEOUT:
        host.defaultIntf().updateIP()
        if host.IP():
            break
        info('.')
        i += 1
        time.sleep(0.1)
    info('\n')

def run_dhcpd_server(host):
    srv = "dhcpd"
    cmd = "/usr/sbin/%s " % (srv)
    cmd += "-pf %s.pid -cf %s.conf -lf %s.leases " % (srv, srv, srv)
    cmd += "> dhcpd.log 2>&1"
    host.cmd("echo > %s.leases" % (srv))
    host.cmd(cmd)

def run_dhcp_client(host):
    cli = "dhclient"
    name = host.name
    iface = host.defaultIntf()
    cmd = "/usr/sbin/%s -v -nw %s -pf dhclient-%s.pid" % (cli, iface, name)
    if (not host.dhcpServer):
        host.cmd(cmd)
        _waitForanIP(host)

def clean():
    info(' *** Cleaning up the previous setup...\n')
    os.system("killall -9 -w dhcpd")
    os.system("killall -9 -w dhclient")
    os.system("rm -f dhcpd.pid")
    os.system("rm -f dhclient*.pid")
    os.system("mn -c")


def myNetwork():
    net = Mininet()

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')

    info( '*** Add Server\n')
    # aqui voces devem inicializar o host "servidor"

    info( '*** Add Clients and links\n')
    for i in range(1, CLIENTS+1):
    # aqui voces devem inicializar os clientes

    info( '*** Starting network\n')
    net.build()

    info( '*** Starting switches\n')
    net.start()

    info( '*** Starting Services\n')
    # aqui voces devem inicializar o serviço

    info( '*** Starting Clients\n')
    for host in net.hosts:
        # aqui voces devem inicializar os clientes

    CLI(net)
    net.stop()

if __name__ == '__main__':
    clean()
    setLogLevel( 'info' )
    myNetwork()
    clean()