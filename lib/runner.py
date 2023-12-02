import torch
import importlib
from lib.util.runner_util import *
from lib.data.default import Data


# one class to rule them all!
class Runner:
    def __init__(self, 
                 data_class_path: str,
                 data_root: str,
                 ):
        DataClass = getattr(importlib.import_module(convert_module_path(data_class_path)), 'Data')
        self.data = DataClass(data_root)
    
    def run(self):
        pass
 