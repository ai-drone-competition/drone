"""
비전 감지 액션

색상 객체를 감지하고 결과를 반환하는 액션입니다.
"""

import numpy as np
from typing import Optional, Tuple, Dict, Union
from djitellopy import Tello
from constants import Colors
from actions.base_action import BaseAction
from sequences.vision_sequences import ColorObjectDetection
from debug.drone import DebugDroneWrapper


class VisionDetection(BaseAction):
    """비전 감지 액션"""
    
    def __init__(self, environment_color: Dict, target_color: Dict, min_area: int = 500) -> None:
        """
        비전 감지 액션 초기화
        
        Args:
            environment_color: 환경색 설정
            target_color: 목표색 설정
            min_area: 최소 감지 영역
        """
        super().__init__(environment_color=environment_color, target_color=target_color, min_area=min_area)
        self.environment_color = environment_color
        self.target_color = target_color
        self.min_area = min_area
        self.vision_system: Optional[ColorObjectDetection] = None
        
        # 감지 결과 저장
        self.target_center: Optional[Tuple[int, int]] = None
        self.estimated_distance: Optional[float] = None
        
    def execute(self, drone: Union[Tello, DebugDroneWrapper]) -> bool:
        """
        비전 감지 실행
        
        Args:
            drone: 드론 객체
            
        Returns:
            bool: 감지 성공 여부
        """
        try:
            print(f"{Colors.BLUE}비전 감지 시작 - 환경색: {self.environment_color['display_name']}, 목표색: {self.target_color['display_name']}{Colors.END}")
            
            # 스트림이 활성화되어 있는지 확인하고 활성화
            try:
                # 스트림 상태 확인을 위해 프레임 읽기 시도
                test_frame = drone.get_frame_read().frame
                if test_frame is None:
                    print(f"{Colors.YELLOW}비디오 스트림 활성화 중...{Colors.END}")
                    drone.streamon()
                    import time
                    time.sleep(2)  # 스트림 안정화 대기
            except Exception as stream_error:
                print(f"{Colors.YELLOW}비디오 스트림 활성화 중... ({stream_error}){Colors.END}")
                try:
                    drone.streamon()
                    import time
                    time.sleep(0.1)  # 스트림 안정화 대기 (2초 → 0.1초)
                except Exception as e:
                    print(f"{Colors.RED}✗ 스트림 활성화 실패: {e}{Colors.END}")
                    return False
            
            # 비전 시스템 초기화 (간소화)
            self.vision_system = ColorObjectDetection(
                min_area=self.min_area,
                environment_color=self.environment_color,
                target_color=self.target_color
            )
            
            # 비전 시스템 설정 (디버그 모드 비활성화로 속도 향상)
            print(f"{Colors.BLUE}빠른 비전 감지 모드{Colors.END}")
            
            # 색상 범위 설정
            color_ranges = {
                'environment': self.environment_color['hsv_ranges'],
                'target': self.target_color['hsv_ranges']
            }
            
            from vision.vision_controller import VisionController
            self.vision_system.vision_controller = VisionController(
                min_area=self.min_area,
                debug_mode=False,  # 디버그 모드 비활성화로 속도 향상
                window_name="Quick Detection",
                target_colors=['target'],  # 목표만 감지
                separate_color_mode=True,
                color_ranges=color_ranges
            )
            
            # 프레임 획득 및 감지
            frame = drone.get_frame_read().frame
            if frame is None:
                print(f"{Colors.RED}✗ 프레임 획득 실패{Colors.END}")
                return False
            
            # 감지 수행
            if self.vision_system.vision_controller and self.vision_system.vision_controller.detection_manager:
                detection_manager = self.vision_system.vision_controller.detection_manager
                detected, bbox, center, color, color_results = detection_manager.detect_by_mode(frame)
                
                # 목표 색상 감지 결과 확인
                if color_results and 'target' in color_results:
                    target_detected, target_bbox, target_center = color_results['target']
                    
                    if target_detected and target_bbox and target_center:
                        # 거리 추정
                        bbox_width = target_bbox[2]
                        self.estimated_distance = max(20.0, 500.0 - bbox_width * 2.0)
                        self.target_center = target_center
                        
                        print(f"{Colors.GREEN}✓ 목표 감지 성공 - 중심: {target_center}, 거리: {self.estimated_distance:.1f}cm{Colors.END}")
                        return True
            
            print(f"{Colors.YELLOW}목표 감지 실패{Colors.END}")
            return False
            
        except Exception as e:
            print(f"{Colors.RED}✗ 비전 감지 오류: {e}{Colors.END}")
            return False
        finally:
            # 리소스 정리
            if self.vision_system:
                self.vision_system._cleanup()
    
    def get_target_center(self) -> Optional[Tuple[int, int]]:
        """감지된 목표 중심점 반환"""
        return self.target_center
    
    def get_estimated_distance(self) -> Optional[float]:
        """추정된 거리 반환"""
        return self.estimated_distance
