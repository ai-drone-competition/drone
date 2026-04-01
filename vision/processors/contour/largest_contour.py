"""
가장 큰 컨투어 찾기 함수
단일 책임: 컨투어 리스트에서 가장 큰 컨투어를 찾기
"""
import cv2
from typing import List, Optional, Any


def get_largest_contour(contours: List[Any]) -> Optional[Any]:
    """
    가장 큰 컨투어 찾기
    
    Args:
        contours: 컨투어 리스트
        
    Returns:
        가장 큰 컨투어 또는 None
    """
    if not contours:
        return None
    return max(contours, key=cv2.contourArea)
