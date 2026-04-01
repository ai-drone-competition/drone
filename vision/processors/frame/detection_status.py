"""
감지 상태 표시 함수
단일 책임: 프레임에 감지 상태 정보를 표시
"""
import numpy as np
from .text_overlay import add_text_overlay


def add_detection_status(frame: np.ndarray, detected: bool, color: str = "") -> np.ndarray:
    """
    프레임에 감지 상태 추가
    
    Args:
        frame: 입력 프레임
        detected: 감지 여부
        color: 감지된 색상
        
    Returns:
        상태가 표시된 프레임
    """
    if detected:
        status_text = f"DETECTED: {color.upper()}" if color else "DETECTED"
        text_color = (0, 255, 0)  # 초록색
    else:
        status_text = "NO DETECTION"
        text_color = (0, 0, 255)  # 빨간색
    
    return add_text_overlay(frame, status_text, (10, 60), text_color)
