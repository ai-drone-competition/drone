"""
드론 연결 관리자 모듈

모든 연결 관련 기능을 통합하여 제공합니다.
auto_reconnect_drone만 외부로 노출하여 사용자가 복잡한 내부 구조를 알 필요 없게 합니다.

사용법:
    from connection_manager import auto_reconnect_drone, get_drone
    
    @auto_reconnect_drone
    def my_drone_task():
        drone = get_drone()
        # ... 드론 작업 수행
"""

from .index import auto_reconnect_drone, get_drone, get_vps_status, get_decorator_drone

__all__ = ['auto_reconnect_drone', 'get_drone', 'get_vps_status', 'get_decorator_drone']
