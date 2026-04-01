"""
비전 프레임 처리 관리자
단일 책임: 프레임 처리 로직 관리
"""
import numpy as np
from typing import Callable
from ..processors.frame import process_single_detection, process_multi_color_detection
from .config import VisionConfig
from .detection_manager import VisionDetectionManager


class VisionFrameProcessor:
    """비전 프레임 처리 로직 관리 클래스"""
    
    def __init__(self, config: VisionConfig, detection_manager: VisionDetectionManager):
        """
        VisionFrameProcessor 초기화
        
        Args:
            config: 비전 설정 객체
            detection_manager: 감지 관리자 객체
        """
        self.config = config
        self.detection_manager = detection_manager
    
    def create_frame_processor(self) -> Callable[[np.ndarray], np.ndarray]:
        """
        설정에 따른 프레임 처리 함수 생성
        
        Returns:
            프레임 처리 함수
        """
        def process_frame(frame: np.ndarray) -> np.ndarray:
            detected, bbox, center, color, color_results = self.detection_manager.detect_by_mode(frame)
            
            if self.config.is_multi_color_mode() and color_results is not None:
                # 다중 색상 개별 감지 모드 - 색상 설정 정보 전달
                return process_multi_color_detection(frame, color_results, self.config.color_configs)
            else:
                # 단일 객체 감지 모드
                return process_single_detection(frame, detected, bbox, center, color)
        
        return process_frame
    
    def process_single_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        단일 프레임 처리 (테스트용)
        
        Args:
            frame: 입력 프레임
            
        Returns:
            처리된 프레임
        """
        processor = self.create_frame_processor()
        return processor(frame)
