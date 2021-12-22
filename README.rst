****************************
Molecule DigitalOcean Plugin
****************************

.. image:: https://badge.fury.io/py/molecule-digitalocean.svg
   :target: https://badge.fury.io/py/molecule-digitalocean
   :alt: PyPI Package

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/python/black
   :alt: Python Black Code Style

.. image:: https://img.shields.io/badge/Code%20of%20Conduct-Ansible-silver.svg
   :target: https://docs.ansible.com/ansible/latest/community/code_of_conduct.html
   :alt: Ansible Code of Conduct

.. image:: https://img.shields.io/badge/Mailing%20lists-Ansible-orange.svg
   :target: https://docs.ansible.com/ansible/latest/community/communication.html#mailing-list-information
   :alt: Ansible mailing lists

.. image:: https://img.shields.io/badge/license-MIT-brightgreen.svg
   :target: LICENSE
   :alt: Repository License

Molecule digitalocean is designed to allow use of digitalocean Cloud for
provisioning test resources.

Documentation
=============

Read the documentation and more at https://molecule.readthedocs.io/.

Sample ``molecule.yml``:::

  ---
  dependency:
    name: galaxy
  driver:
    name: digitalocean
  platforms:
    - name: instance
      region: fra1
      size: s-1vcpu-2gb
      image: ubuntu-20-04-x64
  provisioner:
    name: ansible
  verifier:
    name: ansible

Please consult https://slugs.do-api.dev/ for sizes, images, regions, and more.

.. _get-involved:

Get Involved
============

* Join us in the ``#ansible-molecule`` channel on `Libera.Chat`_.
* Join the discussion in `molecule-users Forum`_.
* Join the community working group by checking the `wiki`_.
* Want to know about releases, subscribe to `ansible-announce list`_.
* For the full list of Ansible email Lists, IRC channels see the
  `communication page`_.

.. _`Libera.Chat`: https://libera.chat
.. _`molecule-users Forum`: https://groups.google.com/forum/#!forum/molecule-users
.. _`wiki`: https://github.com/ansible/community/wiki/Molecule
.. _`ansible-announce list`: https://groups.google.com/group/ansible-announce
.. _`communication page`: https://docs.ansible.com/ansible/latest/community/communication.html

.. _authors:

Authors
=======

Molecule DigitalOcean Plugin was created by Sorin Sbarnea based on code from
Molecule.

.. _license:

License
=======

The `MIT`_ License.

.. _`MIT`: https://github.com/ansible/molecule/blob/master/LICENSE

The logo is licensed under the `Creative Commons NoDerivatives 4.0 License`_.

If you have some other use in mind, contact us.

.. _`Creative Commons NoDerivatives 4.0 License`: https://creativecommons.org/licenses/by-nd/4.0/
