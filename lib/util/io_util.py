import numpy as np
from typing import Literal
import pyntcloud


def load_point_cloud(path: str,
                     format: Literal['ply', 'npy'],
                     color: bool = False):
    if format == 'ply':
        cloud = pyntcloud.PyntCloud.from_file(path)
        pc_df = cloud.points[['x', 'y', 'z']]
        if color:
            rgb_df = cloud.points[['red', 'green', 'blue']]
            pc_df = pd.concat([pc_df, rgb_df], axis=1)
        pc = pc_df.to_numpy()
    elif format == 'npy':
        pc = np.load(path, allow_pickle=True)
        pc: np.ndarray
        assert len(pc.shape) == 2
        if color:
            assert pc.shape[-1] == 6
        else:
            assert pc.shape[-1] == 3
    return pc
