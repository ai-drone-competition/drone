"""
연결 관련 메시지 모듈
연결 작업 진행 상황 및 정보 안내 메시지를 처리합니다
"""

from constants import Colors

class ConnectionMessageHandler:
    """연결 관련 메시지 처리 클래스"""
    
    @classmethod
    def print_success_message(cls, operation: str) -> None:
        """성공 메시지 출력"""
        success_messages = {
            "connection": "드론 연결 성공!",
            "disconnection": "드론 연결 해제 완료",
            "reconnection": "드론 재연결 성공!"
        }
        
        message = success_messages.get(operation, f"{operation} 완료")
        print(f"{Colors.GREEN}[성공] {message}{Colors.END}")
    
    @classmethod
    def print_info_message(cls, message: str) -> None:
        """정보 메시지 출력"""
        print(f"{Colors.BLUE}[정보] {message}{Colors.END}")
    
    @classmethod
    def print_work_start_message(cls) -> None:
        """작업 시작 메시지 출력"""
        print(f"{Colors.BOLD}{Colors.PURPLE}{'=' * 50}")
        print("🚁 드론 작업이 시작되었습니다!")
        print(f"{'=' * 50}{Colors.END}")
    
    @classmethod
    def print_connection_attempt_message_simple(cls) -> None:
        """간단한 드론 연결 시도 메시지"""
        print(f"{Colors.CYAN}🔍 드론 연결을 시도하는 중입니다...{Colors.END}")
    
    @classmethod
    def print_work_end_message(cls) -> None:
        """작업 완료 메시지 출력"""
        print(f"{Colors.BOLD}{Colors.GREEN}{'=' * 50}")
        print("✅ 모든 드론 작업이 완료되었습니다!")
        print(f"{'=' * 50}{Colors.END}")

