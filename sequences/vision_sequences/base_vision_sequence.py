"""
비전 시퀀스 기본 클래스

모든 비전 시퀀스가 상속받아야 하는 기본 클래스입니다.
drone.sequences.BaseSequence와 동일한 패턴을 따릅니다.
"""

from abc import ABC, abstractmethod
from typing import Optional, Union
from djitellopy import Tello
from constants import Colors
from connection_manager import get_drone
from debug.drone import DebugDroneWrapper


class BaseVisionSequence(ABC):
    """모든 비전 시퀀스의 기본 클래스"""
    
    def __init__(self, name: str = "") -> None:
        """
        비전 시퀀스 초기화
        
        Args:
            name (str): 시퀀스 이름
        """
        self.name = name or self.__class__.__name__
        self.is_running = False
        self._setup_complete = False
        
    @abstractmethod
    def setup_vision(self) -> None:
        """
        비전 처리 설정
        하위 클래스에서 구현해야 함
        """
        pass
    
    @abstractmethod
    def process_vision(self, drone: Union[Tello, DebugDroneWrapper]) -> bool:
        """
        실제 비전 처리 로직
        하위 클래스에서 구현해야 함
        
        Args:
            drone: 연결된 드론 객체
            
        Returns:
            bool: 처리 성공 여부
        """
        pass
    
    def execute(self, drone=None) -> bool:
        """
        비전 시퀀스 실행
        
        Args:
            drone: 연결된 드론 객체 (auto_reconnect_drone 데코레이터에서 전달)
        
        Returns:
            bool: 실행 성공 여부
        """
        print(f"{Colors.BOLD}{Colors.PURPLE}{'=' * 60}")
        print(f"🎯 {self.name} 시작")
        print(f"{'=' * 60}{Colors.END}")
        
        # 드론 객체 확인
        if not drone:
            # 데코레이터에서 전달되지 않은 경우 fallback
            from connection_manager import get_drone
            drone = get_drone()
            if not drone:
                print(f"{Colors.RED}✗ 드론 연결 실패{Colors.END}")
                return False
        
        print(f"{Colors.GREEN}✓ 드론 연결 성공{Colors.END}")
        
        # 비전 설정이 완료되지 않았다면 설정
        if not self._setup_complete:
            self.setup_vision()
            self._setup_complete = True
        
        print(f"{Colors.YELLOW}📹 드론 비디오 스트림을 시작합니다{Colors.END}")
        print(f"{Colors.CYAN}💡 종료하려면 OpenCV 창의 X 버튼을 클릭하세요{Colors.END}")
        
        try:
            self.is_running = True
            success = self.process_vision(drone)
            return success
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}사용자에 의해 중단됨{Colors.END}")
            return True
        except Exception as e:
            print(f"\n{Colors.RED}오류 발생: {e}{Colors.END}")
            return False
        finally:
            self.is_running = False
            self._cleanup()
            print(f"\n{Colors.GREEN}{self.name} 종료{Colors.END}")
    
    def _cleanup(self) -> None:
        """리소스 정리"""
        # 하위 클래스에서 필요시 오버라이드
        pass
    
    def stop(self) -> None:
        """비전 시퀀스 중지"""
        self.is_running = False
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
