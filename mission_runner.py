"""
미션 시퀀스 실행 파일
높이 센서를 활용한 복합 미션을 실행
"""

from sequences.drone_sequences import Mission
from connection_manager import auto_reconnect_drone
from sequences.combined_sequences import PrecisionLanding

@auto_reconnect_drone
def main(drone=None):
    """미션 시퀀스 실행"""
    
    # 1단계: 미션 시퀀스 실행
    Mission().execute()
    
    # 2단계: 정밀 착지 시퀀스 실행
    return PrecisionLanding().execute(drone)

if __name__ == "__main__":
    main()
