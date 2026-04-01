"""
상승 동작
"""

from ..base_action import BaseAction
from constants import Colors

class MoveUp(BaseAction):
    """상승 동작"""
    
    def __init__(self, distance: int = 20) -> None:
        """
        상승 동작 초기화
        
        Args:
            distance (int): 상승할 거리 (cm), 기본값: 20
        """
        super().__init__(distance=distance)
        self.distance = distance
        
    def execute(self, drone) -> bool:
        """상승 실행"""
        try:
            print(f"{Colors.YELLOW}상승 {self.distance}cm{Colors.END}")
            drone.move_up(self.distance)
            print(f"{Colors.GREEN}✓ 상승 완료{Colors.END}")
            return True
        except Exception as e:
            print(f"{Colors.RED}✗ 상승 실패: {e}{Colors.END}")
            return False