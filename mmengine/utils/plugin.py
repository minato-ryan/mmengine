# Copyright (c) OpenMMLab. All rights reserved.
import importlib
import os

import importlib_metadata

from mmengine.logging import print_log
from mmengine.utils import package_utils

MODULE2PACKAGE = {}

for key, value in package_utils.OFFICAL_MODULE2PACKAGE.items():
    try:
        m = importlib.import_module(key)
        config_root = os.path.join(m.__file__, '.mim')
        if os.path.exists(config_root):
            MODULE2PACKAGE[key] = value
        else:
            print_log(f'could not find .mim folder in {key}')
    except ModuleNotFoundError:
        print_log(f'can not found package {key}.')

_config_root_eps = importlib_metadata.entry_points(group='mim.module')

for row in _config_root_eps:
    try:
        key = row.name
        module_name = row.value
        m = row.load()

        config_root = os.path.join(m.__file__, '.mim')
        if os.path.exists(config_root):
            MODULE2PACKAGE[key] = module_name
        else:
            print_log(f'could not find .mim folder in {key}')
    except ModuleNotFoundError:
        print_log(
            f"module {key} did not be installed. try `pip install {key.split('.')[0]}`"
        )
