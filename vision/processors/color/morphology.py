"""
모폴로지 연산 함수
단일 책임: 마스크에 모폴로지 연산을 적용하여 노이즈 제거
"""
import cv2
import numpy as np


def apply_morphology(mask: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """
    마스크에 모폴로지 연산 적용 (노이즈 제거)
    
    Args:
        mask: 이진 마스크
        kernel_size: 커널 크기
        
    Returns:
        모폴로지 연산이 적용된 마스크
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    
    # Opening (침식 후 팽창) - 작은 노이즈 제거
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Closing (팽창 후 침식) - 작은 구멍 메우기
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    return mask
