"""
색상 객체 감지 시퀀스

DJI Tello EDU 드론을 사용하여 주변색과 목표색 객체를 감지하는 비전 시퀀스입니다.
기존 red_object_detection.py를 확장하여 다중 색상 감지를 지원합니다.
"""

import numpy as np
from typing import Optional, Union, List, Dict
from djitellopy import Tello
from constants import Colors
from vision import VisionController
from .base_vision_sequence import BaseVisionSequence
from debug.drone import DebugDroneWrapper


class ColorObjectDetection(BaseVisionSequence):
    """색상 객체 감지 시퀀스"""
    
    def __init__(self, min_area: int = 500, environment_color: Optional[Dict] = None, target_color: Optional[Dict] = None) -> None:
        """
        색상 객체 감지 시퀀스 초기화
        
        Args:
            min_area (int): 감지할 최소 객체 크기, 기본값: 500
            environment_color (Dict): 배경색 설정 (RED_COLOR, BLUE_COLOR 등)
            target_color (Dict): 목표색 설정 (WHITE_COLOR, BLACK_COLOR 등)
        """
        super().__init__(name="DJI Tello EDU 색상 객체 감지 시스템")
        
        # 기본값 검증
        if not environment_color or not target_color:
            raise ValueError("environment_color와 target_color는 반드시 지정해야 합니다.")
            
        self.min_area = min_area
        self.environment_color = environment_color
        self.target_color = target_color
        self.vision_controller: Optional[VisionController] = None
        
    def setup_vision(self) -> None:
        """비전 처리 설정"""
        print(f"{Colors.BLUE}비전 설정: 배경색={self.environment_color['display_name']}, 목표색={self.target_color['display_name']}, 최소 객체 크기={self.min_area}px{Colors.END}")
        
        # 색상 범위 매핑 생성
        color_ranges = {
            'environment': self.environment_color['hsv_ranges'],
            'target': self.target_color['hsv_ranges']
        }
        
        # 색상 설정 정보 매핑 생성 (시각화용)
        color_configs = {
            'environment': self.environment_color,
            'target': self.target_color
        }
        
        # VisionController 인스턴스 생성
        self.vision_controller = VisionController(
            min_area=self.min_area,
            debug_mode=True,  # 항상 True
            window_name="Tello EDU Vision Detection",  # 고정값
            target_colors=['environment', 'target'],
            separate_color_mode=True,  # 항상 True
            color_ranges=color_ranges,
            color_configs=color_configs  # 시각화 정보 추가
        )
        
        print(f"{Colors.GREEN}색상 객체 감지 컨트롤러 설정 완료{Colors.END}")
        
    def process_vision(self, drone: Union[Tello, DebugDroneWrapper]) -> bool:
        """
        실제 비전 처리 로직
        
        Args:
            drone: 연결된 드론 객체
            
        Returns:
            bool: 처리 성공 여부
        """
        if not self.vision_controller:
            print(f"{Colors.RED}✗ 비전 컨트롤러가 초기화되지 않았습니다{Colors.END}")
            return False
        
        # 비전 스트림 실행
        success = self.vision_controller.execute(drone)
        return success
    
    def _cleanup(self) -> None:
        """리소스 정리"""
        if self.vision_controller:
            # 스트림 정리는 VisionController에서 처리됨
            pass
