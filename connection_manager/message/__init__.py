"""
연결 관리자 핸들러 모듈

연결 관련 에러 처리와 메시지 출력을 담당합니다.
"""

from .error import ConnectionErrorHandler
from .alert import ConnectionMessageHandler

# 하위 호환성을 위한 별칭
DroneErrorHandler = ConnectionErrorHandler
MessageHandler = ConnectionMessageHandler


