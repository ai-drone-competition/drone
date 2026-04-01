"""
자르기 연산 함수들
단일 책임: 이미지를 특정 영역으로 자르기
"""
import numpy as np


def crop_frame(frame: np.ndarray, x: int, y: int, width: int, height: int) -> np.ndarray:
    """
    프레임 자르기
    
    Args:
        frame: 입력 프레임
        x: 시작 x 좌표
        y: 시작 y 좌표
        width: 자를 너비
        height: 자를 높이
        
    Returns:
        자른 프레임
    """
    return frame[y:y+height, x:x+width]
