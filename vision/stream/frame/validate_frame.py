import numpy as np
from typing import Optional

def validate_frame(frame: Optional[np.ndarray]) -> bool:
    """
    프레임 유효성 검증
    
    Args:
        frame: 검증할 프레임
        
    Returns:
        프레임 유효성 여부
    """
    if frame is None:
        return False
    
    if frame.size == 0:
        return False
    
    if len(frame.shape) != 3:
        return False
    
    return True