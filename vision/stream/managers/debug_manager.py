"""
디버깅 관리자
단일 책임: 디버깅 모드 및 디버거 관리
"""
from typing import Optional, Dict
from debug.vision import VisionDebugger


class DebugManager:
    """디버깅 관리 전용 클래스"""
    
    def __init__(self, debug_mode: bool = True, 
                 color_configs: Optional[Dict[str, Dict]] = None):
        """
        DebugManager 초기화
        
        Args:
            debug_mode: 디버깅 모드 활성화 여부
            color_configs: 색상별 통합 설정 (ENVIRONMENT_COLOR, TARGET_COLOR 형태)
        """
        self.debug_mode = debug_mode
        self.debugger: Optional[VisionDebugger] = None
        
        # 색상 관련 설정 저장
        self.color_configs = color_configs
        
        if self.debug_mode:
            self._create_debugger()
    
    def _create_debugger(self) -> None:
        """디버거 생성"""
        self.debugger = VisionDebugger(
            show_fps=True, 
            show_battery=True,
            color_configs=self.color_configs
        )
    
    def _destroy_debugger(self) -> None:
        """디버거 제거"""
        self.debugger = None
    
    def set_debug_mode(self, enabled: bool) -> None:
        """
        디버깅 모드 설정
        
        Args:
            enabled: 디버깅 모드 활성화 여부
        """
        self.debug_mode = enabled
        
        if enabled and self.debugger is None:
            self._create_debugger()
        elif not enabled and self.debugger is not None:
            self._destroy_debugger()
    
    def is_debug_mode(self) -> bool:
        """디버깅 모드 상태 확인"""
        return self.debug_mode
    
    def reset_counters(self) -> None:
        """디버깅 카운터 리셋"""
        if self.debugger:
            self.debugger.frame_count = 0
            self.debugger.fps_start_time = 0
    
    def get_debugger(self) -> Optional[VisionDebugger]:
        """디버거 인스턴스 반환"""
        return self.debugger
