#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import Link, TCLink
import time
import glob, os


class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()



def mytopo():

        net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )
        # Define Transport Network
        r1 = net.addHost('r1', cls=LinuxRouter, ip='10.0.10.1/24')
        r2 = net.addHost('r2', cls=LinuxRouter, ip='11.0.1.2/24')
        r3 = net.addHost('r3', cls=LinuxRouter, ip='22.0.2.2/24')
        r4 = net.addHost('r4', cls=LinuxRouter, ip='44.0.4.2/24')
        r5 = net.addHost('r5', cls=LinuxRouter, ip='66.0.6.2/24')
	r6 = net.addHost('r6', cls=LinuxRouter, ip='33.0.3.2/24')
        r7 = net.addHost('r7', cls=LinuxRouter, ip='77.0.7.2/24')
        r8 = net.addHost('r8', cls=LinuxRouter, ip='10.0.20.1/24')

	# Add Open Flow Controller
        c0 = net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=6633 )

        # Add Access Network Switches
        s1 = net.addSwitch('s1')
        s2 = net.addSwitch('s2')

	# Add Edge Network Switches
	s3 = net.addSwitch('s3')
	s4 = net.addSwitch('s4')

        # Add Router-Switch Links
        net.addLink(
                     r1,s1,
                     intfName1='r1-eth0',
                     params1={'ip': '10.0.10.1/24'})

	net.addLink(
                     r1,s3,
                     intfName1='r1-eth2',
                     params1={'ip': '10.0.30.1/24'})

        net.addLink(
                     r8,s2,
                     intfName1='r8-eth0',
                     params1={'ip': '10.0.20.1/24'})

	net.addLink(
                     r8,s4,
                     intfName1='r8-eth2',
                     params1={'ip': '10.0.40.1/24'})

        # Add Router-Router Link With Subnet Defination
        net.addLink(r1,
                     r2,
                     intfName1='r1-eth1',
                     intfName2='r2-eth0',
                     params1={'ip': '11.0.1.1/24'},
                     params2={'ip': '11.0.1.2/24'})

        net.addLink(r2,
                     r3,
                     intfName1='r2-eth1',
                     intfName2='r3-eth0',
                     params1={'ip': '22.0.2.1/24'},
                     params2={'ip': '22.0.2.2/24'})

        net.addLink(r2,
                     r6,
                     intfName1='r2-eth2',
                     intfName2='r6-eth0',
                     params1={'ip': '33.0.3.1/24'},
                     params2={'ip': '33.0.3.2/24'})

        net.addLink(r3,
                     r4,
                     intfName1='r3-eth1',
                     intfName2='r4-eth0',
                     params1={'ip': '44.0.4.1/24'},
                     params2={'ip': '44.0.4.2/24'})

        net.addLink(r4,
                     r6,
                     intfName1='r4-eth1',
                     intfName2='r6-eth1',
                     params1={'ip': '55.0.5.1/24'},
                     params2={'ip': '55.0.5.2/24'})
        net.addLink(r6,
                     r7,
                     intfName1='r6-eth2',
                     intfName2='r7-eth0',
                     params1={'ip': '77.0.7.1/24'},
                     params2={'ip': '77.0.7.2/24'})

        net.addLink(r4,
                     r5,
                     intfName1='r4-eth2',
                     intfName2='r5-eth0',
                     params1={'ip': '66.0.6.1/24'},
                     params2={'ip': '66.0.6.2/24'})
        net.addLink(r5,
                     r8,
                     intfName1='r5-eth1',
                     intfName2='r8-eth1',
                     params1={'ip': '88.0.8.2/24'},
                     params2={'ip': '88.0.8.1/24'})


        net.addLink(r7,
                     r5,
                     intfName1='r7-eth1',
                     intfName2='r5-eth2',
                     params1={'ip': '99.0.9.1/24'},
                     params2={'ip': '99.0.9.2/24'})


        # Adding Access Hosts With Specification of Default Route
        h1 = net.addHost(name='h1',
                          ip='10.0.10.11/24',
                          defaultRoute='via 10.0.10.1')
        h2 = net.addHost(name='h2',
                          ip='10.0.10.12/24',
                          defaultRoute='via 10.0.10.1')

        h3 = net.addHost(name='h3',
                          ip='10.0.20.11/24',
                          defaultRoute='via 10.0.20.1')

        h4 =  net.addHost(name='h4',
                          ip='10.0.20.12/24',
                          defaultRoute='via 10.0.20.1')

	# Adding Edge Hosts With Specification of Default Route
	e1 =  net.addHost(name='e1',
                          ip='10.0.30.11/24',
                          defaultRoute='via 10.0.30.1')

	e2 =  net.addHost(name='e2',
                          ip='10.0.40.11/24',
                          defaultRoute='via 10.0.40.1')


      # Add Access Host-Switch Links
        net.addLink(h1, s1)
        net.addLink(h2, s1)
        net.addLink(h3, s2)
        net.addLink(h4, s2)
	
      # Add Edge Host-Switch Links
	net.addLink(e1, s3)
	net.addLink(e2, s4)

      # Build Network & Start Controller & Switches
        net.build()
        c0.start()
        
	s1.start( [c0] )
        s2.start( [c0] )

	s3.start( [c0] )
	s4.start( [c0] )

        # Define Router Inetrface MAC Address
        info(net['r1'].cmd("ifconfig r1-eth0 hw ether 00:00:00:00:01:01"))
	info(net['r1'].cmd("ifconfig r1-eth2 hw ether 00:00:00:00:01:03"))

        info(net['r8'].cmd("ifconfig r8-eth0 hw ether 00:00:00:00:08:01"))
	info(net['r8'].cmd("ifconfig r8-eth2 hw ether 00:00:00:00:08:03"))

	# OVS - Open Flow Control Instructions
        info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=1,arp,actions=flood"))
        info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=65535,ip,dl_dst=00:00:00:00:01:01,actions=output:1"))
        info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_dst=10.0.10.11,actions=output:2"))
        info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_dst=10.0.10.12,actions=output:3"))

        info(net['s2'].cmd("ovs-ofctl add-flow s2 priority=1,arp,actions=flood"))
        info(net['s2'].cmd("ovs-ofctl add-flow s2 priority=65535,ip,dl_dst=00:00:00:00:08:01,actions=output:1"))
        info(net['s2'].cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_dst=10.0.20.11,actions=output:2"))
        info(net['s2'].cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_dst=10.0.20.12,actions=output:3"))
   
	info(net['s3'].cmd("ovs-ofctl add-flow s3 priority=1,arp,actions=flood"))
        info(net['s3'].cmd("ovs-ofctl add-flow s3 priority=65535,ip,dl_dst=00:00:00:00:01:03,actions=output:1"))
        info(net['s3'].cmd("ovs-ofctl add-flow s3 priority=10,ip,nw_dst=10.0.30.11,actions=output:2"))
      
	info(net['s4'].cmd("ovs-ofctl add-flow s4 priority=1,arp,actions=flood"))
        info(net['s4'].cmd("ovs-ofctl add-flow s4 priority=65535,ip,dl_dst=00:00:00:00:08:03,actions=output:1"))
        info(net['s4'].cmd("ovs-ofctl add-flow s4 priority=10,ip,nw_dst=10.0.40.11,actions=output:2"))
   
	# Via Route Info Addition 
        info(net['r1'].cmd("ip route add 22.0.2.0/24  via 11.0.1.2 dev r1-eth1"))
        info(net['r1'].cmd("ip route add 44.0.4.0/24   via 11.0.1.2 dev r1-eth1"))
        info(net['r1'].cmd("ip route add 66.0.6.0/24    via 11.0.1.2 dev r1-eth1"))
        info(net['r1'].cmd("ip route add 44.0.4.0/24    via 11.0.1.2 dev r1-eth1"))
        info(net['r1'].cmd("ip route add 88.0.8.0/24  via 11.0.1.2 dev r1-eth1"))
   
        info(net['r1'].cmd("ip route add 33.0.3.0/24  via 11.0.1.2 dev r1-eth1"))
        info(net['r1'].cmd("ip route add 77.0.7.0/24  via 11.0.1.2 dev r1-eth1"))
        info(net['r1'].cmd("ip route add 99.0.9.0/24  via 11.0.1.2 dev r1-eth1"))
        info(net['r1'].cmd("ip route add 55.0.5.0/24  via 11.0.1.2 dev r1-eth1"))
      
        info(net['r2'].cmd("ip route add 44.0.4.0/24  via 22.0.2.2  dev r2-eth1"))
        info(net['r2'].cmd("ip route add 66.0.6.0/24  via 22.0.2.2 dev r2-eth1"))
        info(net['r2'].cmd("ip route add 88.0.8.0/24   via 22.0.2.2 dev r2-eth1"))
       
        info(net['r2'].cmd("ip route add 77.0.7.0/24   via 33.0.3.2 dev r2-eth2"))
        info(net['r2'].cmd("ip route add 55.0.5.0/24   via 33.0.3.2 dev r2-eth2"))
        info(net['r2'].cmd("ip route add 99.0.9.0/24   via 33.0.3.2 dev r2-eth2"))
      
        info(net['r3'].cmd("ip route add 11.0.1.0/24   via 22.0.2.1 dev r3-eth0"))
        info(net['r3'].cmd("ip route add 33.0.3.0/24   via 22.0.2.1 dev r3-eth0"))
        info(net['r3'].cmd("ip route add 55.0.5.0/24   via 44.0.4.2 dev r3-eth1"))
        info(net['r3'].cmd("ip route add 77.0.7.0/24   via 44.0.4.2 dev r3-eth1"))
        info(net['r3'].cmd("ip route add 66.0.6.0/24   via 44.0.4.2 dev r3-eth1"))
        info(net['r3'].cmd("ip route add 99.0.9.0/24   via 44.0.4.2 dev r3-eth1"))
        info(net['r3'].cmd("ip route add 88.0.8.0/24   via 44.0.4.2 dev r3-eth1"))
       
        info(net['r4'].cmd("ip route add 11.0.1.0/24   via 44.0.4.1 dev r4-eth0"))
        info(net['r4'].cmd("ip route add 22.0.2.0/24   via 44.0.4.1 dev r4-eth0"))
        info(net['r4'].cmd("ip route add 33.0.3.0/24   via 55.0.5.2 dev r4-eth1"))
       
        info(net['r4'].cmd("ip route add 77.0.7.0/24   via 66.0.6.2 dev r4-eth2"))
        info(net['r4'].cmd("ip route add 99.0.9.0/24   via 66.0.6.2 dev r4-eth2"))
        info(net['r4'].cmd("ip route add 88.0.8.0/24   via 66.0.6.2 dev r4-eth2"))
       
        info(net['r5'].cmd("ip route add 44.0.4.0/24   via 66.0.6.1 dev r5-eth0"))
        info(net['r5'].cmd("ip route add 22.0.2.0/24   via 66.0.6.1 dev r5-eth0"))
        info(net['r5'].cmd("ip route add 11.0.1.0/24   via 66.0.6.1 dev r5-eth0"))
       
        info(net['r5'].cmd("ip route add 33.0.3.0/24   via 66.0.6.1 dev r5-eth0"))
        info(net['r5'].cmd("ip route add 55.0.5.0/24   via 66.0.6.1 dev r5-eth0"))
        info(net['r5'].cmd("ip route add 77.0.7.0/24   via 99.0.9.1 dev r5-eth2"))
     
        info(net['r6'].cmd("ip route add 11.0.1.0/24   via 33.0.3.1 dev r6-eth0"))
        info(net['r6'].cmd("ip route add 22.0.2.0/24   via 33.0.3.1 dev r6-eth0"))
        info(net['r6'].cmd("ip route add 44.0.4.0/24   via 55.0.5.1 dev r6-eth1"))
        info(net['r6'].cmd("ip route add 66.0.6.0/24   via 33.0.3.1 dev r6-eth0"))
        info(net['r6'].cmd("ip route add 99.0.9.0/24   via 77.0.7.2 dev r6-eth2"))
        info(net['r6'].cmd("ip route add 88.0.8.0/24   via 77.0.7.2 dev r6-eth2"))
      
        info(net['r7'].cmd("ip route add 11.0.1.0/24   via 77.0.7.1 dev r7-eth0"))
        info(net['r7'].cmd("ip route add 22.0.2.0/24   via 77.0.7.1 dev r7-eth0"))
        info(net['r7'].cmd("ip route add 33.0.3.0/24   via 77.0.7.1 dev r7-eth0"))
        info(net['r7'].cmd("ip route add 55.0.5.0/24   via 77.0.7.1 dev r7-eth0"))
        info(net['r7'].cmd("ip route add 44.0.4.0/24   via 77.0.7.1 dev r7-eth0"))
        info(net['r7'].cmd("ip route add 66.0.6.0/24   via 99.0.9.2 dev r7-eth1"))
        info(net['r7'].cmd("ip route add 88.0.8.0/24   via 99.0.9.2 dev r7-eth1"))
       
        info(net['r8'].cmd("ip route add 11.0.1.0/24   via 88.0.8.2 dev r8-eth1"))
        info(net['r8'].cmd("ip route add 22.0.2.0/24   via 88.0.8.2 dev r8-eth1"))
        info(net['r8'].cmd("ip route add 33.0.3.0/24   via 88.0.8.2 dev r8-eth1"))
        info(net['r8'].cmd("ip route add 44.0.4.0/24   via 88.0.8.2 dev r8-eth1"))
        info(net['r8'].cmd("ip route add 55.0.5.0/24   via 88.0.8.2 dev r8-eth1"))
        info(net['r8'].cmd("ip route add 66.0.6.0/24   via 88.0.8.2 dev r8-eth1"))
        info(net['r8'].cmd("ip route add 77.0.7.0/24   via 88.0.8.2 dev r8-eth1"))
        info(net['r8'].cmd("ip route add 99.0.9.0/24   via 88.0.8.2 dev r8-eth1"))

    # GENEVE Tunnel Between R1 & R8

    # GENEVE Config for R1
        r1.cmd('ip link add dev gnv0 type geneve remote 88.0.8.1 vni 123')
        r1.cmd('ip link set gnv0 up')
        r1.cmd('ip addr add 111.111.111.1/24 dev gnv0')
        r1.cmd('ip route add 10.0.20.11 encap ip via 111.111.111.2 dev gnv0')

        r1.cmd('ip link add dev gnv1 type geneve remote 88.0.8.1 vni 456')
        r1.cmd('ip link set gnv1 up')
        r1.cmd('ip addr add 222.222.222.1/24 dev gnv1')
        r1.cmd('ip route add 10.0.20.12 encap ip via 222.222.222.2 dev gnv1')

    # GENEVE Config for R8
        r8.cmd('ip link add dev gnv0 type geneve remote 11.0.1.1 vni 123')
        r8.cmd('ip link set gnv0 up')
        r8.cmd('ip addr add 111.111.111.2/24 dev gnv0')
        r8.cmd('ip route add 10.0.10.11 encap ip via 111.111.111.1 dev gnv0')

        r8.cmd('ip link add dev gnv1 type geneve remote 11.0.1.1 vni 456')
        r8.cmd('ip link set gnv1 up')
        r8.cmd('ip addr add 222.222.222.2/24 dev gnv1')
        r8.cmd('ip route add 10.0.10.12 encap ip via 222.222.222.1 dev gnv1')

        CLI(net)
        net.stop() 

if __name__ == '__main__':
    setLogLevel('info')
    mytopo()
