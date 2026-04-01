"""
연결 타임아웃 관리 모듈
연결 시도에 대한 시간 제한 및 카운트다운 기능
"""
import time
import threading
import queue
from typing import Callable, Optional
from constants import Colors

class ConnectionTimeoutHandler:
    """연결 타임아웃 관리 클래스"""
    
    @classmethod
    def execute_with_timeout(cls, connection_func: Callable, timeout_seconds: int = 13) -> Optional[object]:
        """
        타임아웃과 함께 연결 함수 실행
        
        Args:
            connection_func: 실행할 연결 함수
            timeout_seconds: 타임아웃 시간 (기본 13초)
        
        Returns:
            연결 결과 (성공 시 드론 객체, 실패 시 None)
        """
        print(f"{Colors.CYAN}🔍 드론 연결을 시도하는 중입니다...{Colors.END}")
        
        result_queue = queue.Queue()
        
        def connection_worker():
            """별도 스레드에서 연결 함수 실행"""
            try:
                start_time = time.time()
                result = connection_func()
                elapsed = time.time() - start_time
                result_queue.put(("success", result, elapsed))
            except Exception as e:
                result_queue.put(("error", e, 0))
        
        # 연결 스레드 시작
        connection_thread = threading.Thread(target=connection_worker)
        connection_thread.daemon = True
        connection_thread.start()
        
        # 메인 스레드에서 카운트다운
        for remaining in range(timeout_seconds, 0, -1):
            print(f"\r{Colors.YELLOW}연결 제한 시간: {Colors.RED}{Colors.BOLD}{remaining:2d}초 남음{Colors.END}", end="", flush=True)
            
            # 연결 결과 확인
            try:
                result_type, result_data, elapsed = result_queue.get(timeout=1)
                
                if result_type == "success":
                    if result_data is not None:
                        print(f"\n{Colors.GREEN}[성공] 드론 연결 성공! ({elapsed:.1f}초 소요){Colors.END}")
                        return result_data
                    else:
                        # 연결 함수에서 None 반환 (연결 실패)
                        break
                elif result_type == "error":
                    # 연결 함수에서 예외 발생
                    break
                    
            except queue.Empty:
                # 1초 동안 결과가 없으면 계속 카운트다운
                continue
        
        # 타임아웃 또는 연결 실패
        print(f"\n{Colors.RED}⏰ 연결 제한 시간이 초과되었습니다! (드론 자동 착륙 예상){Colors.END}")
        return None
