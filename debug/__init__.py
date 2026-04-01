"""
디버깅 시스템 모듈
프로젝트 전체의 디버깅 기능을 체계적으로 관리

구조:
- debug.drone: 드론 및 시퀀스 관련 디버깅 (메서드 호출, 래퍼, 로거, 시퀀스 실행)
- debug.vision: 비전 관련 디버깅 (OpenCV 시각화, FPS, 상태)

사용법:
    from debug.drone import debug_drone_method, DebugDroneWrapper, debug_sequence
    from debug.vision import VisionDebugger
    
    # 또는 통합 import
    from debug import debug_drone_method, debug_sequence, VisionDebugger
"""

# 드론 및 시퀀스 관련 디버깅 (통합)
from .drone import (
    debug_drone_method, DebugDroneWrapper, DroneDebugLogger,
    debug_sequence, SequenceDebugLogger
)

# 비전 관련 디버깅
from .vision import VisionDebugger

__all__ = [
    # 드론 디버깅
    'debug_drone_method',
    'DebugDroneWrapper', 
    'DroneDebugLogger',
    
    # 시퀀스 디버깅 (drone에 통합됨)
    'debug_sequence',
    'SequenceDebugLogger',
    
    # 비전 디버깅
    'VisionDebugger'
]
