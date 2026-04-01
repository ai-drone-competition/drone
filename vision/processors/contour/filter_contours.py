"""
컨투어 필터링 함수들
단일 책임: 컨투어들을 조건에 따라 필터링
"""
import cv2
from typing import List, Any


def filter_by_area(contours: List[Any], min_area: int) -> List[Any]:
    """
    면적 기준으로 컨투어 필터링
    
    Args:
        contours: 컨투어 리스트
        min_area: 최소 면적
        
    Returns:
        필터링된 컨투어 리스트
    """
    return [contour for contour in contours if cv2.contourArea(contour) >= min_area]
