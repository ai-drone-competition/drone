"""
영역 및 크기 계산 함수들
단일 책임: 바운딩 박스로부터 객체의 영역과 크기 정보를 계산
"""
from typing import Tuple


def calculate_area(bbox: Tuple[int, int, int, int]) -> int:
    """
    바운딩 박스로부터 영역 크기 계산
    
    Args:
        bbox: 바운딩 박스 (x, y, w, h)
        
    Returns:
        영역 크기 (픽셀 단위)
    """
    _, _, w, h = bbox
    return w * h


def calculate_dimensions(bbox: Tuple[int, int, int, int]) -> Tuple[int, int]:
    """
    바운딩 박스로부터 가로, 세로 길이 계산
    
    Args:
        bbox: 바운딩 박스 (x, y, w, h)
        
    Returns:
        (가로 길이, 세로 길이) 픽셀 단위
    """
    _, _, w, h = bbox
    return w, h
