"""
착륙 동작
"""

from ..base_action import BaseAction
from constants import Colors

class Land(BaseAction):
    """착륙 동작"""
    
    def __init__(self) -> None:
        """착륙 동작 초기화"""
        super().__init__()
        
    def execute(self, drone) -> bool:
        """착륙 실행"""
        try:
            print(f"{Colors.YELLOW}착륙{Colors.END}")
            drone.land()
            print(f"{Colors.GREEN}✓ 착륙 완료{Colors.END}")
            return True
        except Exception as e:
            print(f"{Colors.RED}✗ 착륙 실패: {e}{Colors.END}")
            return False