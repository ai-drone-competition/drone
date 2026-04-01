"""
위치 정보 계산 함수들
단일 책임: 객체의 위치 관련 정보를 계산
"""
import numpy as np
from typing import Tuple


def calculate_offset(center: Tuple[int, int], frame_shape: Tuple[int, int]) -> Tuple[int, int]:
    """
    화면 중앙과의 오프셋 계산
    
    Args:
        center: 객체 중심점 (x, y)
        frame_shape: 프레임 크기 (height, width)
        
    Returns:
        오프셋 (offset_x, offset_y)
    """
    center_x, center_y = center
    height, width = frame_shape
    screen_center_x, screen_center_y = width // 2, height // 2
    
    offset_x = center_x - screen_center_x
    offset_y = center_y - screen_center_y
    
    return offset_x, offset_y


def calculate_distance_from_center(center: Tuple[int, int], frame_shape: Tuple[int, int]) -> int:
    """
    화면 중앙으로부터의 거리 계산
    
    Args:
        center: 객체 중심점 (x, y)
        frame_shape: 프레임 크기 (height, width)
        
    Returns:
        거리 (픽셀 단위)
    """
    offset_x, offset_y = calculate_offset(center, frame_shape)
    distance = int(np.sqrt(offset_x**2 + offset_y**2))
    return distance
