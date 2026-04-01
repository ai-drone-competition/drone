"""
스트림 상태 관리자
단일 책임: 스트림의 상태 관리 및 제어
"""


class StreamStateManager:
    """스트림 상태 관리 전용 클래스"""
    
    def __init__(self, stabilization_delay: float = 3.0):
        """
        StreamStateManager 초기화
        
        Args:
            stabilization_delay: 안정화 지연 시간
        """
        self._is_stream_active = False
        self._stabilization_delay = stabilization_delay
    
    def start(self) -> None:
        """스트림 시작"""
        self._is_stream_active = True
    
    def stop(self) -> None:
        """스트림 중지"""
        self._is_stream_active = False
    
    def is_running(self) -> bool:
        """스트림 실행 상태 확인"""
        return self._is_stream_active
    
    @property
    def stabilization_delay(self) -> float:
        """안정화 지연 시간"""
        return self._stabilization_delay
    
    @stabilization_delay.setter
    def stabilization_delay(self, delay: float) -> None:
        """안정화 지연 시간 설정"""
        if delay > 0:
            self._stabilization_delay = delay
