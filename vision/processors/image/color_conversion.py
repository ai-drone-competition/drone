"""
색공간 변환 함수들
단일 책임: 이미지의 색공간을 변환
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


def hsv_to_bgr(frame: np.ndarray) -> np.ndarray:
    """
    HSV 프레임을 BGR로 변환
    
    Args:
        frame: HSV 색공간 프레임
        
    Returns:
        BGR 색공간 프레임
    """
    return cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)


def bgr_to_gray(frame: np.ndarray) -> np.ndarray:
    """
    BGR 프레임을 그레이스케일로 변환
    
    Args:
        frame: BGR 색공간 프레임
        
    Returns:
        그레이스케일 프레임
    """
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
