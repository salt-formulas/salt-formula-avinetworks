#!/usr/bin/python
# Copyright 2017 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''
Management of Contrail resources
================================

:depends:   - vnc_api Python module


Enforce the pool existence
--------------------------

.. code-block:: yaml

    create pool:
      avinetworks.pool_present:
        - name: testing_pool
        - lb_algorithm: LB_ALGORITHM_ROUND_ROBIN
        - server_port: 8080
        - servers:
          - "192.168.0.122"
          - "192.168.0.123"
          - "192.168.0.124"


Enforce the pool absence
------------------------

.. code-block:: yaml

    delete pool:
      avinetworks.pool_absent:
        - name: testing_pool


Enforce the cloud existence
---------------------------

.. code-block:: yaml

    create cloud:
      avinetworks.cloud_present:
        - name: testing_cloud
        - mtu: 1450
        - dhcp_enabled: True
        - openstack:
            username: admin
            password: password1*
            admin_tenant: avi-networks
            auth_url: http://10.167.4.100:5000/v2.0
            mgmt_network_name: avi-net
            privilege: WRITE_ACCESS
            region: RegionOne
            hypervisor: KVM
            free_floatingips: True
            img_format: OS_IMG_FMT_QCOW2
            use_internal_endpoints: True
            insecure: False
            contrail_endpoint: http://10.167.4.200:9100
            os_role: '*'
            avi_role: Tenant-Admin


Enforce the cloud absence
-------------------------

.. code-block:: yaml

    delete cloud:
      avinetworks.cloud_absent:
        - name: testing_cloud


Enforce the cluster present
---------------------------

.. code-block:: yaml

    update cluster:
      avinetworks.cluster_present:
        - name: my_cluster
        - virtual_ip: 172.17.32.252
        - nodes:
          - name: avi01
            addr: 172.17.32.228
          - name: avi02
            addr: 172.17.32.235
          - name: avi03
            addr: 172.17.32.232

Enforce the useraccount update
------------------------------

.. code-block:: yaml

    update admin password:
      avinetworks.useraccount_update:
        - old_password: password1*
        - new_password: password12*
        - full_name: Administrator  (optional)
        - email: admin@domain.com   (optional)
'''


def __virtual__():
    '''
    Load Avinetworks module
    '''
    return 'avinetworks'


def pool_present(name, lb_algorithm='LB_ALGORITHM_ROUND_ROBIN', server_port=80, servers=None, **kwargs):
    '''
    Ensures that the Avinetworks pool exists.

    :param name:          Pool name
    :param server_port:   Traffic sent to servers will use this destination server port unless overridden by the server's specific port attribute.
    :param lb_algorithm:  The load balancing algorithm will pick a server within the pool's list of available servers
    :param servers:       The pool directs load balanced traffic to this list of destination servers. The servers can be configured by IP address, name, network or via IP Address

    lb_algorithm choices:
      - LB_ALGORITHM_ROUND_ROBIN
      - LB_ALGORITHM_LEAST_LOAD
      - LB_ALGORITHM_FEWEST_TASKS
      - LB_ALGORITHM_RANDOM
      - LB_ALGORITHM_FEWEST_SERVERS
      - LB_ALGORITHM_CONSISTENT_HASH
      - LB_ALGORITHM_FASTEST_RESPONSE
      - LB_ALGORITHM_LEAST_CONNECTIONS
    '''
    ret = __salt__['avinetworks.pool_create'](name, lb_algorithm, server_port, servers, **kwargs)
    if len(ret['changes']) == 0:
        pass
    return ret


def pool_absent(name, **kwargs):
    '''
    Ensure that the Avinetworks pool doesn't exist

    :param name: The name of the pool that should not exist
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Pool "{0}" is already absent'.format(name)}
    result = __salt__['avinetworks.pool_get'](name, **kwargs)
    if 'Error' not in result:
        ret = __salt__['avinetworks.pool_delete'](name, **kwargs)
    return ret


def cloud_present(name, mtu=1500, dhcp_enabled=False, openstack=None, **kwargs):
    '''
    Ensures that the Avinetworks Cloud exists.

    :param name:            Cloud name [string]
    :param mtu:             MTU setting for the cloud [uint32]
    :param dhcp_enabled:    Select the IP address management scheme [bool]
    :param openstack:       The OpenStack configuration [dict]

    openstack_params:
        :param username:                The username Avi Vantage will use when authenticating to Keystone. [string]
        :param password:                The password Avi Vantage will use when authenticating to Keystone. [string]
        :param admin_tenant:            OpenStack admin tenant (or project) information. [string]
        :param auth_url:                Auth URL for connecting to keystone. If this is specified, any value provided for keystone_host is ignored. [string]
        :param mgmt_network_name:       Avi Management network name or cidr [string]
        :param privilege:               Access privilege. [enum] {WRITE_ACCESS, READ_ACCESS, NO_ACCESS}
        :param region:                  Region name [string]
        :param hypervisor:              Default hypervisor type. [enum] {DEFAULT, VMWARE_VSAN, VMWARE_ESX, KVM}
        :param free_floatingips:        Free unused floating IPs. [bool]
        :param img_format:              If OS_IMG_FMT_RAW, use RAW images else use QCOW2 or streamOptimized/flat VMDK as appropriate. [enum]
        :param use_internal_endpoints:  Use internalURL for OpenStack endpoints instead of the default publicURL [bool]
        :param insecure:                Allow self-signed certificates when communicating with https service endpoints. [bool]
        :param contrail_endpoint:       Contrail VNC endpoint url (example http://10.10.10.100:8082). [string]
        :param os_role:                 Role name in OpenStack [string]
        :param avi_role:                Role name in Avi [string]

    '''

    ret = __salt__['avinetworks.cloud_create'](name, mtu, dhcp_enabled, openstack, **kwargs)
    if len(ret['changes']) == 0:
        pass
    return ret

def cloud_absent(name, **kwargs):
    '''
    Ensure that the Avinetworks cloud doesn't exist

    :param name: The name of the cloud that should not exist
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Cloud "{0}" is already absent'.format(name)}
    result = __salt__['avinetworks.cloud_get'](name, **kwargs)
    if 'Error' not in result:
        ret = __salt__['avinetworks.cloud_delete'](name, **kwargs)
    return ret


def cluster_present(name, nodes, virtual_ip=None, **kwargs):
    '''
    Ensures that the Avinetworks pool exists.

    :param name:          Pool name
    :param server_port:   Traffic sent to servers will use this destination server port unless overridden by the server's specific port attribute.
    :param lb_algorithm:  The load balancing algorithm will pick a server within the pool's list of available servers
    :param servers:       The pool directs load balanced traffic to this list of destination servers. The servers can be configured by IP address, name, network or via IP Address
    '''
    ret = __salt__['avinetworks.cluster_update'](name, nodes, virtual_ip, **kwargs)
    if len(ret['changes']) == 0:
        pass
    return ret


def useraccount_update(old_password, new_password, full_name=None, email=None, **kwargs):
    '''
    Update used user account.

    :param old_password:   Password used for this api connection
    :param new_password:   Traffic sent to servers will use this destination server port unless overridden by the server's specific port attribute.
    :param full_name:      The load balancing algorithm will pick a server within the pool's list of available servers
    :param email:          The pool directs load balanced traffic to this list of destination servers. The servers can be configured by IP address, name, network or via IP Address
    '''
    ret = __salt__['avinetworks.useraccount_update'](old_password=old_password, password=new_password, full_name=full_name, email=email, **kwargs)
    if len(ret['changes']) == 0:
        pass
    return ret
