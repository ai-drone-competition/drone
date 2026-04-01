"""
정밀 착지 실행 파일
"""

from typing import Union
from djitellopy import Tello
from sequences.combined_sequences import PrecisionLanding
from actions.movements.Takeoff import Takeoff
from connection_manager import auto_reconnect_drone
from debug.drone import DebugDroneWrapper
from constants import Colors

@auto_reconnect_drone
def main(drone: Union[Tello, DebugDroneWrapper, None] = None) -> bool:
    """정밀 착지 메인 함수"""
    
    # 1단계: 이륙
    print(f"{Colors.CYAN}=== 정밀 착지 프로세스 시작 ==={Colors.END}")
    takeoff_action = Takeoff()
    if not takeoff_action.execute(drone):
        return False
    
    # 2단계: 정밀 착지 시퀀스 실행
    return PrecisionLanding().execute(drone)

if __name__ == "__main__":
    main()
