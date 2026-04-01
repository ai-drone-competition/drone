"""
연결 재시도 관리 모듈
연결 실패 시 재시도 로직 담당
"""
import time
from typing import Callable, Optional
from ..message import ConnectionMessageHandler
from .timeout_handler import ConnectionTimeoutHandler

class ConnectionRetryHandler:
    """드론 연결 재시도 관리 클래스"""
    
    @classmethod
    def retry_with_timeout(cls, connection_func: Callable, timeout_seconds: int = 13) -> Optional[object]:
        """
        재시도와 타임아웃을 모두 적용한 연결 시도
        
        Args:
            connection_func: 실행할 연결 함수
            timeout_seconds: 타임아웃 시간 (기본 13초)
        
        Returns:
            연결 결과 (성공 시 드론 객체, 실패 시 None)
        """
        return ConnectionTimeoutHandler.execute_with_timeout(connection_func, timeout_seconds)
    
    @classmethod
    def simple_retry(cls, connection_func: Callable, max_attempts: int = 3) -> Optional[object]:
        """
        간단한 재시도 (타임아웃 없음)
        
        Args:
            connection_func: 실행할 연결 함수
            max_attempts: 최대 시도 횟수
        
        Returns:
            연결 결과
        """
        ConnectionMessageHandler.print_connection_attempt_message_simple()
        
        for attempt in range(1, max_attempts + 1):
            try:
                result = connection_func()
                if result is not None:
                    ConnectionMessageHandler.print_success_message("connection")
                    return result
                else:
                    if attempt < max_attempts:
                        time.sleep(1)
                        continue
            except Exception as e:
                if attempt < max_attempts:
                    time.sleep(1)
                    continue
                else:
                    break
        
        return None
