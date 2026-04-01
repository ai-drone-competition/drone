"""
드론 디버깅 데코레이터
드론 메서드 호출 시 자동으로 디버깅 정보를 출력
"""

import functools
import time
from typing import Any, Callable
from constants import Colors

def debug_drone_method(method_name: str = "", show_params: bool = True, show_result: bool = False):
    """
    드론 메서드 실행을 디버깅하는 데코레이터
    
    Args:
        method_name: 표시할 메서드명 (기본값: 함수명)
        show_params: 매개변수 표시 여부
        show_result: 반환값 표시 여부
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 메서드명 결정
            display_name = method_name or func.__name__
            
            # 매개변수 정보
            param_info = ""
            if show_params and (args[1:] or kwargs):  # args[0]은 self이므로 제외
                params = []
                if args[1:]:
                    params.extend([str(arg) for arg in args[1:]])
                if kwargs:
                    params.extend([f"{k}={v}" for k, v in kwargs.items()])
                param_info = f"({', '.join(params)})"
            
            print(f"{Colors.CYAN}🚁 [DRONE] {display_name}{param_info} 실행 중...{Colors.END}")
            
            # 실행 시간 측정
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                
                # 실행 시간 계산
                execution_time = time.time() - start_time
                
                # 결과 표시
                result_info = ""
                if show_result and result is not None:
                    result_info = f" → {result}"
                
                print(f"{Colors.GREEN}✅ [DRONE] {display_name} 완료 ({execution_time:.3f}s){result_info}{Colors.END}")
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                print(f"{Colors.RED}❌ [DRONE] {display_name} 실패 ({execution_time:.3f}s): {str(e)}{Colors.END}")
                raise
                
        return wrapper
    return decorator
