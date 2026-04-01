"""
컨투어 찾기 함수
단일 책임: 이진 마스크에서 컨투어를 찾기
"""
import cv2
import numpy as np
from typing import List, Any


def find_contours(mask: np.ndarray) -> List[Any]:
    """
    마스크에서 컨투어 찾기
    
    Args:
        mask: 이진 마스크
        
    Returns:
        컨투어 리스트
    """
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return list(contours)
