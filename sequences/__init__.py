"""
통합 시퀀스 모듈

드론과 비전을 조합한 시퀀스들과 각각의 전용 시퀀스들을 제공합니다.
"""

# 드론 전용 시퀀스들
from .drone_sequences import BaseSequence, BasicPatrol, Mission

# 비전 전용 시퀀스들  
from .vision_sequences import BaseVisionSequence, ColorObjectDetection

# 조합 시퀀스들 (향후 추가 예정)
# from .combined_sequences import PatrolAndDetect, SearchAndTrack

__all__ = [
    # 드론 시퀀스들
    'BaseSequence', 'BasicPatrol', 'Mission',
    # 비전 시퀀스들
    'BaseVisionSequence', 'ColorObjectDetection',
    # 조합 시퀀스들 (향후 추가)
    # 'PatrolAndDetect', 'SearchAndTrack'
]
