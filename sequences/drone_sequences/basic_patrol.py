"""
기본 패트롤 시퀀스

정사각형 패턴으로 비행하는 기본 패트롤 시퀀스입니다.
이륙 -> 전진 -> 회전을 4번 반복 -> 착륙
"""

from constants import Colors
from .base_sequence import BaseSequence
from actions.movements import Takeoff, Land, MoveForward, RotateClockwise
from debug.drone import debug_sequence

class BasicPatrol(BaseSequence):
    """기본 패트롤 시퀀스 (정사각형 비행)"""
    
    def __init__(self, distance: int = 50, rotation: int = 90) -> None:
        """
        기본 패트롤 시퀀스 초기화
        
        Args:
            distance (int): 각 변의 길이 (cm), 기본값: 50
            rotation (int): 회전 각도 (도), 기본값: 90
        """
        super().__init__(name="기본 패트롤")
        self.distance = distance
        self.rotation = rotation
        
    @debug_sequence()
    def setup_actions(self) -> None:
        """패트롤 동작들 설정"""
        
        # 거리 유효성 검사
        if self.distance < 20:
            self.distance = 20
        
        # 이륙
        self.add_action(Takeoff())
        
        # 정사각형 비행 (4변)
        for i in range(4):
            # 전진
            self.add_action(MoveForward(distance=self.distance))
            # 회전 (마지막에는 회전하지 않음)
            if i < 3:
                self.add_action(RotateClockwise(degrees=self.rotation))
        
        # 착륙
        self.add_action(Land())
