"""
반시계방향 회전 동작
"""

from time import sleep
from ..base_action import BaseAction
from constants import Colors

class RotateCounterclockwise(BaseAction):
    """반시계방향 회전 동작"""
    
    def __init__(self, degrees: int = 90) -> None:
        """
        반시계방향 회전 동작 초기화
        
        Args:
            degrees (int): 회전할 각도 (도), 기본값: 90
        """
        super().__init__(degrees=degrees)
        self.degrees = degrees
        
    def execute(self, drone) -> bool:
        """반시계방향 회전 실행"""
        try:
            print(f"{Colors.YELLOW}반시계방향 회전 {self.degrees}도{Colors.END}")
            drone.rotate_counter_clockwise(self.degrees)
            print(f"{Colors.GREEN}✓ 반시계방향 회전 완료{Colors.END}")
            return True
        except Exception as e:
            print(f"{Colors.RED}✗ 반시계방향 회전 실패: {e}{Colors.END}")
            return False