from yacs.config import CfgNode as CN
import argparse
import yaml
import re
from typing import Dict


program = ''
description = ''


def convert_module_path(path: str) -> str:
    if path[-3:] == '.py':
        path = path[:-3]
    return path.replace('/', '.')


def add_list_dict(cfg: CN, x: Dict):
    if not isinstance(x, Dict):
        return
    for k in x.keys():
        if isinstance(x[k], Dict):
            cfg[k] = CN()
            add_list_dict(cfg[k], x[k])
        else:
            cfg[k] = x[k]
            
            
# loader supports float rep. like 1e10
loader = yaml.SafeLoader
loader.add_implicit_resolver(
    u'tag:yaml.org,2002:float',
    re.compile(u'''^(?:
     [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
    |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
    |\\.[0-9_]+(?:[eE][-+][0-9]+)?
    |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
    |[-+]?\\.(?:inf|Inf|INF)
    |\\.(?:nan|NaN|NAN))$''', re.X),
    list(u'-+0123456789.'))
            

def cfg_from_file(path_to_cfg):
    cfg = CN()
    with open(path_to_cfg, 'r') as f:
        yaml_dict = yaml.load(f, Loader=loader)
    add_list_dict(cfg, yaml_dict)
    return cfg


# FIXME: "None" would produce wrong result
def merge_base_config(cfg: CN, exp_cfg: CN) -> CN:
    base_names = list(cfg.keys()) + ['exp_name']
    for k in exp_cfg:
        if exp_cfg[k] is None:
            continue
        if k not in base_names:
            raise KeyError(f'Invalid key {k} in exp config')
        if isinstance(exp_cfg[k], CN):
            cfg[k] = merge_base_config(cfg[k], exp_cfg[k])
        else:
            cfg[k] = exp_cfg[k]
    return cfg


# gather all base configs
cfg = CN()
cfg = cfg_from_file('lib/config/default.yaml')

parser = argparse.ArgumentParser(prog=program, description=description)
parser.add_argument('--dist', type=bool, default=False, help=argparse.SUPPRESS)
parser.add_argument('--test', type=bool, default=False, help=argparse.SUPPRESS)
parser.add_argument('exp_cfg_path', type=str, help='exp config .yaml file path')
args = parser.parse_args()

cfg.test = args.test
cfg.dist = args.dist

exp_cfg = cfg_from_file(args.exp_cfg_path)
cfg = merge_base_config(cfg, exp_cfg)
