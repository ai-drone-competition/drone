"""
다중 색상 감지 처리 함수
단일 책임: 다중 색상 감지 결과를 프레임에 처리
"""
import numpy as np
from typing import Dict, Tuple, Optional
from ...visualizers import DetectionVisualizer
from .metrics_calculation import calculate_all_metrics


def process_multi_color_detection(frame: np.ndarray, 
                                color_results: Dict[str, Tuple[bool, Optional[Tuple[int, int, int, int]], Optional[Tuple[int, int]]]],
                                color_configs: Optional[Dict[str, Dict]] = None) -> np.ndarray:
    """
    다중 색상 감지 결과 처리
    
    Args:
        frame: 입력 프레임
        color_results: 색상별 감지 결과
        color_configs: 색상 설정 정보 (선택사항)
        
    Returns:
        처리된 프레임
    """
    visualizer = DetectionVisualizer()
    
    # 색상 설정 가져오기 (매개변수가 있으면 우선 사용, 없으면 기본값 사용)
    if color_configs:
        current_color_configs = color_configs
    else:
        from vision_color_config import COLOR_CONFIGS
        current_color_configs = COLOR_CONFIGS
    
    # 십자선 먼저 그리기
    frame = visualizer.draw_crosshair(frame)
    
    # 각 색상별로 감지 정보 시각화
    for color, (detected, bbox, center) in color_results.items():
        if detected and bbox and center:
            # 안전하게 색상 정보 가져오기
            color_config = current_color_configs.get(color, {})
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
    
    return frame
