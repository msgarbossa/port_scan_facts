#!/usr/bin/python

# from ansible.module_utils._text import to_text, to_bytes
from ansible.module_utils.basic import AnsibleModule

import socket
import time


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Mike Sgarbossa'
}

DOCUMENTATION = '''
---
module: port_scan_facts

short_description: Test TCP port connectivity

version_added: "2.8"

description:
    - Test TCP port connectivity to supplied list of targets

options:
    destinations:
        description:
            - list of targets.  Each list contains d_host or d_ip and d_port
        default: []]
        required: true

extends_documentation_fragment:
    - port_scan_facts

author:
    - Mike Sgarbossa
'''

EXAMPLES = '''
- name: Test connectivity to desintation host/ports
  port_scan_facts:
    destinations:
      - name: Google
        d_host: www.google.com
        d_port: 443
      - name: Microsoft
        d_host: www.microsoft.com
        d_port: 443
'''

RETURN = '''
ansible_facts:
    description: The results of the port scan
    type: dict
    returned: always
'''


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        destinations=dict(type='list', required=True)
    )

    # seed the result dict in the object
    # we primarily care about rc
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task

    # initialize result message
    result = dict(
        changed=False,
        original_message='',
        message='',
        rc=0,
        ansible_facts={}
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result['ansible_facts'] = {'port_scan_facts': test_destinations(module.params['destinations'])}

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def test_destinations(destinations):

    results = {}

    for i in range(len(destinations)):
        if 'd_ip' in destinations[i]:
            target = destinations[i]['d_ip']
        else:
            target = destinations[i]['d_host']
        port = destinations[i]['d_port']
        key = '{0}:{1}'.format(target, port)
        start = time.time()
        check = check_server(target, port)
        end = time.time()
        if check:
            results[key] = round((end - start) * 1000)
        else:
            results[key] = -1
    return results


def check_server(address, port):
    # Create a TCP socket
    s = socket.socket()
    if isinstance(port, str):
        port = int(port)
    s.settimeout(2)
    # print("Attempting to connect to %s on port %s" % (address, port))
    try:
        s.connect((address, port))
        # print("Connected to %s on port %s" % (address, port))
        return True
    except socket.error:
        # print("Connection to %s on port %s failed: %s" % (address, port, e))
        return False


def main():
    run_module()


if __name__ == '__main__':
    main()
