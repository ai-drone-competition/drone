"""
드론 연결 및 해제 관리 모듈
드론의 기본적인 연결과 해제 작업을 담당
"""
from djitellopy import Tello
import time
import logging
from typing import Optional, Union
from ..message import ConnectionErrorHandler, ConnectionMessageHandler
from debug.drone import DebugDroneWrapper

# djitellopy 로그 완전 비활성화
logging.getLogger('djitellopy').setLevel(logging.CRITICAL)
logging.getLogger('djitellopy.tello').setLevel(logging.CRITICAL)

class DroneConnectionManager:
    """드론 연결 상태 관리 클래스"""
    _drone: Optional[Tello] = None
    _debug_drone: Optional[DebugDroneWrapper] = None
    _is_connected: bool = False
    _debug_enabled: bool = True
    
    @classmethod
    def set_debug_mode(cls, enabled: bool) -> None:
        """디버깅 모드 설정"""
        cls._debug_enabled = enabled
        if cls._debug_drone:
            cls._debug_drone.set_debug_enabled(enabled)
    
    @classmethod
    def connect(cls) -> Optional[Union[Tello, DebugDroneWrapper]]:
        """드론 연결"""
        if cls._is_connected and cls._debug_drone:
            return cls._debug_drone
        
        max_attempts = 3
        
        for attempt in range(1, max_attempts + 1):
            try:
                cls._drone = Tello()
                cls._drone.connect()
                
                # 디버깅 래퍼로 감싸기
                cls._debug_drone = DebugDroneWrapper(cls._drone)
                cls._debug_drone.set_debug_enabled(cls._debug_enabled)
                
                # 초기 상태 표시 (배터리 등)
                if cls._debug_enabled:
                    cls._debug_drone.show_initial_status()
                
                cls._is_connected = True
                return cls._debug_drone
            except Exception as e:
                if attempt < max_attempts:
                    time.sleep(1)  # 1초 대기 후 재시도
                    continue
                else:
                    # 최종 실패
                    ConnectionErrorHandler.handle_connection_error(e)
                    cls._drone = None
                    cls._debug_drone = None
                    cls._is_connected = False
                    return None
        
        return None
    
    @classmethod
    def disconnect(cls) -> None:
        """드론 연결 해제"""
        if cls._is_connected and cls._drone:
            try:
                cls._drone.end()
                ConnectionMessageHandler.print_success_message("disconnection")
            except Exception as e:
                ConnectionErrorHandler.handle_disconnection_error(e)
            finally:
                cls._is_connected = False
                cls._drone = None
                cls._debug_drone = None
    
    @classmethod
    def get_drone(cls) -> Optional[Union[Tello, DebugDroneWrapper]]:
        """현재 연결된 드론 객체 반환 (디버깅 래퍼 포함)"""
        if not cls._is_connected or not cls._debug_drone:
            ConnectionErrorHandler.print_warning_message("드론이 연결되어 있지 않습니다.")
            return None
        return cls._debug_drone
    
    @classmethod
    def get_raw_drone(cls) -> Optional[Tello]:
        """원본 드론 객체 반환 (디버깅 없음)"""
        if not cls._is_connected or not cls._drone:
            ConnectionErrorHandler.print_warning_message("드론이 연결되어 있지 않습니다.")
            return None
        return cls._drone

# 전역에서 사용할 수 있는 드론 객체 접근 함수
def get_drone() -> Optional[Union[Tello, DebugDroneWrapper]]:
    """전역에서 드론 객체에 접근하기 위한 함수 (디버깅 포함)"""
    return DroneConnectionManager.get_drone()

def get_raw_drone() -> Optional[Tello]:
    """전역에서 원본 드론 객체에 접근하기 위한 함수 (디버깅 없음)"""
    return DroneConnectionManager.get_raw_drone()

def set_debug_mode(enabled: bool) -> None:
    """전역 디버깅 모드 설정"""
    DroneConnectionManager.set_debug_mode(enabled)
