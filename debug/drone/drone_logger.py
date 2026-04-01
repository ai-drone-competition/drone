"""
드론 디버깅 로거
디버깅 정보를 파일로 저장하고 관리
"""

import logging
import os
from datetime import datetime
from typing import Optional
from constants import Colors

class DroneDebugLogger:
    """드론 디버깅 로그 관리 클래스"""
    
    _instance: Optional['DroneDebugLogger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls) -> 'DroneDebugLogger':
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
        log_file = os.path.join(log_dir, f"drone_debug_{timestamp}.log")
        
        # 로거 생성
        self._logger = logging.getLogger("drone_debug")
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
        
        print(f"{Colors.GREEN}📁 드론 디버그 로그 파일: {log_file}{Colors.END}")
    
    def log_drone_action(self, action: str, params: str = "", result: str = "", 
                        execution_time: float = 0.0, success: bool = True) -> None:
        """
        드론 액션 로그 기록
        
        Args:
            action: 액션명
            params: 매개변수
            result: 결과
            execution_time: 실행 시간
            success: 성공 여부
        """
        if self._logger:
            status = "SUCCESS" if success else "FAILED"
            message = f"[DRONE] {action}"
            
            if params:
                message += f" | PARAMS: {params}"
            if result:
                message += f" | RESULT: {result}"
            if execution_time > 0:
                message += f" | TIME: {execution_time:.3f}s"
            
            message += f" | STATUS: {status}"
            
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
            log_method(f"[DRONE] {message}")
