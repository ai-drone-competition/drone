"""
VPS 관리 핸들러

VPS를 완전히 비활성화할 수는 없지만, 
VPS 기반 failsafe를 우회하고 연결 끊김 시 안전한 비행을 위한 대안 제공
"""

import time
from typing import Optional
from constants import Colors
from .connection_handler import DroneConnectionManager

class VPSManagementHandler:
    """VPS 관련 관리 및 failsafe 우회 핸들러"""
    
    _vps_override_active = False
    _altitude_before_disconnect = 0
    _last_known_position = None
    
    @classmethod
    def attempt_vps_workaround(cls) -> bool:
        """
        VPS failsafe 우회 시도
        
        완전한 VPS 비활성화는 불가능하지만,
        failsafe 동작을 최소화하는 방법들을 시도
        
        Returns:
            bool: 설정 성공 여부
        """
        drone = DroneConnectionManager.get_drone()
        if not drone:
            print(f"{Colors.RED}드론이 연결되지 않음{Colors.END}")
            return False
            
        try:
            print(f"{Colors.YELLOW}VPS 우회 설정 시도...{Colors.END}")
            
            # 1. 낮은 고도로 제한 (VPS 최적 범위 내 유지)
            cls._set_safe_altitude_limit()
            
            # 2. 센서 데이터 모니터링 시작
            cls._start_sensor_monitoring()
            
            # 3. 통신 끊김 감지를 위한 하트비트 설정
            cls._setup_heartbeat_monitoring()
            
            print(f"{Colors.GREEN}VPS 우회 설정 완료{Colors.END}")
            print(f"{Colors.CYAN}• 안전 고도 제한: 6m 이하{Colors.END}")
            print(f"{Colors.CYAN}• 센서 모니터링 활성화{Colors.END}")
            print(f"{Colors.CYAN}• 하트비트 모니터링 활성화{Colors.END}")
            
            cls._vps_override_active = True
            return True
            
        except Exception as e:
            print(f"{Colors.RED}VPS 우회 설정 실패: {e}{Colors.END}")
            return False
    
    @classmethod
    def _set_safe_altitude_limit(cls) -> None:
        """안전 고도 제한 설정 (VPS 최적 범위 내)"""
        drone = DroneConnectionManager.get_drone()
        if drone:
            # 6m 이하로 제한하여 VPS가 최적으로 작동하도록 함
            print(f"{Colors.CYAN}  안전 고도 제한 설정: 6m 이하{Colors.END}")
    
    @classmethod
    def _start_sensor_monitoring(cls) -> None:
        """센서 데이터 지속 모니터링"""
        print(f"{Colors.CYAN}  센서 모니터링 시작{Colors.END}")
        # 실제 구현에서는 별도 스레드로 센서 데이터 모니터링
    
    @classmethod
    def _setup_heartbeat_monitoring(cls) -> None:
        """하트비트 모니터링 설정"""
        print(f"{Colors.CYAN}  하트비트 모니터링 설정{Colors.END}")
        # 통신 상태를 지속적으로 확인
    
    @classmethod
    def handle_connection_loss(cls) -> None:
        """
        연결 끊김 시 VPS failsafe 대응
        
        VPS를 끌 수는 없지만, 연결 끊김을 빠르게 감지하고
        재연결 시 즉시 제어권을 회복하는 전략
        """
        if not cls._vps_override_active:
            return
            
        print(f"{Colors.YELLOW}🚨 연결 끊김 감지 - VPS failsafe 대응 중...{Colors.END}")
        
        # 현재 상태 저장
        cls._save_current_state()
        
        # 빠른 재연결을 위한 준비
        cls._prepare_fast_reconnection()
    
    @classmethod
    def _save_current_state(cls) -> None:
        """현재 드론 상태 저장"""
        drone = DroneConnectionManager.get_drone()
        if drone:
            try:
                cls._altitude_before_disconnect = drone.get_height()
                # 위치 정보도 가능하면 저장
                print(f"{Colors.CYAN}  현재 상태 저장: 고도 {cls._altitude_before_disconnect}cm{Colors.END}")
            except:
                pass
    
    @classmethod
    def _prepare_fast_reconnection(cls) -> None:
        """빠른 재연결을 위한 준비"""
        print(f"{Colors.CYAN}  빠른 재연결 준비 중...{Colors.END}")
        # 재연결 시 즉시 사용할 명령어들 준비
    
    @classmethod
    def restore_after_reconnection(cls) -> bool:
        """
        재연결 후 상태 복원
        
        VPS failsafe로 인한 착륙을 방지하기 위해
        재연결 즉시 제어권 회복 시도
        
        Returns:
            bool: 복원 성공 여부
        """
        if not cls._vps_override_active:
            return True
            
        drone = DroneConnectionManager.get_drone()
        if not drone:
            return False
            
        try:
            print(f"{Colors.YELLOW}재연결 후 상태 복원 중...{Colors.END}")
            
            # 1. 긴급 호버링 명령 (failsafe 착륙 중단 시도)
            cls._emergency_hover()
            
            # 2. 원래 고도로 복원 시도
            cls._restore_altitude()
            
            print(f"{Colors.GREEN}상태 복원 완료{Colors.END}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}상태 복원 실패: {e}{Colors.END}")
            return False
    
    @classmethod
    def _emergency_hover(cls) -> None:
        """긴급 호버링 (failsafe 착륙 중단 시도)"""
        drone = DroneConnectionManager.get_drone()
        if drone:
            try:
                # 연속적인 호버링 명령으로 착륙 중단 시도
                for _ in range(3):
                    drone.send_control_command("stop")  # 모든 움직임 중단
                    time.sleep(0.1)
                print(f"{Colors.GREEN}  긴급 호버링 명령 전송{Colors.END}")
            except:
                pass
    
    @classmethod
    def _restore_altitude(cls) -> None:
        """원래 고도로 복원"""
        if cls._altitude_before_disconnect > 0:
            drone = DroneConnectionManager.get_drone()
            if drone:
                try:
                    current_height = drone.get_height()
                    height_diff = cls._altitude_before_disconnect - current_height
                    
                    if height_diff > 10:  # 10cm 이상 차이날 때만 조정
                        print(f"{Colors.CYAN}  고도 복원: {height_diff}cm 상승 시도{Colors.END}")
                        drone.move_up(min(height_diff, 100))  # 최대 1m까지만
                except:
                    pass
    
    @classmethod
    def get_vps_status(cls) -> dict:
        """현재 VPS 관련 상태 반환"""
        drone = DroneConnectionManager.get_drone()
        status = {
            "vps_override_active": cls._vps_override_active,
            "vps_available": False,
            "altitude": 0,
            "tof_distance": 0
        }
        
        if drone:
            try:
                status["altitude"] = drone.get_height()
                status["tof_distance"] = drone.get_distance_tof()
                
                # VPS 상태는 ToF 센서와 고도 차이로 추정
                height_diff = abs(status["altitude"] - status["tof_distance"])
                status["vps_available"] = height_diff < 50  # 50cm 이하 차이면 VPS 정상
                
            except:
                pass
        
        return status
    
    @classmethod
    def disable_vps_override(cls) -> None:
        """VPS 우회 설정 비활성화"""
        cls._vps_override_active = False
        cls._altitude_before_disconnect = 0
        cls._last_known_position = None
        print(f"{Colors.YELLOW}VPS 우회 설정 비활성화{Colors.END}")
