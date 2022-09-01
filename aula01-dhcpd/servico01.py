#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call


def run_dhcpd_server(host):
    srv = "dhcpd"
    cmd = "/usr/sbin/%s " % (srv)
    cmd += "-pf %s.pid -cf %s.conf -lf %s.leases" % (srv, srv, srv)
    cmd += "> dhcpd.log 2>&1"
    host.cmd("echo > %s.leases" % (srv))
    host.cmd(cmd)

def run_dhcp_client(host):
    cli = "dhclient"
    name = host.name
    cmd = "/usr/sbin/%s -v -nw %s-eth0" % (cli, name)
    host.cmd(cmd)


def myNetwork():
    net = Mininet( topo=None,
                   build=False )

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')

    info( '*** Add Server\n')

    info( '*** Add hosts and links\n')

    info( '*** Starting network\n')
    net.build()

    info( '*** Starting Services\n')

    info( '*** Starting switches\n')
    net.get('s1').start([])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

