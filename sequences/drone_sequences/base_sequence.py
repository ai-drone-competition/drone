"""
시퀀스 기본 클래스

모든 시퀀스가 상속받아야 하는 기본 클래스입니다.
"""

from abc import ABC, abstractmethod
from typing import List
from time import sleep
from constants import Colors
from actions.base_action import BaseAction
from debug.drone import debug_sequence

class BaseSequence(ABC):
    """모든 시퀀스의 기본 클래스"""
    
    def __init__(self, name: str = "") -> None:
        """
        시퀀스 초기화
        
        Args:
            name (str): 시퀀스 이름
        """
        self.name = name or self.__class__.__name__
        self.actions: List[BaseAction] = []
        self.current_step = 0
        
    @abstractmethod
    def setup_actions(self) -> None:
        """
        시퀀스에서 실행할 동작들을 설정
        하위 클래스에서 구현해야 함
        """
        pass
    
    def add_action(self, action: BaseAction) -> None:
        """시퀀스에 동작 추가"""
        self.actions.append(action)
        
    @debug_sequence()
    def execute(self, drone = None, delay: float = 0.2) -> bool:
        """
        시퀀스 실행
        
        Args:
            drone: 드론 객체 (선택사항, None이면 자동으로 가져옴)
            delay (float): 각 동작 사이의 대기 시간 (초)
            
        Returns:
            bool: 실행 성공 여부
        """
        print(f"{Colors.CYAN}{self.name} 시퀀스 시작...{Colors.END}")
        
        # 동작들이 설정되지 않았다면 설정
        if not self.actions:
            self.setup_actions()
        
        # 드론 객체 가져오기 (매개변수로 전달되면 우선 사용)
        if drone is None:
            try:
                from connection_manager import get_decorator_drone, get_drone
                drone = get_decorator_drone() or get_drone()
                if not drone:
                    print(f"{Colors.RED}드론 객체를 가져올 수 없습니다{Colors.END}")
                    return False
            except Exception as e:
                print(f"{Colors.RED}드론 객체 접근 실패: {e}{Colors.END}")
                return False
        
        # 디버깅 카운터 초기화
        try:
            if hasattr(drone, 'reset_counters') and callable(getattr(drone, 'reset_counters')):
                drone.reset_counters()  # type: ignore
        except Exception:
            pass  # 디버깅 기능이므로 실패해도 무시
            
        total_steps = len(self.actions)
        print(f"{Colors.BLUE}총 {total_steps}개 동작을 실행합니다{Colors.END}")
        
        for i, action in enumerate(self.actions, 1):
            try:
                # 실행될 클래스명과 파라미터 출력
                class_name = action.__class__.__name__
                params = {}
                
                # 액션 객체의 속성들을 파라미터로 수집
                for attr_name in dir(action):
                    if not attr_name.startswith('_') and not callable(getattr(action, attr_name)):
                        attr_value = getattr(action, attr_name)
                        if attr_name not in ['description']:  # description은 제외
                            params[attr_name] = attr_value
                
                print(f"{Colors.YELLOW}  {i}/{total_steps}. 실행 클래스: {class_name}, 파라미터: {params}{Colors.END}")
                
                # 드론 객체를 액션에 전달
                success = action.execute(drone)
                if not success:
                    print(f"{Colors.RED}  ✗ 동작 실패: {class_name}{Colors.END}")
                    print(f"{Colors.RED}  시퀀스를 중단합니다 (진행률: {i-1}/{total_steps}){Colors.END}")
                    return False
                    
                self.current_step = i
                print(f"{Colors.GREEN}  ✓ 단계 {i}/{total_steps} 완료: {class_name}{Colors.END}")
                
                # 마지막 동작이 아니라면 대기
                if i < total_steps:
                    print(f"{Colors.CYAN}  다음 동작까지 {delay}초 대기...{Colors.END}")
                    sleep(delay)
                    
            except Exception as e:
                print(f"{Colors.RED}  ✗ 시퀀스 실행 중 오류: {e}{Colors.END}")
                print(f"{Colors.RED}  시퀀스를 중단합니다 (진행률: {i-1}/{total_steps}){Colors.END}")
                return False
        
        print(f"{Colors.GREEN}{self.name} 시퀀스 완료 ({total_steps}/{total_steps}){Colors.END}")
        return True
    
    def get_progress(self) -> tuple[int, int]:
        """
        현재 진행 상황 반환
        
        Returns:
            tuple[int, int]: (현재 단계, 전체 단계)
        """
        return (self.current_step, len(self.actions))
    
    def reset(self) -> None:
        """시퀀스 초기화"""
        self.current_step = 0
        
    def __str__(self) -> str:
        return f"{self.name} ({len(self.actions)} actions)"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', actions={len(self.actions)})"
