"""
전진 동작
"""

from ..base_action import BaseAction
from constants import Colors

class MoveForward(BaseAction):
    """전진 동작"""
    
    def __init__(self, distance: int = 20) -> None:
        """
        전진 동작 초기화
        
        Args:
            distance (int): 전진할 거리 (cm), 기본값: 20
        """
        super().__init__(distance=distance)
        self.distance = distance
        
    def execute(self, drone) -> bool:
        """전진 실행"""
        # 거리 유효성 검사
        if self.distance < 20:
            print(f"{Colors.RED}⚠️  전진 거리가 너무 작습니다: {self.distance}cm (최소: 20cm){Colors.END}")
            return False
        
        if self.distance > 500:
            print(f"{Colors.RED}⚠️  전진 거리가 너무 큽니다: {self.distance}cm (최대: 500cm){Colors.END}")
            return False
            
        try:
            print(f"{Colors.YELLOW}전진 {self.distance}cm 실행 중...{Colors.END}")
            
            # 전진 명령 실행
            drone.move_forward(self.distance)
            
            # 결과 확인
            print(f"{Colors.GREEN}✓ 전진 {self.distance}cm 완료{Colors.END}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}✗ 전진 실패: {e}{Colors.END}")
            print(f"{Colors.YELLOW}💡 해결 방법:{Colors.END}")
            print(f"{Colors.CYAN}  • 이동 거리를 20cm 이상으로 설정하세요{Colors.END}")
            print(f"{Colors.CYAN}  • 드론 앞에 장애물이 있는지 확인하세요{Colors.END}")
            print(f"{Colors.CYAN}  • VPS가 정상 작동하는지 확인하세요{Colors.END}")
            return False