"""
드론 시퀀스 실행 파일
시퀀스를 불러와서 auto_reconnect_drone으로 감싸서 실행
"""

from sequences.drone_sequences import BasicPatrol
from connection_manager import auto_reconnect_drone

@auto_reconnect_drone
def main(drone=None):
    """기본 패트롤 시퀀스 실행"""
    
    BasicPatrol(distance=30, rotation=90).execute()  # 30cm로 안전하게 설정

if __name__ == "__main__":
    main()
