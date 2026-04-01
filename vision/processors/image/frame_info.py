"""
프레임 정보 함수들
단일 책임: 프레임의 정보를 추출
"""
import numpy as np
from typing import Tuple


def get_frame_info(frame: np.ndarray) -> Tuple[int, int, int]:
    """
    프레임 정보 반환
    
    Args:
        frame: 입력 프레임
        
    Returns:
        (높이, 너비, 채널수)
    """
    if len(frame.shape) == 3:
        height, width, channels = frame.shape
        return height, width, channels
    else:
        height, width = frame.shape
        return height, width, 1
