"""
크기 조정 함수들
단일 책임: 이미지의 크기를 조정
"""
import cv2
import numpy as np


def resize_frame(frame: np.ndarray, width: int, height: int) -> np.ndarray:
    """
    프레임 크기 조정
    
    Args:
        frame: 입력 프레임
        width: 새로운 너비
        height: 새로운 높이
        
    Returns:
        크기 조정된 프레임
    """
    return cv2.resize(frame, (width, height))


def resize_frame_by_scale(frame: np.ndarray, scale: float) -> np.ndarray:
    """
    비율로 프레임 크기 조정
    
    Args:
        frame: 입력 프레임
        scale: 크기 조정 비율
        
    Returns:
        크기 조정된 프레임
    """
    height, width = frame.shape[:2]
    new_width = int(width * scale)
    new_height = int(height * scale)
    return cv2.resize(frame, (new_width, new_height))
