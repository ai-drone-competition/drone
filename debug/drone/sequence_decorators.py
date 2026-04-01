"""
시퀀스 디버깅 데코레이터
시퀀스 실행 시 자동으로 디버깅 정보를 출력
"""

import functools
import time
from typing import Any, Callable
from constants import Colors

def debug_sequence(sequence_name: str = ""):
    """
    시퀀스 실행을 디버깅하는 데코레이터
    
    Args:
        sequence_name: 표시할 시퀀스명
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 시퀀스명 결정
            if sequence_name:
                display_name = sequence_name
            elif hasattr(args[0], 'name'):
                display_name = args[0].name
            else:
                display_name = func.__name__
            
            print(f"{Colors.BLUE}🎯 [SEQUENCE] {display_name} 시작{Colors.END}")
            print(f"{Colors.BLUE}{'='*50}{Colors.END}")
            
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                
                execution_time = time.time() - start_time
                print(f"{Colors.BLUE}{'='*50}{Colors.END}")
                print(f"{Colors.GREEN}🎉 [SEQUENCE] {display_name} 완료 (총 {execution_time:.2f}s){Colors.END}")
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                print(f"{Colors.BLUE}{'='*50}{Colors.END}")
                print(f"{Colors.RED}💥 [SEQUENCE] {display_name} 실패 ({execution_time:.2f}s): {str(e)}{Colors.END}")
                raise
                
        return wrapper
    return decorator
