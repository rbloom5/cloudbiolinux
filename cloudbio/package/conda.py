"""Install packages via the Conda package manager: http://conda.pydata.org/
"""
import yaml

from cloudbio.custom import shared
from cloudbio.flavor.config import get_config_file
from cloudbio.package.shared import _yaml_to_packages

def install_packages(env, to_install=None, packages=None):
    if shared._is_anaconda(env):
        conda_bin = shared._conda_cmd(env)
        config_file = get_config_file(env, "packages-conda.yaml")
        if to_install:
            (packages, _) = _yaml_to_packages(config_file.base, to_install, config_file.dist)
        with open(config_file.base) as in_handle:
            channels = " ".join(["-c %s" % x for x in yaml.safe_load(in_handle).get("channels", [])])
        if len(packages) > 0:
            for pkg in packages:
                env.safe_run("{conda_bin} install -y {channels} {pkg}".format(**locals()))