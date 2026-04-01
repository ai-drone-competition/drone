"""
자동 재연결 드론 연결 관리자
모든 연결 관련 기능을 통합하여 @auto_reconnect_drone 데코레이터 제공
"""
import atexit
from typing import Callable, Any
from functools import wraps
from .message import ConnectionErrorHandler, ConnectionMessageHandler
from .handlers import DroneConnectionManager, get_drone, ConnectionRetryHandler, ConnectionMonitoringHandler, TaskState, VPSManagementHandler

# 데코레이터가 관리하는 전역 드론 객체
_decorator_drone = None

def auto_reconnect_drone(func: Callable) -> Callable:
    """
    자동 재연결 및 연결 처리 데코레이터
    - 작업 시작 전 자동 연결
    - VPS failsafe 우회 설정
    - 작업 중 연결 끊김 시 자동 재연결
    - 작업 완료 후 자동 해제
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        global _decorator_drone
        
        # 작업 시작 메시지
        ConnectionMessageHandler.print_work_start_message()
        
        # 초기 연결
        drone = ConnectionRetryHandler.retry_with_timeout(DroneConnectionManager.connect, 13)
        if not drone:
            ConnectionErrorHandler.print_warning_message("드론 연결에 실패하여 작업을 중단합니다.")
            return False
        
        # 데코레이터가 생성한 드론 객체를 전역 변수에 저장
        _decorator_drone = drone
        
        # VPS failsafe 우회 설정
        vps_success = VPSManagementHandler.attempt_vps_workaround()
        if not vps_success:
            ConnectionErrorHandler.print_warning_message("VPS 우회 설정에 실패했지만 작업을 계속 진행합니다.")
        
        # 작업 상태 초기화
        task_state = TaskState()
        
        # 연결 모니터링 시작
        ConnectionMonitoringHandler.start_monitoring(task_state)
        
        try:
            # 원본 함수 실행 시 드론 객체 주입
            if 'drone' not in kwargs:
                kwargs['drone'] = drone
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            ConnectionErrorHandler.handle_operation_error(e, "작업")
            return False
        finally:
            # 데코레이터 드론 객체 초기화
            _decorator_drone = None
            
            # 연결 모니터링 중지
            ConnectionMonitoringHandler.stop_monitoring()
            
            # VPS 우회 설정 해제
            VPSManagementHandler.disable_vps_override()
            
            # 드론 해제
            DroneConnectionManager.disconnect()
            
            # 작업 완료 메시지
            ConnectionMessageHandler.print_work_end_message()
    
    return wrapper

def get_decorator_drone():
    """데코레이터가 생성한 드론 객체 반환"""
    return _decorator_drone

# 프로그램 종료 시 자동 정리
atexit.register(DroneConnectionManager.disconnect)

# 외부에서 사용할 수 있는 함수들 재export
def get_vps_status() -> dict:
    """VPS 상태 정보 반환"""
    return VPSManagementHandler.get_vps_status()

__all__ = ['auto_reconnect_drone', 'get_drone', 'get_vps_status', 'get_decorator_drone']
