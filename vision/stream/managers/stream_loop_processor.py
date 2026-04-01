"""
스트림 루프 처리기
단일 책임: 메인 스트림 처리 루프 관리
"""
import numpy as np
from typing import Callable, Any
from ..frame.get_processed_frame import get_processed_frame
from ..frame.validate_frame import validate_frame
from constants import Colors


class StreamLoopProcessor:
    """스트림 루프 처리 전용 클래스"""
    
    def __init__(self, max_consecutive_fails: int = 20):
        """
        StreamLoopProcessor 초기화
        
        Args:
            max_consecutive_fails: 최대 연속 실패 횟수
        """
        self.max_consecutive_fails = max_consecutive_fails
    
    def process_stream_loop(self, drone: Any, frame_processor: Callable[[np.ndarray], np.ndarray],
                          is_active_callback: Callable[[], bool],
                          display_callback: Callable[[np.ndarray], bool],
                          deactivate_callback: Callable[[], None]) -> bool:
        """
        스트림 처리 메인 루프
        
        Args:
            drone: 연결된 드론 객체
            frame_processor: 프레임 처리 함수
            is_active_callback: 스트림 활성 상태 확인 콜백
            display_callback: 프레임 표시 콜백
            deactivate_callback: 스트림 비활성화 콜백
            
        Returns:
            처리 성공 여부
        """
        frame_fail_count = 0
        
        while is_active_callback():
            # 프레임 읽기
            frame = get_processed_frame(drone)
            
            if not validate_frame(frame):
                frame_fail_count += 1
                if frame_fail_count >= self.max_consecutive_fails:
                    print(f"{Colors.RED}연속 프레임 읽기 실패가 {self.max_consecutive_fails}회를 초과했습니다. 스트림을 종료합니다.{Colors.END}")
                    deactivate_callback()
                    break
                print(f"{Colors.YELLOW}드론 프레임 읽기 실패 ({frame_fail_count}/{self.max_consecutive_fails}){Colors.END}")
                continue
            
            # 프레임 읽기 성공 시 카운터 리셋
            frame_fail_count = 0
            
            # 프레임 처리
            if frame is not None:
                processed_frame = frame_processor(frame)
                
                # 화면에 표시
                if not display_callback(processed_frame):
                    deactivate_callback()
                    break
        
        return True
    
    def set_max_consecutive_fails(self, max_fails: int) -> None:
        """
        최대 연속 실패 횟수 설정
        
        Args:
            max_fails: 최대 연속 실패 횟수
        """
        if max_fails > 0:
            self.max_consecutive_fails = max_fails
    
    def get_max_consecutive_fails(self) -> int:
        """최대 연속 실패 횟수 반환"""
        return self.max_consecutive_fails
