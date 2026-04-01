"""
정밀 착지 시퀀스

목표물을 감지하여 정밀 착지를 수행하는 시퀀스입니다.

시퀀스 순서:
1. 목표물 방향 정렬 및 이동 (비전 감지 + 회전 + 전진)
2. 착지 (카메라 자동 종료)
"""

from sequences.drone_sequences.base_sequence import BaseSequence
from actions.movements.Land import Land
from actions.vision.align_to_target import AlignToTarget
from vision_color_config import RED_COLOR, WHITE_COLOR
from debug.drone import debug_sequence


class PrecisionLanding(BaseSequence):
    """정밀 착지 시퀀스 - 목표 감지 후 이동 및 착지"""
    
    def __init__(self) -> None:
        """정밀 착지 시퀀스 초기화"""
        super().__init__(name="정밀 착지")
        
    @debug_sequence()
    def setup_actions(self) -> None:
        """정밀 착지 동작들 설정"""
        
        # 1단계: 목표물 정렬 및 이동 (비전 감지 + 회전 + 전진)
        self.add_action(AlignToTarget(
            environment_color=RED_COLOR,
            target_color=WHITE_COLOR
        ))
        
        # 2단계: 착지
        self.add_action(Land())
