
===================
Avinetworks formula
===================

Sample pillars
==============

Salt formula to setup Avi Networks LBaaS

.. code-block:: yaml

    avinetworks:
      server:
        enabled: true
        identity: cloud1
        image_location: http://...
        disk_format: qcow2
        public_network: INET1
        saltmaster_ip: 10.0.0.90

    avinetworks:
      client:
        enabled: true

External links
==============

- https://kb.avinetworks.com/installing-avi-vantage-for-openstack-2/

Documentation and Bugs
======================

To learn how to install and update salt-formulas, consult the documentation
available online at:

    http://salt-formulas.readthedocs.io/

In the unfortunate event that bugs are discovered, they should be reported to
the appropriate issue tracker. Use Github issue tracker for specific salt
formula:

    https://github.com/salt-formulas/salt-formula-avinetworks/issues

For feature requests, bug reports or blueprints affecting entire ecosystem,
use Launchpad salt-formulas project:

    https://launchpad.net/salt-formulas

You can also join salt-formulas-users team and subscribe to mailing list:

    https://launchpad.net/~salt-formulas-users

Developers wishing to work on the salt-formulas projects should always base
their work on master branch and submit pull request against specific formula.

    https://github.com/salt-formulas/salt-formula-avinetworks

Any questions or feedback is always welcome so feel free to join our IRC
channel:

    #salt-formulas @ irc.freenode.net
