{%- from "avinetworks/map.jinja" import server with context %}
{%- if server.enabled %}

avinetworks_tenant:
  keystone.tenant_present:
    - profile: {{ server.identity }}
    - name: avinetworks
    - description: Avi Networks Vantage service project

avinetworks_flavor:
  novang.flavor_present:
  - name: avinetworks
  - profile: {{ server.identity }}
  - flavor_id: avinetworks
  - ram: 8
  - disk: 160
  - vcpus: 4
  - require:
    - keystone: avinetworks_tenant

avinetworks_image:
  glanceng.image_present:
  - name: avinetworks
  - profile: {{ server.identity }}
  - visibility: public
  - protected: False
  - location: {{ server.image_location }}
  - require:
    - keystone: avinetworks_tenant

avinetworks_network:
  neutronng.network_present:
  - profile: {{ server.identity }}
  - name: avinetworks
  - tenant: avinetworks
  - require:
    - keystone: avinetworks_tenant

avinetworks_subnet:
  neutronng.subnet_present:
  - profile: {{ server.identity }}
  - name: avinetworks
  - tenant: avinetworks
  - network: avinetworks
  - cidr: 10.1.0.0/24
  - require:
    - keystone: avinetworks_tenant
    - neutronng: avinetworks_network

avinetworks_router:
  neutronng.router_present:
  - profile: {{ server.identity }}
  - name: avinetworks
  - tenant: avinetworks
  - interfaces:
    - avinetworks
  - gateway_network: {{ server.public_network }}
  - require:
    - keystone: avinetworks_tenant
    - neutronng: avinetworks_network
    - neutronng: avinetworks_subnet

avinetworks_secgroup:
  neutronng.security_group_present:
  - profile: {{ server.identity }}
  - name: avinetworks
  - tenant: avinetworks
  - rules:
    - direction: egress
      ethertype: IPv6
      protocol: tcp
      remote_ip_prefix: ::/0
      port_range_min: 0
      port_range_max: 65535
    - direction: egress
      ethertype: IPv4
      remote_ip_prefix: 0.0.0.0/0
      port_range_min: 0
      port_range_max: 65535
    - direction: ingress
      ethertype: IPv4
      protocol: icmp
      remote_ip_prefix: 0.0.0.0/0
    - direction: ingress
      ethertype: IPv4
      protocol: tcp
      port_range_min: 22
      port_range_max: 22
      remote_ip_prefix: 0.0.0.0/0
    - direction: ingress
      ethertype: IPv4
      protocol: tcp
      port_range_min: 80
      port_range_max: 80
      remote_ip_prefix: 0.0.0.0/0
    - direction: ingress
      ethertype: IPv4
      protocol: tcp
      port_range_min: 123
      port_range_max: 123
      remote_ip_prefix: 10.1.0.0/24
    - direction: ingress
      ethertype: IPv4
      protocol: tcp
      port_range_min: 443
      port_range_max: 443
      remote_ip_prefix: 0.0.0.0/0
  - require:
    - keystone: avinetworks_tenant

avinetworks_instance_01:
  novang.instance_present:
  - profile: {{ server.identity }}
  - tenant_name: avinetworks
  - name: avi_ctl01
  - flavor: avinetworks
  - image: avinetworks
  - security_groups:
    - avinetworks
  - networks:
    - name: avinetworks
      v4_fixed_ip: 10.1.0.10
  - require:
    - keystone: avinetworks_tenant
    - novang: avinetworks_flavor
    - glanceng: avinetworks_image
    - neutronng: avinetworks_network
    - neutronng: avinetworks_subnet
    - neutronng: avinetworks_secgroup

avinetworks_instance_02:
  novang.instance_present:
  - profile: {{ server.identity }}
  - tenant_name: avinetworks
  - name: avi_ctl02
  - flavor: avinetworks
  - image: avinetworks
  - security_groups:
    - avinetworks
  - networks:
    - name: avinetworks
      v4_fixed_ip: 10.1.0.11
  - require:
    - keystone: avinetworks_tenant
    - novang: avinetworks_flavor
    - glanceng: avinetworks_image
    - neutronng: avinetworks_network
    - neutronng: avinetworks_subnet
    - neutronng: avinetworks_secgroup

avinetworks_instance_03:
  novang.instance_present:
  - profile: {{ server.identity }}
  - tenant_name: avinetworks
  - name: avi_ctl03
  - flavor: avinetworks
  - image: avinetworks
  - security_groups:
    - avinetworks
  - networks:
    - name: avinetworks
      v4_fixed_ip: 10.1.0.12
  - require:
    - keystone: avinetworks_tenant
    - novang: avinetworks_flavor
    - glanceng: avinetworks_image
    - neutronng: avinetworks_network
    - neutronng: avinetworks_subnet
    - neutronng: avinetworks_secgroup

avinetworks_floating_ip_01:
  neutronng.floatingip_present:
  - profile: {{ server.identity }}
  - subnet: avinetworks
  - tenant_name: avinetworks
  - name: avi_ctl01
  - network: avinetworks
  - require:
    - keystone: avinetworks_tenant
    - neutronng: avinetworks_network
    - neutronng: avinetworks_subnet
    - novang: avinetworks_instance_01

avinetworks_floating_ip_02:
  neutronng.floatingip_present:
  - profile: {{ server.identity }}
  - subnet: avinetworks
  - tenant_name: avinetworks
  - name: avi_ctl02
  - network: avinetworks
  - require:
    - keystone: avinetworks_tenant
    - neutronng: avinetworks_network
    - neutronng: avinetworks_subnet
    - novang: avinetworks_instance_02

avinetworks_floating_ip_03:
  neutronng.floatingip_present:
  - profile: {{ server.identity }}
  - subnet: avinetworks
  - tenant_name: avinetworks
  - name: avi_ctl03
  - network: avinetworks
  - require:
    - keystone: avinetworks_tenant
    - neutronng: avinetworks_network
    - neutronng: avinetworks_subnet
    - novang: avinetworks_instance_03

{%- endif %}