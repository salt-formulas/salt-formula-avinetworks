avinetworks:
  server:
    enabled: true
    identity: cloud1
    image_location: http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img
    disk_format: qcow2
    public_network: INET1
    saltmaster_ip: 10.0.0.90