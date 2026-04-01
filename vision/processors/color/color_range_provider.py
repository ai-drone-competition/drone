"""
색상 범위 제공자
외부에서 전달받은 색상 설정을 관리
"""
import numpy as np
from typing import Dict, Optional


class ColorRangeProvider:
    """색상 범위를 외부에서 주입받아 관리하는 클래스"""
    
    def __init__(self, color_ranges: Optional[Dict[str, Dict[str, np.ndarray]]] = None):
        """
        ColorRangeProvider 초기화
        
        Args:
            color_ranges: 색상 범위 설정 딕셔너리
        """
        self._color_ranges: Dict[str, Dict[str, np.ndarray]] = color_ranges or {}
    
    def set_color_ranges(self, color_ranges: Dict[str, Dict[str, np.ndarray]]) -> None:
        """색상 범위 설정"""
        self._color_ranges = color_ranges
    
    def get_color_range(self, color_type: str) -> Optional[Dict[str, np.ndarray]]:
        """특정 색상 타입의 범위 반환"""
        return self._color_ranges.get(color_type)
    
    def has_color_range(self, color_type: str) -> bool:
        """특정 색상 타입의 범위가 존재하는지 확인"""
        return color_type in self._color_ranges
    
    def get_available_colors(self) -> list[str]:
        """사용 가능한 색상 타입 목록 반환"""
        return list(self._color_ranges.keys())
