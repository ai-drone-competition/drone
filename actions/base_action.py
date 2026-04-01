"""
기본 동작 클래스의 베이스 클래스

모든 동작 클래스가 상속받아야 하는 기본 클래스입니다.
"""

from abc import ABC, abstractmethod
from typing import Any, Union

class BaseAction(ABC):
    """모든 동작의 기본 클래스"""
    
    def __init__(self, **kwargs: Any) -> None:
        """
        동작 초기화
        
        Args:
            **kwargs: 동작별 파라미터
        """
        self.params = kwargs
        
    @abstractmethod
    def execute(self, drone: Union[Any, Any]) -> bool:
        """
        동작 실행
        
        Args:
            drone: 실행할 드론 객체
            
        Returns:
            bool: 실행 성공 여부
        """
        pass
    
    @property
    def description(self) -> str:
        """동작 설명 반환"""
        return f"{self.__class__.__name__}({', '.join(f'{k}={v}' for k, v in self.params.items())})"
    
    def __str__(self) -> str:
        return self.description
    
    def __repr__(self) -> str:
        return self.description
