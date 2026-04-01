"""
조합 시퀀스 모듈

드론 동작과 비전 처리를 조합한 복합 시퀀스들을 제공합니다.
향후 확장을 위한 기반 구조입니다.

예시:
- PatrolAndDetect: 패트롤 수행 후 객체 감지
- SearchAndTrack: 탐색하며 객체 추적
- PrecisionLandingSequence: 목표물 인식 후 정밀 착륙
"""

from .precision_landing import PrecisionLanding

# 향후 조합 시퀀스들이 추가될 예정
# from .patrol_and_detect import PatrolAndDetect
# from .search_and_track import SearchAndTrack

__all__ = [
    'PrecisionLanding',
    # 향후 추가될 조합 시퀀스들
    # 'PatrolAndDetect',
    # 'SearchAndTrack'
]
