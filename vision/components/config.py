"""
비전 설정 관리자
단일 책임: 비전 시스템의 모든 설정값 관리
"""
import numpy as np
from typing import List, Optional, Dict
from ..processors.color import ColorRangeProvider


class VisionConfig:
    """비전 시스템 설정 관리 클래스"""
    
    def __init__(self, min_area: int = 500, 
                 target_colors: Optional[List[str]] = None,
                 separate_color_mode: bool = False,
                 window_name: str = "Tello EDU Vision Detection",
                 debug_mode: bool = True,
                 color_ranges: Optional[Dict[str, Dict[str, np.ndarray]]] = None,
                 color_configs: Optional[Dict[str, Dict]] = None):
        """
        VisionConfig 초기화
        
        Args:
            min_area: 감지할 최소 객체 크기
            target_colors: 감지할 색상 목록, 기본값: ['environment']
            separate_color_mode: 색상별 개별 감지 모드
            window_name: OpenCV 창 이름
            debug_mode: 디버깅 모드 활성화 여부
            color_ranges: 색상 범위 설정 딕셔너리
            color_configs: 색상 설정 정보 딕셔너리 (시각화용)
        """
        if target_colors is None:
            target_colors = ['environment']
        
        self._min_area = min_area
        self._target_colors = target_colors
        self._separate_color_mode = separate_color_mode
        self._window_name = window_name
        self._debug_mode = debug_mode
        self._color_configs = color_configs or {}
        
        # 색상 범위 제공자 초기화
        self._color_range_provider = ColorRangeProvider(color_ranges)
        
        # 유효한 색상 목록 (색상 범위 제공자에서 가져옴)
        self._valid_colors = self._color_range_provider.get_available_colors()
    
    @property
    def min_area(self) -> int:
        """최소 감지 면적"""
        return self._min_area
    
    @min_area.setter
    def min_area(self, value: int) -> None:
        """최소 감지 면적 설정"""
        if value > 0:
            self._min_area = value
    
    @property
    def target_colors(self) -> List[str]:
        """감지 대상 색상 목록 (복사본 반환)"""
        return self._target_colors.copy()
    
    @target_colors.setter
    def target_colors(self, colors: List[str]) -> None:
        """감지 대상 색상 목록 설정"""
        filtered_colors = [color for color in colors if color in self._valid_colors]
        if filtered_colors:
            self._target_colors = filtered_colors
    
    @property
    def separate_color_mode(self) -> bool:
        """색상별 개별 감지 모드"""
        return self._separate_color_mode
    
    @separate_color_mode.setter
    def separate_color_mode(self, enabled: bool) -> None:
        """색상별 개별 감지 모드 설정"""
        self._separate_color_mode = enabled
    
    @property
    def window_name(self) -> str:
        """OpenCV 창 이름"""
        return self._window_name
    
    @window_name.setter
    def window_name(self, name: str) -> None:
        """OpenCV 창 이름 설정"""
        self._window_name = name
    
    @property
    def debug_mode(self) -> bool:
        """디버깅 모드"""
        return self._debug_mode
    
    @debug_mode.setter
    def debug_mode(self, enabled: bool) -> None:
        """디버깅 모드 설정"""
        self._debug_mode = enabled
    
    @property
    def color_range_provider(self) -> ColorRangeProvider:
        """색상 범위 제공자"""
        return self._color_range_provider
    
    @property
    def color_configs(self) -> Dict[str, Dict]:
        """색상 설정 정보"""
        return self._color_configs.copy()
    
    @property
    def valid_colors(self) -> List[str]:
        """지원되는 색상 목록 (읽기 전용)"""
        return self._valid_colors.copy()
    
    def is_multi_color_mode(self) -> bool:
        """다중 색상 감지 모드인지 확인"""
        return self._separate_color_mode and len(self._target_colors) > 1
    
    def validate_color(self, color: str) -> bool:
        """색상이 유효한지 확인"""
        return color in self._valid_colors
    
    def set_color_ranges(self, color_ranges: Dict[str, Dict[str, np.ndarray]]) -> None:
        """색상 범위 설정 업데이트"""
        self._color_range_provider.set_color_ranges(color_ranges)
        self._valid_colors = self._color_range_provider.get_available_colors()
    
    def reset_to_defaults(self) -> None:
        """기본값으로 재설정"""
        self._min_area = 500
        self._target_colors = ['environment']
        self._separate_color_mode = False
        self._debug_mode = True
