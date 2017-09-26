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

# todo:
# CRUD VirtualService
# CRUD Pool
# CRUD

import requests
import os
import re
import json

__opts__ = {}

def _auth(**kwargs):
    '''
    Set up Contrail API credentials.
    '''
    cluster_ip = __pillar__['avinetworks']['api']['ip']
    username = __pillar__['avinetworks']['api']['user']
    password = __pillar__['avinetworks']['api']['password']
    login = requests.post('https://' + cluster_ip + '/login',
                          verify=False,
                          data={'username': username, 'password': password})
    return login


def _get_input_type(_input):
    test = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    result = test.match(_input)
    if result:
        return "V4"
    return "DNS"


def logout(login):
    cluster_ip = __pillar__['avinetworks']['api']['ip']
    requests.post('https://' + cluster_ip + '/logout',
                  verify=False,
                  headers={'X-CSRFToken': login.cookies['csrftoken'],
                           'Referer': 'https://' + cluster_ip},
                  cookies=login.cookies)


def send_request_get(_command):
    cluster_ip = __pillar__['avinetworks']['api']['ip']
    login = _auth()
    url = "https://" + os.path.join(cluster_ip, "api", _command)
    try:
        resp = requests.get(url,
                            verify=False,
                            cookies=dict(sessionid=login.cookies['sessionid']))
    except requests.exceptions.RequestException as ex:
        print ex
        return None
    logout(login)
    return resp


def send_request_post(_command, data):
    cluster_ip = __pillar__['avinetworks']['api']['ip']
    login = _auth()
    url = "https://" + os.path.join(cluster_ip, "api", _command)
    try:
        resp = requests.post(url,
                             verify=False,
                             headers={'X-CSRFToken': login.cookies['csrftoken'],
                                      'Referer': 'https://' + cluster_ip,
                                      'Content-Type': 'application/json'},
                             cookies=login.cookies,
                             data=json.dumps(data))
    except requests.exceptions.RequestException as ex:
        print ex
        return None
    logout(login)
    return resp


def send_request_put(_command, data):
    cluster_ip = __pillar__['avinetworks']['api']['ip']
    login = _auth()
    url = "https://" + os.path.join(cluster_ip, "api", _command)
    try:
        resp = requests.put(url,
                            verify=False,
                            headers={'X-CSRFToken': login.cookies['csrftoken'],
                                     'Referer': 'https://' + cluster_ip,
                                     'Content-Type': 'application/json'},
                            cookies=login.cookies,
                            data=json.dumps(data))
    except requests.exceptions.RequestException as ex:
        print ex
        return None
    logout(login)
    return resp


def send_request_delete(_command, uuid, **kwargs):
    cluster_ip = __pillar__['avinetworks']['api']['ip']
    login = _auth()
    url = "https://" + os.path.join(cluster_ip, "api", _command, uuid)
    try:
        resp = requests.delete(url,
                               verify=False,
                               headers={'X-CSRFToken': login.cookies['csrftoken'],
                                        'Referer': 'https://' + cluster_ip,
                                        'Content-Type': 'application/json'},
                               cookies=login.cookies)
    except requests.exceptions.RequestException as ex:
        print ex
        return None
    logout(login)
    return resp


def pool_list(**kwargs):
    command = "pool"
    ret = send_request_get(command)
    return ret.json()


def pool_get(name, **kwargs):
    pools = pool_list()
    for pool in pools['results']:
        if name == pool['name'] or name == pool['uuid']:
            return pool
    return {'result': False,
            'Error': "Error in the retrieving pool."}


def pool_create(name, lb_algorithm='LB_ALGORITHM_ROUND_ROBIN', server_port=80, servers=None, **kwargs):
    command = 'pool'
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': ''}

    if not servers:
        ret['result'] = False
        ret['comment'] = "Error: Server not defined"
        return ret

    check = pool_get(name)
    if 'Error' not in check:
        ret['comment'] = "Pool " + name + " already exists"
        return ret

    if __opts__['test']:
        ret['result'] = None
        ret['comment'] = "Pool " + name + " will be created"
        return ret

    data = {}
    data["lb_algorithm"] = lb_algorithm
    data["default_server_port"] = server_port
    data["name"] = name
    server_data = []
    for server in servers:
        servers_type = _get_input_type(server)
        srv = {'ip': {'type': servers_type,
                      'addr': server}}
        server_data.append(srv)
    data['servers'] = server_data
    result = send_request_post(command, data)
    if result:
        ret['comment'] = "Pool " + name + " has been created"
        ret['changes'] = {'Pool': {'old': '', 'new': name}}
    else:
        ret['result'] = False
        ret['comment'] = {"Error": "Pool was not created", "reason": result}
    return ret


def pool_delete(name, **kwargs):
    command = 'pool'
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': ''}

    check = pool_get(name)
    if not check:
        ret['comment'] = "Pool " + name + " is already deleted"
        return ret

    if __opts__['test']:
        ret['result'] = None
        ret['comment'] = "Pool " + name + " will be deleted"
        return ret

    result = send_request_delete(command, check['uuid'])
    if result:
        ret['comment'] = "Pool " + name + " has been deleted"
        ret['changes'] = {'Pool': {'old': name, 'new': ''}}
    else:
        ret['result'] = False
        ret['comment'] = "Error: Pool was not created"
    return ret


def virtual_service_list():
    command = "virtualservice"
    ret = send_request_get(command)
    return ret.json()


def virtual_service_get(name):
    vservices = virtual_service_list()
    for vs in vservices['results']:
        if name == vs['name'] or name == vs['uuid']:
            return vs
    return None


def virtual_service_create():
    command = "virtualservice"
    vip = [{'auto_allocate_floating_ip': True,
            'auto_allocate_ip': True,
            'ipam_network_subnet': {
                'subnet': {
                    "mask": 24,
                    "ip_addr": {
                        "type": "V4",
                        "addr": "192.168.32.0"
                    }
                }
            }
            }]
    service = [{"port": 8080}]
    data = {'name': "test",
            'services': service,
            'vip': vip
            }
    ret = send_request_post(command, data)
    return ret.json()


def cloud_list():
    command = "cloud"
    ret = send_request_get(command)
    return ret.json()


def cloud_get(name, **kwargs):
    clouds = cloud_list()
    for cloud in clouds['results']:
        if name == cloud['name'] or name == cloud['uuid']:
            return cloud
    return {'result': False,
            'Error': "Error in the retrieving cloud."}


def cloud_create(name, mtu=1500, dhcp_enabled=False, openstack=None,  **kwargs):
    command = 'cloud'
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': ''}

    check = cloud_get(name)
    if 'Error' not in check:
        ret['comment'] = "Cloud " + name + " already exists"
        return ret

    if __opts__['test']:
        ret['result'] = None
        ret['comment'] = "Cloud " + name + " will be created"
        return ret

    data = {}
    data["name"] = name
    data["vtype"] = "CLOUD_OPENSTACK"
    data["license_type"] = "LIC_CORES"
    data["mtu"] = mtu
    data["dhcp_enabled"] = dhcp_enabled

    if openstack:
        openstack_conf = {}
        openstack_conf['username'] = openstack['username']
        openstack_conf['password'] = openstack['password']
        openstack_conf['admin_tenant'] = openstack['admin_tenant']
        openstack_conf['auth_url'] = openstack['auth_url']
        openstack_conf['mgmt_network_name'] = openstack['mgmt_network_name']
        openstack_conf['privilege'] = 'WRITE_ACCESS'
        openstack_conf['region'] = openstack['region']
        openstack_conf['hypervisor'] = 'KVM'
        openstack_conf['free_floatingips'] = openstack['free_floatingips']
        openstack_conf['img_format'] = 'OS_IMG_FMT_QCOW2'
        openstack_conf['use_internal_endpoints'] = openstack['use_internal_endpoints']
        openstack_conf['insecure'] = openstack['insecure']
        openstack_conf['contrail_endpoint'] = openstack['contrail_endpoint']
        role_mapping = {'os_role': '*', 'avi_role': openstack['avi_role']}
        openstack_conf['role_mapping'] = role_mapping
        data["openstack_configuration"] = openstack_conf
    result = send_request_post(command, data)
    if result:
        ret['comment'] = "Cloud " + name + " has been created"
        ret['changes'] = {'Cloud': {'old': '', 'new': name}}
    else:
        ret['result'] = False
        ret['comment'] = {"Error": "Cloud was not created", "reason": result}
    return ret


def cloud_delete(name, **kwargs):
    command = 'cloud'
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': ''}

    check = cloud_get(name)
    if not check:
        ret['comment'] = "Cloud " + name + " is already deleted"
        return ret

    if __opts__['test']:
        ret['result'] = None
        ret['comment'] = "Cloud " + name + " will be deleted"
        return ret

    result = send_request_delete(command, check['uuid'])
    if result:
        ret['comment'] = "Cloud " + name + " has been deleted"
        ret['changes'] = {'Cloud': {'old': name, 'new': ''}}
    else:
        ret['result'] = False
        ret['comment'] = "Error: Cloud was not created"
    return ret


def cluster_get():
    command = "cluster"
    ret = send_request_get(command)
    return ret.json()


def cluster_update(name, nodes, virtual_ip=None, **kwargs):
    command = 'cluster'
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': ''}

    if __opts__['test']:
        ret['result'] = None
        ret['comment'] = "Cluster " + name + " will be updated"
        return ret

    data = {}
    data["name"] = name

    vip = {'addr': virtual_ip,
           'type': _get_input_type(virtual_ip)}
    data['virtual_ip'] = vip
    nodes_data = []
    for node in nodes:
        node_type = _get_input_type(node['addr'])
        n = {'ip': {'type': node_type,
                    'addr': node['addr']},
             'name': node['name']}
        nodes_data.append(n)
    data['nodes'] = nodes_data

    result = send_request_put(command, data)
    if result:
        ret['comment'] = "Cluster " + name + " has been updated"
        ret['changes'] = {'Pool': {'old': 'unknown', 'new': name}}
    else:
        ret['result'] = False
        ret['comment'] = {"Error": "Cluster was not updates", "reason": result.json()['error']}
    return ret
