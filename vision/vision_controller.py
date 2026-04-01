"""
비전 컨트롤러
단일 책임: 비전 시스템의 전체 조합 및 제어
"""
import numpy as np
from typing import Optional, List, Dict, Tuple
from .components import VisionConfig, VisionDetectionManager, VisionFrameProcessor
from .stream import VisionStreamManager


class VisionController:
    """비전 컨트롤러 - 단순 실행 인터페이스 제공"""
    
    def __init__(self, min_area: int = 500, debug_mode: bool = True, 
                 window_name: str = "Tello EDU Vision Detection",
                 target_colors: Optional[List[str]] = None,
                 separate_color_mode: bool = False,
                 color_ranges: Optional[Dict[str, Dict[str, np.ndarray]]] = None,
                 color_configs: Optional[Dict[str, Dict]] = None):
        """
        VisionController 초기화
        
        Args:
            min_area: 감지할 최소 객체 크기
            debug_mode: 디버깅 모드 활성화 여부
            window_name: OpenCV 창 이름
            target_colors: 감지할 색상 목록 ['environment', 'target'], 기본값: ['environment']
            separate_color_mode: 색상별 개별 감지 모드 (True: 개별 감지, False: 통합 감지)
            color_ranges: 색상 범위 설정 딕셔너리
            color_configs: 색상 설정 정보 딕셔너리 (시각화용)
        """
        # 설정 관리자
        self.config = VisionConfig(
            min_area=min_area,
            target_colors=target_colors,
            separate_color_mode=separate_color_mode,
            window_name=window_name,
            debug_mode=debug_mode,
            color_ranges=color_ranges,
            color_configs=color_configs
        )
        
        # 구성 요소들
        self.detection_manager = VisionDetectionManager(self.config)
        self.frame_processor = VisionFrameProcessor(self.config, self.detection_manager)
        
        # 스트림 관리자 - color_configs가 제공되면 사용, 아니면 기본값 사용
        from vision_color_config import COLOR_CONFIGS
        if color_configs:
            final_color_configs = {**COLOR_CONFIGS, **color_configs}  # 전달받은 설정이 기본값을 덮어씀
        else:
            final_color_configs = COLOR_CONFIGS
        
        self.stream_manager = VisionStreamManager(
            self.config.window_name, 
            self.config.debug_mode,
            final_color_configs
        )
    
    def execute(self, drone) -> bool:
        """
        드론 비전 스트림 실행 (단일 진입점)
        
        Args:
            drone: 연결된 드론 객체
            
        Returns:
            처리 성공 여부
        """
        # 프레임 처리 함수 생성
        process_frame = self.frame_processor.create_frame_processor()
        
        # 스트림 실행
        return self.stream_manager.execute(drone, process_frame)
