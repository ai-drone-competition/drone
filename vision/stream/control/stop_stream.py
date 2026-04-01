import time

def stop_stream(drone) -> None:
    """
    드론 비디오 스트림 중지
    
    Args:
        drone: 연결된 드론 객체
    """
    try:
        drone.streamoff()
        # 포트 해제를 위한 대기 시간 추가
        time.sleep(2.0)
    except Exception as e:
        print(f"드론 스트림 종료 중 오류: {e}")
        # 오류가 발생해도 대기 시간 확보
        time.sleep(2.0)