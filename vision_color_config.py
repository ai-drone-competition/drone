"""
비전 시스템 색상 설정 상수
다양한 색상의 HSV 범위 및 시각화 설정
"""
import numpy as np
from typing import Dict

# ======================================
# 색상별 HSV 범위 및 표시 설정
# ======================================

RED_COLOR = {
    # HSV 감지 범위 (빨간색은 2개 범위 필요)
    'hsv_ranges': {
        'lower_range1': np.array([0, 50, 50]),      # H: 0, S: 50, V: 50
        'upper_range1': np.array([10, 255, 255]),   # H: 10, S: 255, V: 255
        'lower_range2': np.array([170, 50, 50]),    # H: 170, S: 50, V: 50
        'upper_range2': np.array([180, 255, 255])   # H: 180, S: 255, V: 255
    },
    # 시각화 설정
    'display_name': 'Red',
    'bgr_color': (0, 0, 255),  # 빨간색
    'debug_text': 'RED'
}

WHITE_COLOR = {
    # HSV 감지 범위 (하얀색)
    'hsv_ranges': {
        'lower_range': np.array([0, 0, 200]),       # H: 0, S: 0, V: 200
        'upper_range': np.array([180, 30, 255])     # H: 180, S: 30, V: 255
    },
    # 시각화 설정
    'display_name': 'White',
    'bgr_color': (255, 255, 255),  # 하얀색
    'debug_text': 'WHITE'
}

BLUE_COLOR = {
    # HSV 감지 범위 (파란색)
    'hsv_ranges': {
        'lower_range': np.array([100, 50, 50]),     # H: 100, S: 50, V: 50
        'upper_range': np.array([130, 255, 255])    # H: 130, S: 255, V: 255
    },
    # 시각화 설정
    'display_name': 'Blue',
    'bgr_color': (255, 0, 0),  # 파란색 (BGR 순서)
    'debug_text': 'BLUE'
}

BLACK_COLOR = {
    # HSV 감지 범위 (검은색)
    'hsv_ranges': {
        'lower_range': np.array([0, 0, 0]),         # H: 0, S: 0, V: 0
        'upper_range': np.array([180, 255, 50])     # H: 180, S: 255, V: 50
    },
    # 시각화 설정
    'display_name': 'Black',
    'bgr_color': (128, 128, 128),  # 회색으로 표시 (검은색은 보이지 않으므로)
    'debug_text': 'BLACK'
}

# ======================================
# 색상 설정 딕셔너리
# ======================================

COLOR_CONFIGS = {
    'red': RED_COLOR,
    'white': WHITE_COLOR,
    'blue': BLUE_COLOR,
    'black': BLACK_COLOR,
    'environment': RED_COLOR,  # 기본 배경색
    'target': WHITE_COLOR      # 기본 목표색
}

# ======================================
# 기본 시스템 설정
# ======================================

# 기본 감지 최소 영역 크기
DEFAULT_MIN_AREA: int = 500
