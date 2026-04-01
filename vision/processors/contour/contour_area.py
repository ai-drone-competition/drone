"""
컨투어 면적 계산 함수
단일 책임: 컨투어의 면적을 계산
"""
import cv2
from typing import Any


def get_contour_area(contour: Any) -> float:
    """
    컨투어의 면적 계산
    
    Args:
        contour: 컨투어
        
    Returns:
        컨투어 면적
    """
    return cv2.contourArea(contour)
