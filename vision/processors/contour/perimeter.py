"""
컨투어 둘레 계산 함수
단일 책임: 컨투어의 둘레를 계산
"""
import cv2
from typing import Any


def get_contour_perimeter(contour: Any) -> float:
    """
    컨투어의 둘레 계산
    
    Args:
        contour: 컨투어
        
    Returns:
        컨투어 둘레
    """
    return cv2.arcLength(contour, True)
