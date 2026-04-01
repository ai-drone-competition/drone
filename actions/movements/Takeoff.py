"""
이륙 동작
"""

from ..base_action import BaseAction
from constants import Colors

class Takeoff(BaseAction):
    """이륙 동작"""
    
    def __init__(self) -> None:
        """이륙 동작 초기화"""
        super().__init__()
        
    def execute(self, drone) -> bool:
        """이륙 실행"""
        try:
            print(f"{Colors.YELLOW}이륙{Colors.END}")
            drone.takeoff()
            print(f"{Colors.GREEN}✓ 이륙 완료{Colors.END}")
            return True
        except Exception as e:
            print(f"{Colors.RED}✗ 이륙 실패: {e}{Colors.END}")
            return False