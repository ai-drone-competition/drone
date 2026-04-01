"""
메트릭 계산 함수
단일 책임: 감지된 객체의 모든 메트릭을 계산
"""
import numpy as np
from typing import Dict, Tuple
from ...calculators import (
    calculate_area, calculate_dimensions, calculate_hsv_color, 
    calculate_offset, calculate_distance_from_center
)


def calculate_all_metrics(frame: np.ndarray, bbox: Tuple[int, int, int, int], 
                         center: Tuple[int, int], 
                         frame_shape: Tuple[int, int]) -> Dict[str, int]:
    """
    모든 메트릭을 계산
    
    Args:
        frame: 입력 프레임
        bbox: 바운딩 박스 (x, y, w, h)
        center: 객체 중심점 (x, y)
        frame_shape: 프레임 크기 (height, width)
        
    Returns:
        계산된 모든 메트릭 딕셔너리
    """
    # 영역 및 크기 계산
    area = calculate_area(bbox)
    width, height = calculate_dimensions(bbox)
    
    # 색상 계산
    h, s, v = calculate_hsv_color(frame, center)
    
    # 위치 계산
    offset_x, offset_y = calculate_offset(center, frame_shape)
    distance = calculate_distance_from_center(center, frame_shape)
    
    return {
        'area': area,
        'width': width,
        'height': height,
        'hsv_h': h,
        'hsv_s': s,
        'hsv_v': v,
        'offset_x': offset_x,
        'offset_y': offset_y,
        'distance': distance
    }
