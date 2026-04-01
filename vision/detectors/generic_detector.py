"""
범용 색상 객체 감지기
외부에서 전달받은 색상 설정을 사용하여 객체 감지
"""

import numpy as np
from typing import Optional, Tuple, List
from ..processors.color import (
    bgr_to_hsv, create_color_mask, apply_morphology, ColorRangeProvider
)
from ..processors.contour import (
    find_contours, filter_by_area, get_largest_contour,
    get_bounding_box, get_center_point
)


def detect_color_object(frame: np.ndarray, color_range_provider: ColorRangeProvider, 
                       color_type: str, min_area: int = 500) -> Tuple[bool, Optional[Tuple[int, int, int, int]], Optional[Tuple[int, int]]]:
    """
    프레임에서 지정된 색상 타입의 객체 감지
    
    Args:
        frame: 입력 프레임 (BGR)
        color_range_provider: 색상 범위 제공자
        color_type: 색상 타입 ('environment', 'target' 등)
        min_area: 감지할 최소 객체 크기
        
    Returns:
        (감지여부, 바운딩박스(x,y,w,h), 중심점(x,y))
    """
    # HSV 변환
    hsv = bgr_to_hsv(frame)
    
    # 색상 마스크 생성
    mask = create_color_mask(hsv, color_range_provider, color_type)
    if mask is None:
        return False, None, None
    
    # 노이즈 제거
    mask = apply_morphology(mask)
    
    # 컨투어 찾기
    contours = find_contours(mask)
    
    # 면적 기준으로 필터링
    valid_contours = filter_by_area(contours, min_area)
    
    if not valid_contours:
        return False, None, None
    
    # 가장 큰 컨투어 찾기
    largest_contour = get_largest_contour(valid_contours)
    
    if largest_contour is None:
        return False, None, None
    
    # 바운딩 박스와 중심점 계산
    bbox = get_bounding_box(largest_contour)
    center = get_center_point(largest_contour)
    
    return True, bbox, center


def detect_color_objects_all(frame: np.ndarray, color_range_provider: ColorRangeProvider,
                            color_type: str, min_area: int = 500) -> List[Tuple[Tuple[int, int, int, int], Tuple[int, int]]]:
    """
    프레임에서 지정된 색상 타입의 모든 객체 감지
    
    Args:
        frame: 입력 프레임 (BGR)
        color_range_provider: 색상 범위 제공자
        color_type: 색상 타입 ('environment', 'target' 등)
        min_area: 감지할 최소 객체 크기
        
    Returns:
        [(바운딩박스(x,y,w,h), 중심점(x,y))] 리스트
    """
    # HSV 변환
    hsv = bgr_to_hsv(frame)
    
    # 색상 마스크 생성
    mask = create_color_mask(hsv, color_range_provider, color_type)
    if mask is None:
        return []
    
    # 노이즈 제거
    mask = apply_morphology(mask)
    
    # 컨투어 찾기
    contours = find_contours(mask)
    
    # 면적 기준으로 필터링
    valid_contours = filter_by_area(contours, min_area)
    
    results = []
    for contour in valid_contours:
        bbox = get_bounding_box(contour)
        center = get_center_point(contour)
        results.append((bbox, center))
    
    return results
