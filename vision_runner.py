"""
DJI Tello EDU 비전 시스템 실행 파일
드론 카메라를 이용한 OpenCV 주변색(빨간색) 및 목표색(하얀색) 객체 감지
색상별 개별 감지를 통해 각 색상을 구분하여 표시
"""

from sequences.vision_sequences import ColorObjectDetection
from connection_manager import auto_reconnect_drone
from vision_color_config import (
    DEFAULT_MIN_AREA, RED_COLOR, WHITE_COLOR
)

@auto_reconnect_drone
def main(drone=None) -> bool:
    """DJI Tello EDU 비전 시스템 메인 함수"""
    
    sequence = ColorObjectDetection(
        min_area=DEFAULT_MIN_AREA, 
        environment_color=RED_COLOR,
        target_color=WHITE_COLOR
    )
    return sequence.execute(drone)  # 드론 객체 전달

if __name__ == "__main__":
    main()
