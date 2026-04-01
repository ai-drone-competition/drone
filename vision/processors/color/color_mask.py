"""
범용 색상 마스크 생성기
외부에서 전달받은 HSV 범위를 사용하여 마스크 생성
"""
import cv2
import numpy as np
from typing import Dict, Optional
from .color_range_provider import ColorRangeProvider


def create_color_mask(hsv_frame: np.ndarray, color_range_provider: ColorRangeProvider, color_type: str) -> Optional[np.ndarray]:
    """
    지정된 색상 타입에 대한 마스크 생성
    
    Args:
        hsv_frame: HSV 색공간의 프레임
        color_range_provider: 색상 범위 제공자
        color_type: 색상 타입 ('environment', 'target' 등)
        
    Returns:
        생성된 마스크 또는 None
    """
    color_ranges = color_range_provider.get_color_range(color_type)
    if not color_ranges:
        return None
    
    # 단일 범위인 경우
    if 'lower_range' in color_ranges and 'upper_range' in color_ranges:
        return cv2.inRange(hsv_frame, color_ranges['lower_range'], color_ranges['upper_range'])
    
    # 다중 범위인 경우 (예: 빨간색)
    masks = []
    range_index = 1
    
    while f'lower_range{range_index}' in color_ranges and f'upper_range{range_index}' in color_ranges:
        lower_key = f'lower_range{range_index}'
        upper_key = f'upper_range{range_index}'
        
        mask = cv2.inRange(hsv_frame, color_ranges[lower_key], color_ranges[upper_key])
        masks.append(mask)
        range_index += 1
    
    # 모든 마스크를 결합
    if masks:
        combined_mask = masks[0]
        for mask in masks[1:]:
            combined_mask = cv2.bitwise_or(combined_mask, mask)
        return combined_mask
    
    return None
