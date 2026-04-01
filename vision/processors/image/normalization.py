"""
정규화 함수들
단일 책임: 이미지를 정규화
"""
import cv2
import numpy as np


def normalize_frame(frame: np.ndarray) -> np.ndarray:
    """
    프레임 정규화 (0-255 범위로)
    
    Args:
        frame: 입력 프레임
        
    Returns:
        정규화된 프레임
    """
    normalized = np.zeros_like(frame)
    return cv2.normalize(frame, normalized, 0, 255, cv2.NORM_MINMAX)
