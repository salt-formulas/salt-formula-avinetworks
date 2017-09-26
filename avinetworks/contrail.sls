{%- if pillar.avinetworks is defined %}
{%- if pillar.avinetworks.get('module','') == 'contrail' %}

{%- set service_appliance = pillar.avinetworks.service_appliance %}

Avinetworks_create_contrail_service_appliance:
  contrail.service_appliance_set_present:
    - name: {{ service_appliance.name }}
    - driver: {{ service_appliance.driver }}
    - properties:
        address:  {{ service_appliance.address }}
        user: {{ service_appliance.user }}
        password: {{ service_appliance.password }}
        cloud: {{ service_appliance.cloud }}
    - ha_mode: {{ service_appliance.ha_mode }}

{%- endif %}
{%- endif %}
