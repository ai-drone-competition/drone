"""
스트림 관리자
"""
import numpy as np
from typing import Callable, Any, Optional, Dict
from .control.start_stream import start_stream
from .control.stop_stream import stop_stream
from .managers import StreamStateManager, DisplayManager, DroneMonitor, DebugManager, StreamLoopProcessor
from constants import Colors


class VisionStreamManager:
    """스트림 관리 전용 클래스 - 단순 실행 인터페이스 제공"""
    
    def __init__(self, window_name: str = "Vision Stream", debug_mode: bool = True,
                 color_configs: Optional[Dict[str, Dict]] = None):
        """
        VisionStreamManager 초기화
        
        Args:
            window_name: OpenCV 창 이름
            debug_mode: 디버깅 모드 활성화 여부
            color_configs: 색상별 통합 설정 (ENVIRONMENT_COLOR, TARGET_COLOR 형태)
        """
        # 관리자들 초기화
        self.state_manager = StreamStateManager()
        self.display_manager = DisplayManager(window_name)
        self.drone_monitor = DroneMonitor()
        self.debug_manager = DebugManager(debug_mode, color_configs)
        self.loop_processor = StreamLoopProcessor()
    
    def execute(self, drone: Any, frame_processor: Callable[[np.ndarray], np.ndarray]) -> bool:
        """
        비전 스트림 실행 (단일 진입점)
        
        Args:
            drone: 연결된 드론 객체
            frame_processor: 프레임 처리 함수
            
        Returns:
            처리 성공 여부
        """
        try:
            # 스트림 시작
            if not start_stream(drone, self.state_manager.stabilization_delay):
                print(f"{Colors.RED}드론 비디오 스트림 시작 실패{Colors.END}")
                return False
            
            self.state_manager.start()
            print(f"{Colors.GREEN}드론 비디오 스트림 시작됨{Colors.END}")
            
            # 드론 상태 확인
            self.drone_monitor.check_drone_status(drone)
            
            # 디버깅 카운터 리셋
            self.debug_manager.reset_counters()
            
            # 메인 루프 실행
            return self.loop_processor.process_stream_loop(
                drone=drone,
                frame_processor=frame_processor,
                is_active_callback=self.state_manager.is_running,
                display_callback=self.display_manager.display_frame,
                deactivate_callback=self.state_manager.stop
            )
            
        except Exception as e:
            print(f"{Colors.RED}드론 비디오 스트림 오류: {e}{Colors.END}")
            return False
        finally:
            self._cleanup(drone)
    
    def _cleanup(self, drone: Any) -> None:
        """
        스트림 정리 (내부 메서드)
        
        Args:
            drone: 연결된 드론 객체
        """
        stop_stream(drone)
        self.state_manager.stop()
        self.display_manager.close_all_windows()
        print(f"{Colors.YELLOW}드론 비디오 스트림 종료{Colors.END}")
