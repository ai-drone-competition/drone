"""
색상 정보 계산 함수들
단일 책임: 객체의 색상 정보를 계산
"""
import cv2
import numpy as np
from typing import Tuple


def calculate_hsv_color(frame: np.ndarray, center: Tuple[int, int]) -> Tuple[int, int, int]:
    """
    중심점에서의 HSV 색상값 계산
    
    Args:
        frame: 입력 프레임
        center: 객체 중심점 (x, y)
        
    Returns:
        HSV 색상값 (H, S, V)
    """
    center_x, center_y = center
    
    # 프레임을 HSV로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 중심점에서의 HSV 값 추출
    h, s, v = hsv[center_y, center_x]
    
    return int(h), int(s), int(v)
