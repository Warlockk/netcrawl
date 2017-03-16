'''
Created on Mar 13, 2017

@author: Wyko
'''

from faker import Factory

import pytest

from netcrawl.devices.base import Interface
from tests.helpers import Cisco


def _new_interface():

    fake = Factory.create()
    
    # then add new provider to faker instance
    fake.add_provider(Cisco)
    
    i = Interface()
 
    addr, mask = fake.ipv4(network=True).split('/')
     
    i.interface_ip= addr 
    i.interface_subnet= mask
     
    i.interface_description= fake.sentence(nb_words=6, variable_nb_words=True)
     
    i.interface_type= fake.interfaceType() 
    i.interface_number= fake.interfaceNumber()
    i.interface_name= i.interface_type + i.interface_number
    
    i.get_network_ip()
    
    return i

@pytest.mark.parametrize("ip, mask, expected", [
    ('169.98.102.209', '255.255.255.0', '169.98.102.0'),
    ('207.17.208.94', '255.255.0.0', '207.17.0.0'),
    ('50.204.211.184', '255.0.0.0', '50.0.0.0'),
    ('116.219.191.68', '255.255.254.0', '116.219.190.0'),
    ('102.168.167.157', '0.0.0.0', '0.0.0.0'),
    ('40.187.188.120', '255.255.255.128', '40.187.188.0'),
    ])    
def test_returns_correct_network_ip(ip, mask, expected):
    i= _new_interface()
    i.interface_ip= ip
    i.interface_subnet= mask
    i.get_network_ip()
    assert i.network_ip == expected
    
    
