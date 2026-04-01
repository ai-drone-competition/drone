"""
드론 모니터링 관리자
단일 책임: 드론 상태 모니터링 및 체크
"""
from typing import Any
from constants import Colors


class DroneMonitor:
    """드론 상태 모니터링 전용 클래스"""
    
    def __init__(self):
        """DroneMonitor 초기화"""
        pass
    
    def check_drone_status(self, drone: Any) -> None:
        """
        드론 상태 확인
        
        Args:
            drone: 연결된 드론 객체
        """
        try:
            battery = drone.get_battery()
            print(f"{Colors.BLUE}드론 배터리: {battery}%{Colors.END}")
        except Exception as e:
            print(f"{Colors.YELLOW}배터리 정보 읽기 실패: {e}{Colors.END}")
    
    def check_connection(self, drone: Any) -> bool:
        """
        드론 연결 상태 확인
        
        Args:
            drone: 연결된 드론 객체
            
        Returns:
            연결 상태
        """
        try:
            # 간단한 상태 체크 (배터리 정보로 연결 확인)
            drone.get_battery()
            return True
        except Exception:
            return False
    
    def get_battery_level(self, drone: Any) -> int:
        """
        드론 배터리 레벨 반환
        
        Args:
            drone: 연결된 드론 객체
            
        Returns:
            배터리 레벨 (0-100), 실패 시 -1
        """
        try:
            return drone.get_battery()
        except Exception:
            return -1
