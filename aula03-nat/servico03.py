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

CLIENTS = 10
TIMEOUT = 50

def enableNAT(host):
    # Flush any currently active rules
    host.cmd('iptables -F')
    host.cmd('iptables -t nat -F')

    # Create default entries for unmatched traffic
    host.cmd( 'iptables -P INPUT ACCEPT' )
    host.cmd( 'iptables -P OUTPUT ACCEPT' )
    host.cmd( 'iptables -P FORWARD ACCEPT' )

    # Configure NAT
    host.cmd( 'iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE' )

def enableForwarding(host):
    host.cmd('sysctl -w net.ipv4.ip_forward=1')

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
    primaryIP = '192.168.0.254/24'
    secondaryIP = '192.168.100.254/24'
    hostSRV = net.addHost('hsrv', ip=primaryIP, inNamespace=False)
    net.addLink(hostSRV, s1)
    net.addLink(hostSRV, s2)
    setIPaddr(hostSRV, 'eth1', secondaryIP)
    enableForwarding(hostSRV)
    enableNAT(hostSRV)
    hostSRV.dhcpServer = True

    info( '*** Add Clients and links\n')
    hostsPerSegment=CLIENTS/2
    # S1 hosts
    for i in range(1, hostsPerSegment+1):
        host = net.addHost('h%s' % i, ip='0.0.0.0', mac='00:00:00:00:00:%02x' % i)
        net.addLink(host, s1)
        host.dhcpServer = False

    # S2 hosts
    for i in range(1, hostsPerSegment+1):
        host = net.addHost('h%s' % (i+hostsPerSegment), ip='0.0.0.0', mac='00:00:00:00:01:%02x' % i)
        net.addLink(host, s2)
        host.dhcpServer = False

    info( '*** Starting network\n')
    net.build()

    info( '*** Starting switches\n')
    net.start()

    info( '*** Starting Services\n')
    run_dhcpd_server(hostSRV)

    info( '*** Starting Clients\n')
    for host in net.hosts:
        run_dhcp_client(host)

    CLI(net)
    net.stop()

if __name__ == '__main__':
    clean()
    setLogLevel( 'info' )
    myNetwork()
    clean()
