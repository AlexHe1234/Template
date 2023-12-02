import numpy as np
from typing import Literal, List


class Data:
    def __init__(self, root_dir: str) -> None:
        raise NotImplementedError('Please don\'t call template data class')
    
    @property
    def frame_len(self) -> int:
        return 100  # frames
    
    @property
    def cam_len(self) -> int:
        return 60
    
    @property
    def bg_color(self) -> np.ndarray[float]:  # return a 3-dim vector within range of 0, 1, representing background color
        return np.zeros(3, dtype=np.float32)
    
    @property
    def cam(self) -> np.ndarray[float]:  # intrinsic and extrinsic (CAM, 3, 7) matrices, ordered by camera index
        return np.random.randn((self.cam_len, 3, 7))
    
    def get_point_cloud(self, frame_id: int) -> np.ndarray[float]:  # return pretrained pointcloud xyz & radius (N, 4) that can be obtained by using methods like 4k4d
        return np.random.randn(10000, 4)
    
    def get_img(self, frame_id, cam_id) -> np.ndarray[float]:
        return np.random.rand(960, 540, 3)  # H, W, 3 within range [0, 1] 
    
    def get_mask(self, frame_id, cam_id) -> np.ndarray[bool]:
        return (np.random.rand(960, 540) > 0.5)  # H, W [True, False]
