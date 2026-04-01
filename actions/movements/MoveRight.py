"""
우이동 동작
"""

from ..base_action import BaseAction
from constants import Colors

class MoveRight(BaseAction):
    """우이동 동작"""
    
    def __init__(self, distance: int = 20) -> None:
        """
        우이동 동작 초기화
        
        Args:
            distance (int): 우이동할 거리 (cm), 기본값: 20
        """
        super().__init__(distance=distance)
        self.distance = distance
        
    def execute(self, drone) -> bool:
        """우이동 실행"""
        try:
            print(f"{Colors.YELLOW}우이동 {self.distance}cm{Colors.END}")
            drone.move_right(self.distance)
            print(f"{Colors.GREEN}✓ 우이동 완료{Colors.END}")
            return True
        except Exception as e:
            print(f"{Colors.RED}✗ 우이동 실패: {e}{Colors.END}")
            return False