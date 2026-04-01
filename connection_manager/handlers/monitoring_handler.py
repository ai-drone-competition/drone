"""
연결 모니터링 및 자동 재연결 관리 모듈
드론 연결 상태를 모니터링하고 끊어졌을 때 자동 재연결
"""
import time
import threading
from typing import List, Optional
from constants import Colors
from .connection_handler import DroneConnectionManager
from .retry_handler import ConnectionRetryHandler
from .vps_management_handler import VPSManagementHandler

class TaskState:
    """작업 상태 관리"""
    def __init__(self):
        self.completed_tasks: List[str] = []
        self.current_task: Optional[str] = None
        self.remaining_tasks: List[tuple] = []  # (task_name, task_func, args, kwargs)

class ConnectionMonitoringHandler:
    """드론 연결 모니터링 및 재연결 관리"""
    
    _monitoring = False
    _monitor_thread = None
    _task_state = None
    
    @classmethod
    def start_monitoring(cls, task_state: TaskState):
        """연결 모니터링 시작"""
        cls._task_state = task_state
        cls._monitoring = True
        
        cls._monitor_thread = threading.Thread(target=cls._monitor_connection)
        cls._monitor_thread.daemon = True
        cls._monitor_thread.start()
        
        print(f"{Colors.BLUE}[모니터링] 드론 연결 상태 모니터링을 시작합니다{Colors.END}")
    
    @classmethod
    def stop_monitoring(cls):
        """연결 모니터링 중지"""
        cls._monitoring = False
        if cls._monitor_thread:
            cls._monitor_thread.join(timeout=1)
        print(f"{Colors.BLUE}[모니터링] 드론 연결 상태 모니터링을 중지합니다{Colors.END}")
    
    @classmethod
    def _monitor_connection(cls):
        """연결 상태 모니터링 (별도 스레드)"""
        while cls._monitoring:
            try:
                drone = DroneConnectionManager.get_drone()
                if drone:
                    # 간단한 상태 확인 명령 (배터리 조회)
                    battery = drone.get_battery()
                    # 연결이 정상이면 계속 모니터링
                    time.sleep(2)  # 2초마다 확인
                else:
                    # 드론 객체가 없으면 연결 끊김
                    cls._handle_disconnection()
                    break
            except Exception as e:
                # 명령 실행 실패 = 연결 끊김
                cls._handle_disconnection()
                break
    
    @classmethod
    def _handle_disconnection(cls):
        """연결 끊김 처리 및 재연결"""
        print(f"\n{Colors.RED}🚨 드론 연결이 끊어졌습니다!{Colors.END}")
        print(f"{Colors.YELLOW}⏸️  현재 작업을 일시 중단하고 재연결을 시도합니다...{Colors.END}")
        
        # VPS 연결 끊김 처리
        VPSManagementHandler.handle_connection_loss()
        
        # 재연결 시도
        drone = ConnectionRetryHandler.retry_with_timeout(DroneConnectionManager.connect, 13)
        
        if drone:
            print(f"{Colors.GREEN}🔄 재연결 성공! 중단된 작업을 이어서 실행합니다{Colors.END}")
            
            # VPS 관련 상태 복원
            VPSManagementHandler.restore_after_reconnection()
            
            # 모니터링 재시작 (task_state가 None이 아닌 경우에만)
            if cls._task_state is not None:
                cls.start_monitoring(cls._task_state)
        else:
            print(f"{Colors.RED}❌ 재연결 실패. 작업을 중단합니다{Colors.END}")
            cls._monitoring = False
