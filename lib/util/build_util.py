from yacs.config import CfgNode as CN
from typing import Any
import importlib
import inspect


def convert_module_path(path: str) -> str:
    if path[-3:] == '.py':
        path = path[:-3]
    return path.replace('/', '.')


def build_module(config: CN, **kwargs) -> Any:
    # display.update_status(f'Building {config.name}')
    
    module = getattr(importlib.import_module(convert_module_path(config.path)), config.name)
    arg_list = inspect.signature(module).parameters
    
    args = {}
    for k in config.keys():
        if k in arg_list:
            args[k] = config[k]
            
    for k in kwargs.keys():
        if k in arg_list:
            args[k] = kwargs[k]

    return module(**args)
