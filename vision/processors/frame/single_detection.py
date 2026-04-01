"""
단일 객체 감지 처리 함수
단일 책임: 단일 객체 감지 결과를 프레임에 처리
"""
import numpy as np
from typing import Tuple, Optional
from ...visualizers import DetectionVisualizer
from .metrics_calculation import calculate_all_metrics


def process_single_detection(frame: np.ndarray, detected: bool, 
                           bbox: Optional[Tuple[int, int, int, int]], 
                           center: Optional[Tuple[int, int]], 
                           color: Optional[str] = None) -> np.ndarray:
    """
    단일 객체 감지 결과 처리
    
    Args:
        frame: 입력 프레임
        detected: 감지 여부
        bbox: 바운딩 박스
        center: 중심점
        color: 감지된 색상
        
    Returns:
        처리된 프레임
    """
    visualizer = DetectionVisualizer()
    
    if detected and bbox and center and color:
        # 색상 설정 가져오기
        from vision_color_config import COLOR_CONFIGS
        
        # 안전하게 색상 정보 가져오기
        color_config = COLOR_CONFIGS.get(color, {})
        display_name = color_config.get('display_name', color.upper())
        display_color = color_config.get('bgr_color', (0, 255, 0))  # 기본 초록색
        
        # 영역 크기 및 관련 정보 계산
        metrics = calculate_all_metrics(
            frame, bbox, center, (frame.shape[0], frame.shape[1])
        )
        
        # 색상별 감지 정보 시각화
        frame = visualizer.draw_colored_detection_info(
            frame, bbox, center, metrics, display_name, display_color, display_color
        )
    else:
        # 감지되지 않았어도 십자선은 표시
        frame = visualizer.draw_crosshair(frame)
    
    return frame
