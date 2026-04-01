import numpy as np
import cv2
import time
from typing import Optional


def get_processed_frame(drone, max_retries: int = 3, retry_delay: float = 0.1) -> Optional[np.ndarray]:
    """
    드론에서 프레임을 읽고 기본 처리
    
    Args:
        drone: 연결된 드론 객체
        max_retries: 최대 재시도 횟수
        retry_delay: 재시도 간 대기 시간 (초)
        
    Returns:
        처리된 BGR 프레임 또는 None
    """
    for attempt in range(max_retries + 1):
        try:
            frame_read = drone.get_frame_read()
            if frame_read is None:
                if attempt < max_retries:
                    time.sleep(retry_delay)
                    continue
                return None
            
            frame = frame_read.frame
            if frame is None:
                if attempt < max_retries:
                    time.sleep(retry_delay)
                    continue
                return None
            
            # 프레임 크기 검증
            if frame.size == 0 or len(frame.shape) != 3:
                if attempt < max_retries:
                    time.sleep(retry_delay)
                    continue
                return None
            
            # RGB를 BGR로 변환 (OpenCV 호환성)
            return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
        except Exception as e:
            if attempt < max_retries:
                print(f"프레임 읽기 실패 (시도 {attempt + 1}/{max_retries + 1}): {e}")
                time.sleep(retry_delay)
                continue
            else:
                print(f"프레임 읽기 최종 실패: {e}")
                return None
    
    return None