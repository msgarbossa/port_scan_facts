import os
import yaml

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_port_scan_facts(host):
    f = host.file('/tmp/port_scan_facts')
    assert f.exists

    data = f.content
    fact_dict = yaml.load(data)
    assert fact_dict['www.google.com:443'] > 0
    assert fact_dict['www.microsoft.com:443'] > 0
