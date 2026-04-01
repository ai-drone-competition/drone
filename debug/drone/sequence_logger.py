"""
시퀀스 디버깅 로거
시퀀스 실행 정보를 파일로 저장하고 관리
"""

import logging
import os
from datetime import datetime
from typing import Optional
from constants import Colors

class SequenceDebugLogger:
    """시퀀스 디버깅 로그 관리 클래스"""
    
    _instance: Optional['SequenceDebugLogger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls) -> 'SequenceDebugLogger':
        """싱글톤 패턴 구현"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """로거 초기화"""
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self) -> None:
        """로거 설정"""
        # 로그 디렉토리 생성
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 날짜별 로그 파일명
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = os.path.join(log_dir, f"sequence_debug_{timestamp}.log")
        
        # 로거 생성
        self._logger = logging.getLogger("sequence_debug")
        self._logger.setLevel(logging.DEBUG)
        
        # 핸들러가 이미 있는 경우 제거 (중복 방지)
        if self._logger.handlers:
            self._logger.handlers.clear()
        
        # 파일 핸들러 생성
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # 포맷터 설정
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        # 핸들러 추가
        self._logger.addHandler(file_handler)
        
        print(f"{Colors.GREEN}📁 시퀀스 디버그 로그 파일: {log_file}{Colors.END}")
    
    def log_sequence_start(self, sequence_name: str) -> None:
        """시퀀스 시작 로그"""
        if self._logger:
            self._logger.info(f"[SEQUENCE] {sequence_name} - START")
    
    def log_sequence_end(self, sequence_name: str, execution_time: float, success: bool) -> None:
        """시퀀스 종료 로그"""
        if self._logger:
            status = "COMPLETED" if success else "FAILED"
            message = f"[SEQUENCE] {sequence_name} - {status} | TIME: {execution_time:.2f}s"
            
            if success:
                self._logger.info(message)
            else:
                self._logger.error(message)
    
    def log_action_step(self, sequence_name: str, step: int, total_steps: int, 
                       action_name: str, success: bool, execution_time: float = 0.0) -> None:
        """시퀀스 내 액션 단계 로그"""
        if self._logger:
            status = "SUCCESS" if success else "FAILED"
            message = f"[SEQUENCE] {sequence_name} - Step {step}/{total_steps}: {action_name} - {status}"
            
            if execution_time > 0:
                message += f" | TIME: {execution_time:.3f}s"
            
            if success:
                self._logger.info(message)
            else:
                self._logger.error(message)
    
    def log_custom(self, level: str, message: str) -> None:
        """
        커스텀 로그 기록
        
        Args:
            level: 로그 레벨 (debug, info, warning, error)
            message: 메시지
        """
        if self._logger:
            log_method = getattr(self._logger, level.lower(), self._logger.info)
            log_method(f"[SEQUENCE] {message}")
