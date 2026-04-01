"""
특정 높이로 이동 동작
"""

from ..base_action import BaseAction
from .MoveUp import MoveUp
from .MoveDown import MoveDown
from constants import Colors

class MoveToHeight(BaseAction):
    """특정 높이로 이동 동작"""
    
    def __init__(self, target_height: int, from_current: bool = False) -> None:
        """
        특정 높이로 이동 동작 초기화
        
        Args:
            target_height (int): 목표 높이 (cm) 또는 상대적 이동 거리 (cm)
            from_current (bool): True면 현재 높이 기준 상대 이동, False면 절대 높이
        """
        super().__init__(target_height=target_height, from_current=from_current)
        self.target_height = target_height
        self.from_current = from_current
        
    def execute(self, drone) -> bool:
        """특정 높이로 이동 실행"""
        try:
            # 현재 높이 확인
            current_height = drone.get_height()
            
            if self.from_current:
                # 상대적 이동 (현재 높이 기준)
                print(f"{Colors.CYAN}현재 높이: {current_height}cm, 상대 이동: {self.target_height:+d}cm{Colors.END}")
                
                if self.target_height == 0:
                    print(f"{Colors.GREEN}✓ 이동할 거리가 0입니다{Colors.END}")
                    return True
                
                # 이동할 거리의 절댓값
                move_distance = abs(self.target_height)
                
                # Tello SDK 제한: 최소 20cm 이동 필요
                if move_distance < 20:
                    print(f"{Colors.YELLOW}이동 거리 {move_distance}cm가 너무 짧습니다 (최소 20cm). 이동 생략{Colors.END}")
                    print(f"{Colors.GREEN}✓ 상대 이동 완료 (허용 오차 내){Colors.END}")
                    return True
                
                # 상대 이동 방향에 따라 상승 또는 하강 선택
                if self.target_height > 0:
                    # 상승 필요
                    print(f"{Colors.YELLOW}{move_distance}cm 상승 중...{Colors.END}")
                    move_action = MoveUp(distance=move_distance)
                else:
                    # 하강 필요
                    print(f"{Colors.YELLOW}{move_distance}cm 하강 중...{Colors.END}")
                    move_action = MoveDown(distance=move_distance)
            else:
                # 절대적 이동 (목표 높이까지)
                print(f"{Colors.CYAN}현재 높이: {current_height}cm, 목표 높이: {self.target_height}cm{Colors.END}")
                
                # 높이 차이 계산
                height_difference = self.target_height - current_height
                
                if height_difference == 0:
                    print(f"{Colors.GREEN}✓ 이미 목표 높이에 도달했습니다{Colors.END}")
                    return True
                
                # 이동할 거리의 절댓값
                move_distance = abs(height_difference)
                
                # Tello SDK 제한: 최소 20cm 이동 필요
                if move_distance < 20:
                    print(f"{Colors.YELLOW}이동 거리 {move_distance}cm가 너무 짧습니다 (최소 20cm). 이동 생략{Colors.END}")
                    print(f"{Colors.GREEN}✓ 목표 높이 {self.target_height}cm 도달 (허용 오차 내){Colors.END}")
                    return True
                
                # 높이 차이에 따라 상승 또는 하강 선택
                if height_difference > 0:
                    # 상승 필요
                    print(f"{Colors.YELLOW}{move_distance}cm 상승하여 목표 높이로 이동 중...{Colors.END}")
                    move_action = MoveUp(distance=move_distance)
                else:
                    # 하강 필요
                    print(f"{Colors.YELLOW}{move_distance}cm 하강하여 목표 높이로 이동 중...{Colors.END}")
                    move_action = MoveDown(distance=move_distance)
            
            # 이동 실행 (드론 객체 전달)
            success = move_action.execute(drone)
            
            if success:
                if self.from_current:
                    print(f"{Colors.GREEN}✓ 상대 이동 {self.target_height:+d}cm 완료{Colors.END}")
                else:
                    print(f"{Colors.GREEN}✓ 목표 높이 {self.target_height}cm로 이동 완료{Colors.END}")
            else:
                print(f"{Colors.RED}✗ 높이 이동 실패{Colors.END}")
            
            return success
            
        except Exception as e:
            print(f"{Colors.RED}✗ 높이 이동 실패: {e}{Colors.END}")
            print(f"{Colors.YELLOW}💡 해결 방법:{Colors.END}")
            print(f"{Colors.CYAN}  • 드론이 정상적으로 연결되어 있는지 확인하세요{Colors.END}")
            print(f"{Colors.CYAN}  • 목표 높이가 유효한 범위인지 확인하세요{Colors.END}")
            print(f"{Colors.CYAN}  • VPS가 정상 작동하는지 확인하세요{Colors.END}")
            return False
