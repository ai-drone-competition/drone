"""
다중 색상 객체 감지 함수들
단일 책임: 여러 색상을 통합하여 감지
"""
import numpy as np
from typing import Dict, List, Optional, Tuple
from .generic_detector import detect_color_object
from ..processors.color import ColorRangeProvider


def detect_largest_object(frame: np.ndarray, color_range_provider: ColorRangeProvider, 
                         colors: List[str], min_area: int = 500) -> Tuple[bool, Optional[Tuple[int, int, int, int]], Optional[Tuple[int, int]], Optional[str]]:
    """
    프레임에서 지정된 색상들 중 가장 큰 객체 감지
    
    Args:
        frame: 입력 프레임 (BGR)
        color_range_provider: 색상 범위 제공자
        colors: 감지할 색상 목록
        min_area: 감지할 최소 객체 크기
        
    Returns:
        (감지여부, 바운딩박스(x,y,w,h), 중심점(x,y), 감지된색상)
    """
    largest_area = 0
    largest_bbox = None
    largest_center = None
    detected_color = None
    
    for color in colors:
        detected, bbox, center = detect_color_object(frame, color_range_provider, color, min_area)
            
        if detected and bbox:
            # 면적 계산
            _, _, w, h = bbox
            area = w * h
            
            if area > largest_area:
                largest_area = area
                largest_bbox = bbox
                largest_center = center
                detected_color = color
    
    if largest_bbox is not None:
        return True, largest_bbox, largest_center, detected_color
    else:
        return False, None, None, None


def detect_all_colors_separately(frame: np.ndarray, color_range_provider: ColorRangeProvider,
                               colors: List[str], min_area: int = 500) -> Dict[str, Tuple[bool, Optional[Tuple[int, int, int, int]], Optional[Tuple[int, int]]]]:
    """
    프레임에서 모든 색상을 개별적으로 감지
    
    Args:
        frame: 입력 프레임 (BGR)
        color_range_provider: 색상 범위 제공자
        colors: 감지할 색상 목록
        min_area: 감지할 최소 객체 크기
        
    Returns:
        색상별 감지 결과 딕셔너리 {color: (감지여부, 바운딩박스, 중심점)}
    """
    results = {}
    
    for color in colors:
        results[color] = detect_color_object(frame, color_range_provider, color, min_area)
    
    return results


def detect_specific_color(frame: np.ndarray, color_range_provider: ColorRangeProvider,
                         color: str, min_area: int = 500) -> Tuple[bool, Optional[Tuple[int, int, int, int]], Optional[Tuple[int, int]]]:
    """
    특정 색상만 감지
    
    Args:
        frame: 입력 프레임 (BGR)
        color_range_provider: 색상 범위 제공자
        color: 감지할 색상
        min_area: 감지할 최소 객체 크기
        
    Returns:
        (감지여부, 바운딩박스(x,y,w,h), 중심점(x,y))
    """
    return detect_color_object(frame, color_range_provider, color, min_area)
