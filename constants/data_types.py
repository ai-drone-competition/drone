"""
공통 데이터 타입 정의 모듈
"""
from typing import NamedTuple

class DetectionResult(NamedTuple):
    """감지 결과 데이터 클래스"""
    detected: bool
    center_x: int
    center_y: int
    bbox_x: int
    bbox_y: int
    bbox_width: int
    bbox_height: int
    area: int

class MovementCommand(NamedTuple):
    """드론 이동 명령 데이터 클래스"""
    move_x: int  # 좌우 이동 (-100 ~ 100, 음수=왼쪽, 양수=오른쪽)
    move_y: int  # 상하 이동 (-100 ~ 100, 음수=아래, 양수=위)
    move_z: int  # 전후 이동 (-100 ~ 100, 음수=후진, 양수=전진)
    rotate: int  # 회전 (-100 ~ 100, 음수=반시계, 양수=시계)
