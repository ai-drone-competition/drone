"""
중심점 계산 함수
단일 책임: 컨투어의 중심점을 계산
"""
import cv2
from typing import Tuple, Any
from .bounding_box import get_bounding_box


def get_center_point(contour: Any) -> Tuple[int, int]:
    """
    컨투어의 중심점 계산
    
    Args:
        contour: 컨투어
        
    Returns:
        중심점 (x, y)
    """
    M = cv2.moments(contour)
    if M["m00"] == 0:
        # 면적이 0인 경우 바운딩 박스의 중심점 사용
        x, y, w, h = get_bounding_box(contour)
        return (x + w // 2, y + h // 2)
    
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    return (cx, cy)
