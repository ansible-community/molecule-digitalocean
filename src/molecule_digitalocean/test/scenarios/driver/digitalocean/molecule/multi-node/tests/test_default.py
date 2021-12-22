"""Missing docstring."""
import os
import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_hostname(host):
    """Missing docstring."""
    assert re.search(r"instance-[12].*", host.check_output("hostname -s"))


def test_etc_molecule_directory(host):
    """Missing docstring."""
    f = host.file("/etc/molecule")

    assert f.is_directory
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o755


def test_etc_molecule_ansible_hostname_file(host):
    """Missing docstring."""
    filename = "/etc/molecule/{}".format(host.check_output("hostname -s"))
    f = host.file(filename)

    assert f.is_file
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o644
