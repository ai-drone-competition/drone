"""
호버링 동작
"""

from time import sleep
from ..base_action import BaseAction
from constants import Colors

class Hover(BaseAction):
    """호버링 동작"""
    
    def __init__(self, duration: float = 3.0) -> None:
        """
        호버링 동작 초기화
        
        Args:
            duration (float): 호버링 지속 시간 (초), 기본값: 3.0
        """
        super().__init__(duration=duration)
        self.duration = duration
        
    def execute(self, drone) -> bool:
        """호버링 실행"""
        try:
            print(f"{Colors.YELLOW}호버링 {self.duration}초{Colors.END}")
            sleep(self.duration)
            print(f"{Colors.GREEN}✓ 호버링 완료{Colors.END}")
            return True
        except Exception as e:
            print(f"{Colors.RED}✗ 호버링 실패: {e}{Colors.END}")
            return False