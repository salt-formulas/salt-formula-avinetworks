{%- from "avinetworks/map.jinja" import client with context %}
{%- if client.enabled %}

{%- if client.cluster.enabled %}
update_avinetworks_cluster:
  avinetworks.cluster_present:
    - name: {{ client.cluster.name }}
    - virtual_ip: {{ client.cluster.virtual_ip }}
    - nodes:
      {%- for node in client.cluster.nodes %}
      - name: {{ node.name }}
        addr: {{ node.addr }}
      {%- endfor %}
{%- endif %}


{%- if client.cloud.enabled %}
avinetworks_create_cloud:
  avinetworks.cloud_present:
    - name: {{ client.cloud.name }}
    - mtu: {{ client.cloud.mtu }}
    - dhcp_enabled: {{ client.cloud.dhcp_enabled }}
    - openstack:
        username: {{ client.cloud.openstack.username }}
        password: {{ client.cloud.openstack.password }}
        admin_tenant: {{ client.cloud.openstack.admin_tenant }}
        auth_url: {{ client.cloud.openstack.auth_url }}
        mgmt_network_name: {{ client.cloud.openstack.mgmt_network_name }}
        privilege: {{ client.cloud.openstack.privilege }}
        region: {{ client.cloud.openstack.region }}
        hypervisor: {{ client.cloud.openstack.hypervisor }}
        free_floatingips: {{ client.cloud.openstack.free_floatingips }}
        img_format: {{ client.cloud.openstack.img_format }}
        use_internal_endpoints: {{ client.cloud.openstack.use_internal_endpoints }}
        insecure: {{ client.cloud.openstack.insecure }}
        contrail_endpoint: {{ client.cloud.openstack.contrail_endpoint }}
        os_role: {{ client.cloud.openstack.os_role }}
        avi_role: {{ client.cloud.openstack.avi_role }}
{%- endif %}


{%- endif %}
