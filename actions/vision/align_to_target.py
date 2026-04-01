"""
목표물 정렬 및 이동 액션

목표물이 화면 중심에 오도록 드론을 회전시키고,
거리를 계산해서 목표까지 이동하는 통합 액션입니다.
"""

from typing import Optional, Tuple, Dict, Union
from djitellopy import Tello
from constants import Colors
from actions.base_action import BaseAction
from actions.movements.RotateClockWise import RotateClockwise
from actions.movements.RotateCounterClockWise import RotateCounterclockwise
from actions.movements.MoveForward import MoveForward
from actions.vision.vision_detection import VisionDetection
from debug.drone import DebugDroneWrapper
import time


class AlignToTarget(BaseAction):
    """목표물 정렬 및 이동 액션"""
    
    def __init__(self, environment_color: Dict, target_color: Dict, 
                 center_tolerance: int = 50, max_attempts: int = 10,
                 rotation_step: int = 30, min_move_distance: int = 20,
                 max_move_distance: int = 500) -> None:
        """
        목표물 정렬 및 이동 액션 초기화
        
        Args:
            environment_color: 환경색 설정
            target_color: 목표색 설정  
            center_tolerance: 중심 허용 오차 (픽셀)
            max_attempts: 최대 회전 시도 횟수
            rotation_step: 회전 각도 단위 (도)
            min_move_distance: 최소 이동 거리 (cm)
            max_move_distance: 최대 이동 거리 (cm)
        """
        super().__init__(environment_color=environment_color, target_color=target_color, 
                        center_tolerance=center_tolerance, max_attempts=max_attempts,
                        rotation_step=rotation_step, min_move_distance=min_move_distance,
                        max_move_distance=max_move_distance)
        self.environment_color = environment_color
        self.target_color = target_color
        self.center_tolerance = center_tolerance
        self.max_attempts = max_attempts
        self.rotation_step = rotation_step
        self.min_move_distance = min_move_distance
        self.max_move_distance = max_move_distance
        
    def execute(self, drone: Union[Tello, DebugDroneWrapper]) -> bool:
        """
        목표물 정렬 및 이동 실행
        
        Args:
            drone: 드론 객체
            
        Returns:
            bool: 실행 성공 여부
        """
        try:
            print(f"{Colors.BLUE}목표물 정렬 및 이동 시작{Colors.END}")
            
            # 1단계: 목표물 감지 시도
            estimated_distance = self._align_to_target(drone)
            # 감지 실패 시에도 기본 거리로 설정
            if estimated_distance is None:
                print(f"{Colors.CYAN}감지 실패로 기본 거리 100cm로 전진합니다{Colors.END}")
                estimated_distance = max(100.0, 20.0)  # 최소 20cm 보장
            
            # 2단계: 목표까지 이동 (항상 실행)
            return self._move_to_target(drone, estimated_distance)
            
        except Exception as e:
            print(f"{Colors.RED}✗ 목표물 정렬 및 이동 오류: {e}{Colors.END}")
            # 오류 발생 시에도 기본 거리로 전진 시도
            print(f"{Colors.CYAN}오류 발생으로 기본 거리 80cm로 전진을 시도합니다{Colors.END}")
            return self._move_to_target(drone, max(80.0, 20.0))  # 최소 20cm 보장
    
    def _align_to_target(self, drone: Union[Tello, DebugDroneWrapper]) -> Optional[float]:
        """목표물 감지 및 거리 추정"""
        print(f"{Colors.CYAN}목표물 감지를 시작합니다...{Colors.END}")
        
        # 비전 감지 수행 (1회만)
        vision_action = VisionDetection(
            environment_color=self.environment_color,
            target_color=self.target_color
        )
        
        if vision_action.execute(drone):
            estimated_distance = vision_action.get_estimated_distance()
            target_center = vision_action.get_target_center()
            
            if estimated_distance and target_center:
                print(f"{Colors.GREEN}✓ 목표 감지 성공! 중심: {target_center}, 거리: {estimated_distance:.1f}cm{Colors.END}")
                return estimated_distance
            else:
                print(f"{Colors.YELLOW}목표 감지되었지만 거리 계산 실패, 기본 거리 사용{Colors.END}")
                return max(100.0, 20.0)  # 최소 20cm 보장
        else:
            print(f"{Colors.YELLOW}목표를 감지하지 못했지만 기본 거리로 전진합니다{Colors.END}")
            return max(100.0, 20.0)  # 최소 20cm 보장
    
    def _move_to_target(self, drone: Union[Tello, DebugDroneWrapper], distance: float) -> bool:
        """목표까지 이동"""
        print(f"{Colors.BLUE}목표까지 이동 시작 - 추정 거리: {distance:.1f}cm{Colors.END}")
        
        # 거리 제한 적용
        distance_cm = int(distance)
        original_distance = distance_cm
        
        if distance_cm < self.min_move_distance:
            distance_cm = self.min_move_distance
            print(f"{Colors.YELLOW}거리가 최소값보다 작음: {original_distance}cm → {distance_cm}cm{Colors.END}")
        elif distance_cm > self.max_move_distance:
            distance_cm = self.max_move_distance
            print(f"{Colors.YELLOW}거리가 최대값보다 큼: {original_distance}cm → {distance_cm}cm{Colors.END}")
        
        print(f"{Colors.CYAN}전진 거리: {distance_cm}cm{Colors.END}")
        
        # 전진 액션 실행
        move_action = MoveForward(distance=distance_cm)
        success = move_action.execute(drone)
        
        if success:
            print(f"{Colors.GREEN}✓ 목표까지 이동 완료{Colors.END}")
        else:
            print(f"{Colors.RED}✗ 목표까지 이동 실패{Colors.END}")
            
        return success
