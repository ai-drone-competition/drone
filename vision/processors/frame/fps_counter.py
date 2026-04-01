"""
FPS 카운터 함수
단일 책임: 프레임에 FPS 정보를 표시
"""
import numpy as np
from .text_overlay import add_text_overlay


def add_fps_counter(frame: np.ndarray, fps: float) -> np.ndarray:
    """
    프레임에 FPS 카운터 추가
    
    Args:
        frame: 입력 프레임
        fps: FPS 값
        
    Returns:
        FPS가 표시된 프레임
    """
    fps_text = f"FPS: {fps:.1f}"
    return add_text_overlay(frame, fps_text, (10, 30), (0, 255, 0))
