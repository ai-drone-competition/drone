"""
HSV 색공간 변환 함수
단일 책임: BGR과 HSV 간의 색공간 변환
"""
import cv2
import numpy as np


def bgr_to_hsv(frame: np.ndarray) -> np.ndarray:
    """
    BGR 프레임을 HSV로 변환
    
    Args:
        frame: BGR 색공간 프레임
        
    Returns:
        HSV 색공간 프레임
    """
    return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
