"""
연결 관련 에러 처리 모듈
드론 연결, 해제, 연결 모니터링 관련 에러만 처리합니다
"""
from constants import Colors

class ConnectionErrorHandler:
    """연결 관련 에러 처리 전용 클래스"""
    
    @classmethod
    def handle_connection_error(cls, error: Exception) -> None:
        """드론 연결 에러 처리"""
        print(f"{Colors.RED}[연결 오류] 드론 연결에 실패했습니다.{Colors.END}")
        print(f"{Colors.CYAN}[해결 방법] 다음 사항을 확인하세요:{Colors.END}")
        print(f"  {Colors.CYAN}• 드론의 전원이 켜져 있는지 확인{Colors.END}")
        print(f"  {Colors.CYAN}• WiFi 연결 상태 확인{Colors.END}")
        print(f"  {Colors.CYAN}• 드론과의 통신 상태 확인{Colors.END}")
        print(f"  {Colors.CYAN}• 드론이 연결 가능한 범위 내에 있는지 확인{Colors.END}")
    
    @classmethod
    def handle_disconnection_error(cls, error: Exception) -> None:
        """드론 해제 에러 처리"""
        print(f"{Colors.RED}[해제 오류] 드론 연결 해제 중 문제가 발생했습니다: {error}{Colors.END}")
    
    @classmethod
    def handle_operation_error(cls, error: Exception, operation: str = "작업") -> None:
        """드론 작업 중 에러 처리"""
        print(f"{Colors.RED}[작업 오류] {operation} 중 오류가 발생했습니다: {error}{Colors.END}")
    
    @classmethod
    def print_warning_message(cls, message: str) -> None:
        """경고 메시지 출력"""
        print(f"{Colors.YELLOW}[경고] {message}{Colors.END}")

