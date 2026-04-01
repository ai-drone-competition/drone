"""
블러 필터 함수들
단일 책임: 이미지에 블러 효과를 적용
"""
import cv2
import numpy as np


def apply_gaussian_blur(frame: np.ndarray, kernel_size: int = 5, sigma: float = 0) -> np.ndarray:
    """
    가우시안 블러 적용
    
    Args:
        frame: 입력 프레임
        kernel_size: 커널 크기 (홀수여야 함)
        sigma: 시그마 값 (0이면 자동 계산)
        
    Returns:
        블러 처리된 프레임
    """
    if kernel_size % 2 == 0:
        kernel_size += 1  # 짝수면 홀수로 변경
    
    return cv2.GaussianBlur(frame, (kernel_size, kernel_size), sigma)


def apply_median_filter(frame: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """
    미디안 필터 적용 (노이즈 제거)
    
    Args:
        frame: 입력 프레임
        kernel_size: 커널 크기 (홀수여야 함)
        
    Returns:
        필터 처리된 프레임
    """
    if kernel_size % 2 == 0:
        kernel_size += 1  # 짝수면 홀수로 변경
    
    return cv2.medianBlur(frame, kernel_size)
