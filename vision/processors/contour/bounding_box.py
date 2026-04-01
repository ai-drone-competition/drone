"""
바운딩 박스 계산 함수
단일 책임: 컨투어의 바운딩 박스를 계산
"""
import cv2
from typing import Tuple, Any


def get_bounding_box(contour: Any) -> Tuple[int, int, int, int]:
    """
    컨투어의 바운딩 박스 계산
    
    Args:
        contour: 컨투어
        
    Returns:
        바운딩 박스 (x, y, w, h)
    """
    x, y, w, h = cv2.boundingRect(contour)
    return (int(x), int(y), int(w), int(h))
