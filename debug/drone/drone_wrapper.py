"""
드론 객체 래퍼 클래스
djitellopy Tello 객체를 감싸서 디버깅 기능을 자동으로 추가
"""

from typing import Any, Optional
from djitellopy import Tello
from .drone_decorators import debug_drone_method
from constants import Colors

class DebugDroneWrapper:
    """
    djitellopy Tello 객체를 감싸는 디버깅 래퍼 클래스
    중요한 드론 메서드 호출 시에만 디버깅 정보를 출력
    """
    
    def __init__(self, drone: Tello) -> None:
        """
        드론 래퍼 초기화
        
        Args:
            drone: djitellopy Tello 객체
        """
        self._drone = drone
        self._debug_enabled = True
        self._battery_shown = False  # 배터리 정보 표시 여부 추적
        self._height_calls = 0  # 고도 호출 횟수 추적
        
        # 디버깅이 필요한 주요 메서드들 (중요한 것들만)
        self._debug_methods = {
            # 기본 제어 (항상 표시)
            'takeoff': {'show_params': False, 'show_result': False, 'priority': 'high'},
            'land': {'show_params': False, 'show_result': False, 'priority': 'high'},
            'emergency': {'show_params': False, 'show_result': False, 'priority': 'high'},
            
            # 이동 명령 (중요한 이동만)
            'move_up': {'show_params': True, 'show_result': False, 'priority': 'medium'},
            'move_down': {'show_params': True, 'show_result': False, 'priority': 'medium'},
            'move_left': {'show_params': True, 'show_result': False, 'priority': 'medium'},
            'move_right': {'show_params': True, 'show_result': False, 'priority': 'medium'},
            'move_forward': {'show_params': True, 'show_result': False, 'priority': 'medium'},
            'move_back': {'show_params': True, 'show_result': False, 'priority': 'medium'},
            
            # 회전 명령 (중요한 회전만)
            'rotate_clockwise': {'show_params': True, 'show_result': False, 'priority': 'medium'},
            'rotate_counter_clockwise': {'show_params': True, 'show_result': False, 'priority': 'medium'},
            
            # RC 제어
            'send_rc_control': {'show_params': True, 'show_result': False, 'priority': 'low'},
            
            # 스트림 관련
            'streamon': {'show_params': False, 'show_result': False, 'priority': 'medium'},
            'streamoff': {'show_params': False, 'show_result': False, 'priority': 'medium'},
        }
        
        # 제한적으로 표시할 정보 조회 메서드들
        self._info_methods = {
            'get_battery': {'limit': 1, 'count': 0},  # 첫 번째만 표시
            'get_height': {'limit': 3, 'count': 0},   # 처음 3번만 표시
            'get_temperature': {'limit': 1, 'count': 0},
            'get_barometer': {'limit': 1, 'count': 0},
        }
    
    def set_debug_enabled(self, enabled: bool) -> None:
        """디버깅 활성화/비활성화"""
        self._debug_enabled = enabled
    
    def reset_counters(self) -> None:
        """카운터 초기화 (새로운 시퀀스 시작 시 사용)"""
        for method_info in self._info_methods.values():
            method_info['count'] = 0
        self._battery_shown = False
        self._height_calls = 0
    
    def show_initial_status(self) -> None:
        """초기 드론 상태 표시 (연결 직후 호출)"""
        if not self._debug_enabled:
            return
            
        try:
            battery = self._drone.get_battery()
            print(f"{Colors.GREEN}🔋 [초기상태] 배터리: {battery}%{Colors.END}")
            self._battery_shown = True
            self._info_methods['get_battery']['count'] = 1  # 이미 표시했음을 기록
        except Exception:
            pass  # 실패해도 무시
    
    def __getattr__(self, name: str) -> Any:
        """
        드론 객체의 속성/메서드에 대한 접근을 처리
        중요한 메서드만 디버깅하고, 정보 조회는 제한적으로 표시
        """
        attr = getattr(self._drone, name)
        
        # 메서드가 아니거나 디버깅이 비활성화된 경우 그대로 반환
        if not callable(attr) or not self._debug_enabled:
            return attr
        
        # 정보 조회 메서드 처리 (제한적 표시)
        if name in self._info_methods:
            info = self._info_methods[name]
            
            def limited_info_wrapper(*args, **kwargs):
                result = attr(*args, **kwargs)
                
                # 표시 횟수 제한 확인
                if info['count'] < info['limit']:
                    info['count'] += 1
                    
                    # 특별한 경우들 처리
                    if name == 'get_battery' and not self._battery_shown:
                        print(f"{Colors.CYAN}🔋 [DRONE] 배터리: {result}%{Colors.END}")
                        self._battery_shown = True
                    elif name == 'get_height':
                        self._height_calls += 1
                        if self._height_calls <= 2:  # 처음 2번만 표시
                            print(f"{Colors.CYAN}📏 [DRONE] 고도: {result}cm{Colors.END}")
                
                return result
            
            return limited_info_wrapper
        
        # 디버깅 대상 메서드인 경우 데코레이터 적용
        if name in self._debug_methods:
            debug_config = self._debug_methods[name]
            priority = debug_config.get('priority', 'medium')
            
            # 우선순위에 따라 표시 여부 결정
            if priority == 'low':
                return attr  # 낮은 우선순위는 표시하지 않음
            
            decorated_method = debug_drone_method(
                method_name=name,
                show_params=debug_config['show_params'],
                show_result=debug_config['show_result']
            )(attr)
            return decorated_method
        
        # 일반 메서드는 그대로 반환
        return attr
    
    def get_original_drone(self) -> Tello:
        """원본 드론 객체 반환"""
        return self._drone
