"""
텍스트 오버레이 함수
단일 책임: 프레임에 텍스트를 오버레이
"""
import cv2
import numpy as np
from typing import Tuple


def add_text_overlay(frame: np.ndarray, text: str, position: Tuple[int, int], 
                    color: Tuple[int, int, int] = (255, 255, 255), 
                    font_scale: float = 0.7, thickness: int = 2) -> np.ndarray:
    """
    프레임에 텍스트 오버레이 추가
    
    Args:
        frame: 입력 프레임
        text: 표시할 텍스트
        position: 텍스트 위치 (x, y)
        color: 텍스트 색상 (BGR)
        font_scale: 폰트 크기
        thickness: 두께
        
    Returns:
        텍스트가 추가된 프레임
    """
    cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, 
                font_scale, color, thickness)
    return frame
