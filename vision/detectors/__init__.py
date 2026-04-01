"""
decorators export
"""

from .generic_detector import detect_color_object, detect_color_objects_all
from .multi_detector import (
    detect_largest_object, detect_all_colors_separately, detect_specific_color
)

__all__ = [
    # 범용 색상 감지 함수들
    'detect_color_object',
    'detect_color_objects_all',
    
    # 다중 색상 감지 함수들
    'detect_largest_object',
    'detect_all_colors_separately',
    'detect_specific_color',
]
