import time

def start_stream(drone, stabilization_delay: float = 3.0) -> bool:
    """
    드론 비디오 스트림 시작
    
    Args:
        drone: 연결된 드론 객체
        stabilization_delay: 스트림 안정화 대기 시간 (초)
        
    Returns:
        스트림 시작 성공 여부
    """
    try:
        drone.streamon()
        time.sleep(stabilization_delay)
        return True
    except Exception as e:
        print(f"드론 비디오 스트림 시작 실패: {e}")
        return False