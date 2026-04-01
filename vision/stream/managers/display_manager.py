"""
Display 관리자
단일 책임: OpenCV 창 및 프레임 표시 관리
"""
import cv2
import numpy as np


class DisplayManager:
    """Display 관리 전용 클래스"""
    
    def __init__(self, window_name: str = "Vision Stream"):
        """
        DisplayManager 초기화
        
        Args:
            window_name: OpenCV 창 이름
        """
        self.window_name = window_name
        self.window_created = False
    
    def create_window(self) -> None:
        """OpenCV 창 생성"""
        if not self.window_created:
            cv2.namedWindow(self.window_name, cv2.WINDOW_AUTOSIZE)
            self.window_created = True
    
    def display_frame(self, frame: np.ndarray) -> bool:
        """
        프레임을 화면에 표시
        
        Args:
            frame: 표시할 프레임
            
        Returns:
            창이 열려있는지 여부
        """
        if not self.window_created:
            self.create_window()
        
        cv2.imshow(self.window_name, frame)
        
        # OpenCV 창이 닫혔는지 확인
        if cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE) < 1:
            return False
        
        cv2.waitKey(1)
        return True
    
    def close_all_windows(self) -> None:
        """모든 OpenCV 창 닫기"""
        cv2.destroyAllWindows()
        self.window_created = False
    
    def is_window_created(self) -> bool:
        """창 생성 상태 확인"""
        return self.window_created
    
    def set_window_name(self, name: str) -> None:
        """
        창 이름 변경
        
        Args:
            name: 새로운 창 이름
        """
        if not self.window_created:
            self.window_name = name
