"""
비전 감지 관리자
단일 책임: 다양한 감지 메서드들을 관리하고 실행
"""
import numpy as np
from typing import Dict, Tuple, Optional, List
from ..detectors import detect_largest_object, detect_all_colors_separately, detect_specific_color
from .config import VisionConfig


class VisionDetectionManager:
    """비전 감지 로직 관리 클래스"""
    
    def __init__(self, config: VisionConfig):
        """
        VisionDetectionManager 초기화
        
        Args:
            config: 비전 설정 객체
        """
        self.config = config
    
    def detect_largest_object(self, frame: np.ndarray) -> Tuple[bool, Optional[Tuple[int, int, int, int]], Optional[Tuple[int, int]], Optional[str]]:
        """
        가장 큰 객체 감지
        
        Args:
            frame: 입력 프레임
            
        Returns:
            (감지여부, 바운딩박스, 중심점, 색상)
        """
        return detect_largest_object(frame, self.config.color_range_provider, self.config.target_colors, self.config.min_area)
    
    def detect_all_separately(self, frame: np.ndarray) -> Dict[str, Tuple[bool, Optional[Tuple[int, int, int, int]], Optional[Tuple[int, int]]]]:
        """
        모든 색상 개별 감지
        
        Args:
            frame: 입력 프레임
            
        Returns:
            색상별 감지 결과
        """
        return detect_all_colors_separately(frame, self.config.color_range_provider, self.config.target_colors, self.config.min_area)
    
    def detect_specific_color(self, frame: np.ndarray, color: str) -> Tuple[bool, Optional[Tuple[int, int, int, int]], Optional[Tuple[int, int]]]:
        """
        특정 색상 감지
        
        Args:
            frame: 입력 프레임
            color: 감지할 색상
            
        Returns:
            (감지여부, 바운딩박스, 중심점)
        """
        if not self.config.validate_color(color):
            return False, None, None
        
        return detect_specific_color(frame, self.config.color_range_provider, color, self.config.min_area)
    
    def detect_by_mode(self, frame: np.ndarray) -> Tuple[bool, Optional[Tuple[int, int, int, int]], Optional[Tuple[int, int]], Optional[str], Optional[Dict]]:
        """
        설정된 모드에 따라 감지 수행
        
        Args:
            frame: 입력 프레임
            
        Returns:
            단일 모드: (감지여부, 바운딩박스, 중심점, 색상, None)
            다중 모드: (True, None, None, None, 색상별_결과)
        """
        if self.config.is_multi_color_mode():
            # 다중 색상 개별 감지 모드
            color_results = self.detect_all_separately(frame)
            return True, None, None, None, color_results
        else:
            # 단일 객체 감지 모드
            detected, bbox, center, color = self.detect_largest_object(frame)
            return detected, bbox, center, color, None
