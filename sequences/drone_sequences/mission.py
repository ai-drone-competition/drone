"""
미션 시퀀스

복잡한 고도 변화와 이동을 포함하는 미션 시퀀스입니다.
높이 센서를 활용하여 정확한 고도 제어를 수행합니다.

미션 순서:
1. 이륙 → 현재 고도에서 50cm 추가 상승 (약 1.5m 목표)
2. 1.5m 전진
3. 50cm 하강 (상대적)
4. 0.5m 전진
5. 90도 우회전
6. 0.5m 전진
7. 50cm 상승 (상대적)
8. 1.5m 전진
9. 착륙

주요 변경사항:
- 절대 고도 방식에서 상대 고도 방식으로 변경
- 이륙 후 현재 고도를 기준으로 한 상대적 이동 적용
"""

from constants import Colors
from .base_sequence import BaseSequence
from actions.movements import Takeoff, Land, MoveForward, RotateClockwise, MoveToHeight, MoveBackWard

from debug.drone import debug_sequence

class Mission(BaseSequence):
    """미션 시퀀스 (고도 변화와 이동 조합)"""
    
    def __init__(self) -> None:
        """미션 시퀀스 초기화"""
        super().__init__(name="미션")
        
    @debug_sequence()
    def setup_actions(self) -> None:
        """미션 동작들 설정"""
        
        # 1. 이륙 → 현재 고도에서 50cm 더 상승 (총 1m 목표)
        self.add_action(Takeoff())
        self.add_action(MoveToHeight(target_height=50, from_current=True))
        self.add_action(MoveToHeight(target_height=50, from_current=True))

        # 2. 1.5m 전진
        self.add_action(MoveForward(distance=50))
        self.add_action(MoveForward(distance=50))
        self.add_action(MoveForward(distance=50))

        # 3. 50cm 하강 (1.5m → 1m)
        self.add_action(MoveToHeight(target_height=-50, from_current=True))

        # 4. 0.5m 전진
        self.add_action(MoveForward(distance=50))

        # 5. 시계방향 90도 회전
        self.add_action(RotateClockwise(degrees=90))

        # 6. 0.5m 전진
        self.add_action(MoveForward(distance=50))

        # 7. 0.5cm 상승 (1.5m → 1m)
        self.add_action(MoveToHeight(target_height=50, from_current=True))

        # 8. 1.5m 전진
        self.add_action(MoveForward(distance=50))

        # 9. 착륙
        self.add_action(Land())
        
       
