"""
하강 동작
"""

from ..base_action import BaseAction
from constants import Colors

class MoveDown(BaseAction):
    """하강 동작"""
    
    def __init__(self, distance: int = 20) -> None:
        """
        하강 동작 초기화
        
        Args:
            distance (int): 하강할 거리 (cm), 기본값: 20
        """
        super().__init__(distance=distance)
        self.distance = distance
        
    def execute(self, drone) -> bool:
        """하강 실행"""
        try:
            print(f"{Colors.YELLOW}하강 {self.distance}cm{Colors.END}")
            drone.move_down(self.distance)
            print(f"{Colors.GREEN}✓ 하강 완료{Colors.END}")
            return True
        except Exception as e:
            print(f"{Colors.RED}✗ 하강 실패: {e}{Colors.END}")
            return False