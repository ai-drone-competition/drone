"""
감지 정보 시각화 도구
단일 책임: 감지된 정보를 프레임에 시각적으로 표시
"""
import cv2
import numpy as np
from typing import Tuple, Dict


class DetectionVisualizer:
    """감지 정보 시각화 전용 클래스"""
    
    def __init__(self):
        """DetectionVisualizer 초기화"""
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.5
        self.thickness = 1
    
    def draw_bounding_box(self, frame: np.ndarray, bbox: Tuple[int, int, int, int], 
                         color: Tuple[int, int, int] = (0, 255, 0), thickness: int = 2) -> np.ndarray:
        """
        바운딩 박스 그리기
        
        Args:
            frame: 입력 프레임
            bbox: 바운딩 박스 (x, y, w, h)
            color: 박스 색상 (B, G, R)
            thickness: 선 두께
            
        Returns:
            바운딩 박스가 그려진 프레임
        """
        x, y, w, h = bbox
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)
        return frame
    
    def draw_center_point(self, frame: np.ndarray, center: Tuple[int, int], 
                         color: Tuple[int, int, int] = (0, 0, 255), radius: int = 5) -> np.ndarray:
        """
        중심점 그리기
        
        Args:
            frame: 입력 프레임
            center: 중심점 (x, y)
            color: 점 색상 (B, G, R)
            radius: 점 반지름
            
        Returns:
            중심점이 그려진 프레임
        """
        cv2.circle(frame, center, radius, color, -1)
        return frame
    
    def draw_text_info(self, frame: np.ndarray, bbox: Tuple[int, int, int, int], 
                      center: Tuple[int, int], metrics: Dict[str, int], 
                      color: Tuple[int, int, int] = (0, 255, 0)) -> np.ndarray:
        """
        텍스트 정보 그리기
        
        Args:
            frame: 입력 프레임
            bbox: 바운딩 박스 (x, y, w, h)
            center: 객체 중심점 (x, y)
            metrics: 계산된 메트릭 딕셔너리
            color: 텍스트 색상 (B, G, R)
            
        Returns:
            텍스트 정보가 그려진 프레임
        """
        x, y, _, _ = bbox
        center_x, center_y = center
        
        # 각 정보를 순차적으로 표시
        texts = [
            f"Size: {metrics['width']}x{metrics['height']}px",
            f"Center: ({center_x}, {center_y})",
            f"HSV: ({metrics['hsv_h']}, {metrics['hsv_s']}, {metrics['hsv_v']})",
            f"Offset: ({metrics['offset_x']}, {metrics['offset_y']})",
            f"Distance: {metrics['distance']}px"
        ]
        
        for i, text in enumerate(texts):
            y_pos = y - 10 - (i * 20)
            cv2.putText(frame, text, (x, y_pos), self.font, self.font_scale, color, self.thickness)
        
        return frame
    
    def draw_crosshair(self, frame: np.ndarray, color: Tuple[int, int, int] = (255, 0, 0), 
                      thickness: int = 2) -> np.ndarray:
        """
        화면 중앙에 십자선 그리기
        
        Args:
            frame: 입력 프레임
            color: 십자선 색상 (B, G, R)
            thickness: 선 두께
            
        Returns:
            십자선이 그려진 프레임
        """
        height, width = frame.shape[:2]
        center_x, center_y = width // 2, height // 2
        
        # 중앙 십자선
        cv2.circle(frame, (center_x, center_y), 10, color, thickness)
        cv2.line(frame, (center_x-15, center_y), (center_x+15, center_y), color, thickness)
        cv2.line(frame, (center_x, center_y-15), (center_x, center_y+15), color, thickness)
        
        return frame
    
    def draw_all_detection_info(self, frame: np.ndarray, bbox: Tuple[int, int, int, int], 
                               center: Tuple[int, int], metrics: Dict[str, int]) -> np.ndarray:
        """
        모든 감지 정보를 한번에 그리기
        
        Args:
            frame: 입력 프레임
            bbox: 바운딩 박스 (x, y, w, h)
            center: 중심점 (x, y)
            metrics: 계산된 메트릭 딕셔너리
            
        Returns:
            모든 정보가 그려진 프레임
        """
        # 1. 바운딩 박스 그리기
        frame = self.draw_bounding_box(frame, bbox)
        
        # 2. 중심점 그리기
        frame = self.draw_center_point(frame, center)
        
        # 3. 텍스트 정보 그리기
        frame = self.draw_text_info(frame, bbox, center, metrics)
        
        # 4. 십자선 그리기
        frame = self.draw_crosshair(frame)
        
        return frame
    
    def draw_colored_detection_info(self, frame: np.ndarray, bbox: Tuple[int, int, int, int], 
                                  center: Tuple[int, int], metrics: Dict[str, int], color_name: str,
                                  box_color: Tuple[int, int, int], text_color: Tuple[int, int, int]) -> np.ndarray:
        """
        색상별로 구분된 감지 정보 시각화
        
        Args:
            frame: 입력 프레임
            bbox: 바운딩 박스
            center: 중심점
            metrics: 계산된 메트릭
            color_name: 색상 이름
            box_color: 바운딩 박스 색상
            text_color: 텍스트 색상
            
        Returns:
            시각화된 프레임
        """
        x, y, w, h = bbox
        cx, cy = center
        
        # 1. 바운딩 박스 그리기
        cv2.rectangle(frame, (x, y), (x + w, y + h), box_color, 2)
        
        # 2. 중심점 그리기
        cv2.circle(frame, center, 5, box_color, -1)
        
        # 3. 색상 이름 표시
        label = f"{color_name.upper()}"
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)
        
        # 4. 크기 정보 표시 (바운딩 박스 내부에)
        area_text = f"Area: {metrics.get('area', 0)}"
        cv2.putText(frame, area_text, (x + 5, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, text_color, 1)
        
        # 5. 좌표 정보 표시
        coord_text = f"({cx}, {cy})"
        cv2.putText(frame, coord_text, (x + 5, y + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.4, text_color, 1)
        
        return frame
