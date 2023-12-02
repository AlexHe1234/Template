import torch
from torch import nn


def to_cuda_float(*args):
    for i in range(len(args)):
        if isinstance(args[i], torch.Tensor):
            args[i] = args[i].float().cuda()
    return args


def convert_module_path(path: str) -> str:
    if path[-3:] == '.py':
        path = path[:-3]
    return path.replace('/', '.')


def create_buffer(x: torch.Tensor) -> nn.Parameter:
    return nn.Parameter(x, requires_grad=False)
