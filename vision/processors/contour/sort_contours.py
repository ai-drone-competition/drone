"""
컨투어 정렬 함수
단일 책임: 컨투어들을 면적 순으로 정렬
"""
import cv2
from typing import List, Any


def sort_contours_by_area(contours: List[Any], descending: bool = True) -> List[Any]:
    """
    컨투어를 면적 순으로 정렬
    
    Args:
        contours: 컨투어 리스트
        descending: True면 큰 것부터, False면 작은 것부터
        
    Returns:
        정렬된 컨투어 리스트
    """
    return sorted(contours, key=cv2.contourArea, reverse=descending)
