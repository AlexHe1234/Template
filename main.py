import lib
from lib.util.config_util import cfg
from lib.util.build_util import build_module


if __name__ == '__main__':
    runner = build_module(cfg)
    runner.run()
