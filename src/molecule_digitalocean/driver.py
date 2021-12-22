#  Copyright (c) 2019 Red Hat, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
"""DigitalOcean Driver Module."""

import os
import requests

from molecule import logger, util
from molecule.api import Driver
from molecule.util import sysexit_with_message
from typing import Dict

log = logger.get_logger(__name__)


class DigitalOcean(Driver):
    """
    This class is responsible for managing `DigitalOcean`_ instances.
    `DigitalOcean`_ is **not** the default driver used in Molecule.

    Molecule leverages Ansible's `digital_ocean_module`_, by mapping variables
    from ``molecule.yml`` into ``create.yml`` and ``destroy.yml``.

    .. _`digital_ocean_module`: https://docs.ansible.com/ansible/latest/modules/digital_ocean_module.html#digital-ocean-module

    .. code-block:: yaml

        driver:
          name: digitalocean
        platforms:
          - name: instance

    .. code-block:: bash

        $ pip install 'molecule[digitalocean]'

    Change the options passed to the ssh client.

    .. code-block:: yaml

        driver:
          name: digitalocean
          ssh_connection_options:
            - '-o ControlPath=~/.ansible/cp/%r@%h-%p'

    .. important::

        Molecule does not merge lists, when overriding the developer must
        provide all options.

    Provide the files Molecule will preserve upon each subcommand execution.

    .. code-block:: yaml

        driver:
          name: digitalocean
          safe_files:
            - foo

    .. _`DigitalOcean`: https://www.digitalocean.com
    """  # noqa

    auth_env_vars = ["DO_API_TOKEN", "DO_API_KEY", "DO_OAUTH_TOKEN", "OAUTH_TOKEN"]

    def __init__(self, config=None):
        """Missing docstring."""
        super(DigitalOcean, self).__init__(config)
        self._name = "digitalocean"

    @property
    def name(self):
        """Missing docstring."""
        return self._name

    @name.setter
    def name(self, value):
        """Missing docstring."""
        self._name = value

    @property
    def login_cmd_template(self):
        """Missing docstring."""
        connection_options = " ".join(self.ssh_connection_options)

        return (
            "ssh {{address}} "
            "-l {{user}} "
            "-p {{port}} "
            "-i {{identity_file}} "
            "{}"
        ).format(connection_options)

    @property
    def default_safe_files(self):
        """Missing docstring."""
        return [self.instance_config]

    @property
    def default_ssh_connection_options(self):
        """Missing docstring."""
        return self._get_ssh_connection_options()

    def template_dir(self):
        """Return path to its own cookiecutterm templates.

        It is used by init command in order to figure out where to load the
        templates from.
        """
        return os.path.join(os.path.dirname(__file__), "cookiecutter")

    def login_options(self, instance_name):
        """Missing docstring."""
        d = {"instance": instance_name}

        return util.merge_dicts(d, self._get_instance_config(instance_name))

    def ansible_connection_options(self, instance_name):
        """Missing docstring."""
        try:
            d = self._get_instance_config(instance_name)

            return {
                "ansible_user": d["user"],
                "ansible_host": d["address"],
                "ansible_port": d["port"],
                "ansible_private_key_file": d["identity_file"],
                "connection": "ssh",
                "ansible_ssh_common_args": " ".join(self.ssh_connection_options),
            }
        except StopIteration:
            return {}
        except IOError:
            # Instance has yet to be provisioned , therefore the
            # instance_config is not on disk.
            return {}

    def _get_instance_config(self, instance_name):
        instance_config_dict = util.safe_load_file(self._config.driver.instance_config)

        return next(
            item for item in instance_config_dict if item["instance"] == instance_name
        )

    @staticmethod
    def _first_oauth_token():
        for auth_env_var in DigitalOcean.auth_env_vars:
            oauth_token = os.getenv(auth_env_var)
            if oauth_token:
                return auth_env_var, oauth_token
        return None, None

    def sanity_checks(self):
        """Missing docstring."""
        log.info("Sanity checks: '%s'", self._name)

        # Ensure that at least one of them is set:
        auth_env_var, oauth_token = self._first_oauth_token()
        if not oauth_token:
            sysexit_with_message(
                "Please ensure that one of the following environment variables "
                f"are set: {', '.join(DigitalOcean.auth_env_vars)}",
                code=1,
            )
        else:
            # Test authentication against DO:
            headers = {"Authorization": f"Bearer {oauth_token}"}
            r = requests.get("https://api.digitalocean.com/v2/account", headers=headers)
            if r.status_code != 200:
                sysexit_with_message(
                    "Failed to authentication to DigitalOcean, please ensure the "
                    "validity of your DO API token. The environment variable "
                    f"{auth_env_var} is currently defined.",
                    code=1,
                )

    @property
    def required_collections(self) -> Dict[str, str]:
        """Return collections dict containing names and versions required."""
        return {"community.digitalocean": "1.13.0"}
