# Copyright (c) OpenMMLab. All rights reserved.
import importlib
import logging
import os

import importlib_metadata

from mmengine.logging import print_log
from mmengine.utils import package_utils

MODULE2PACKAGE = {}

for key, value in package_utils.OFFICAL_MODULE2PACKAGE.items():
    m = importlib.util.find_spec(key)
    if m is None:
        print_log(f'can not found package {key}.')
        continue

    config_root = os.path.join(
        os.path.dirname(m.origin), '.mim', level=logging.DEBUG)
    if os.path.exists(config_root):
        MODULE2PACKAGE[key] = value
    else:
        print_log(f'could not find .mim folder in {key}', level=logging.INFO)

_config_root_eps = importlib_metadata.entry_points(group='mim.module')

for row in _config_root_eps:
    key = row.name

    try:
        module_name = row.value
        m = importlib.util.find_spec(key)
        if m is None:
            print_log(f'can not found package {key}.')
            continue

        config_root = os.path.join(os.path.dirname(m.origin), '.mim')
        if os.path.exists(config_root):
            MODULE2PACKAGE[key] = module_name
        else:
            print_log(
                f'could not find .mim folder in {key}', level=logging.ERROR)
    except ModuleNotFoundError:
        print_log(
            f'module {key} did not be installed. '
            f"try `pip install {key.split('.')[0]}`",
            level=logging.ERROR)
