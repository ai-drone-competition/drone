"""
비전 시스템 디버깅 클래스
OpenCV 처리 과정의 시각화 및 정보 표시 담당
"""
import cv2
import numpy as np
from typing import Tuple, Optional, Dict
from constants import Colors


class VisionDebugger:
    """비전 시스템 디버깅 및 시각화 클래스"""
    
    def __init__(self, show_fps: bool = True, show_battery: bool = True, 
                 color_configs: Optional[Dict[str, Dict]] = None):
        """
        VisionDebugger 초기화
        
        Args:
            show_fps: FPS 표시 여부
            show_battery: 배터리 표시 여부
            color_configs: 색상별 통합 설정 (ENVIRONMENT_COLOR, TARGET_COLOR 형태)
        """
        self.show_fps = show_fps
        self.show_battery = show_battery
        self.frame_count = 0
        self.fps_start_time = 0
        self.current_fps = 0.0
        
        # 색상 관련 설정 저장
        self.color_configs = color_configs or {}
        
        # 기본 색상 설정
        self.default_color = (0, 255, 0)  # 기본 초록색
        
    def draw_crosshair(self, frame: np.ndarray, color: Tuple[int, int, int] = (255, 0, 0), 
                      size: int = 15, thickness: int = 2) -> np.ndarray:
        """
        화면 중앙에 십자선 그리기
        
        Args:
            frame: 입력 프레임
            color: 십자선 색상 (B, G, R)
            size: 십자선 크기
            thickness: 선 두께
            
        Returns:
            십자선이 그려진 프레임
        """
        height, width = frame.shape[:2]
        center_x, center_y = width // 2, height // 2
        
        # 중앙 원
        cv2.circle(frame, (center_x, center_y), 10, color, thickness)
        
        # 십자선
        cv2.line(frame, (center_x - size, center_y), (center_x + size, center_y), color, thickness)
        cv2.line(frame, (center_x, center_y - size), (center_x, center_y + size), color, thickness)
        
        return frame
    
    def draw_detection_box(self, frame: np.ndarray, bbox: Tuple[int, int, int, int], 
                          color: Tuple[int, int, int] = (0, 255, 0), thickness: int = 2) -> np.ndarray:
        """
        감지된 객체 바운딩 박스 그리기
        
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
                         color: Tuple[int, int, int] = (255, 0, 0), radius: int = 5) -> np.ndarray:
        """
        중심점 그리기
        
        Args:
            frame: 입력 프레임
            center: 중심점 좌표 (x, y)
            color: 점 색상 (B, G, R)
            radius: 점 크기
            
        Returns:
            중심점이 그려진 프레임
        """
        cv2.circle(frame, center, radius, color, -1)
        return frame
    
    def draw_text_info(self, frame: np.ndarray, text: str, position: Tuple[int, int], 
                      color: Tuple[int, int, int] = (0, 255, 0), font_scale: float = 0.5, 
                      thickness: int = 1) -> np.ndarray:
        """
        텍스트 정보 그리기
        
        Args:
            frame: 입력 프레임
            text: 표시할 텍스트
            position: 텍스트 위치 (x, y)
            color: 텍스트 색상 (B, G, R)
            font_scale: 폰트 크기
            thickness: 텍스트 두께
            
        Returns:
            텍스트가 그려진 프레임
        """
        cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)
        return frame
    
    def draw_color_detection_info(self, frame: np.ndarray, bbox: Tuple[int, int, int, int], 
                                 center: Tuple[int, int], area: float, color_type: str) -> np.ndarray:
        """
        색상별 객체 감지 정보 종합 표시
        
        Args:
            frame: 입력 프레임
            bbox: 바운딩 박스 (x, y, w, h)
            center: 중심점 (x, y)
            area: 객체 영역 크기
            color_type: 색상 타입 ('environment', 'target' 등)
            
        Returns:
            정보가 표시된 프레임
        """
        x, y, w, h = bbox
        center_x, center_y = center
        
        # 색상 설정에서 정보 가져오기 (안전하게)
        color_config = self.color_configs.get(color_type, {})
        display_color = color_config.get('bgr_color', self.default_color)
        display_name = color_config.get('display_name', color_type.upper())
        debug_text = color_config.get('debug_text', color_type.upper())
        
        # 바운딩 박스 그리기 (색상별)
        frame = self.draw_detection_box(frame, bbox, display_color)
        
        # 중심점 그리기 (색상별)
        frame = self.draw_center_point(frame, center, display_color)
        
        # 기본 정보 표시
        frame = self.draw_text_info(frame, f"{display_name} [{debug_text}]", (x, y - 10), display_color)
        frame = self.draw_text_info(frame, f"Area: {int(area)}", (x, y - 30), display_color)
        frame = self.draw_text_info(frame, f"Center: ({center_x}, {center_y})", (x, y - 50), display_color)
        
        # 화면 중앙과의 오프셋 계산 및 표시
        height, width = frame.shape[:2]
        screen_center_x, screen_center_y = width // 2, height // 2
        offset_x = center_x - screen_center_x
        offset_y = center_y - screen_center_y
        distance = int(np.sqrt(offset_x**2 + offset_y**2))
        
        frame = self.draw_text_info(frame, f"Offset: ({offset_x}, {offset_y})", (x, y - 70), display_color)
        frame = self.draw_text_info(frame, f"Distance: {distance}px", (x, y - 90), display_color)
        
        return frame
    
    def draw_detection_info(self, frame: np.ndarray, bbox: Tuple[int, int, int, int], 
                           center: Tuple[int, int], area: float) -> np.ndarray:
        """
        객체 감지 정보 종합 표시
        
        Args:
            frame: 입력 프레임
            bbox: 바운딩 박스 (x, y, w, h)
            center: 중심점 (x, y)
            area: 객체 영역 크기
            
        Returns:
            정보가 표시된 프레임
        """
        x, y, w, h = bbox
        center_x, center_y = center
        
        # 바운딩 박스 그리기
        frame = self.draw_detection_box(frame, bbox)
        
        # 중심점 그리기
        frame = self.draw_center_point(frame, center)
        
        # 기본 정보 표시
        frame = self.draw_text_info(frame, f"Area: {int(area)}", (x, y - 10))
        frame = self.draw_text_info(frame, f"Center: ({center_x}, {center_y})", (x, y - 30))
        
        # 화면 중앙과의 오프셋 계산 및 표시
        height, width = frame.shape[:2]
        screen_center_x, screen_center_y = width // 2, height // 2
        offset_x = center_x - screen_center_x
        offset_y = center_y - screen_center_y
        distance = int(np.sqrt(offset_x**2 + offset_y**2))
        
        frame = self.draw_text_info(frame, f"Offset: ({offset_x}, {offset_y})", (x, y - 50))
        frame = self.draw_text_info(frame, f"Distance: {distance}px", (x, y - 70))
        
        return frame
    
    def draw_drone_status(self, frame: np.ndarray, drone, position: Tuple[int, int] = (10, 30)) -> np.ndarray:
        """
        드론 상태 정보 표시
        
        Args:
            frame: 입력 프레임
            drone: 드론 객체
            position: 표시 위치 (x, y)
            
        Returns:
            상태 정보가 표시된 프레임
        """
        if not self.show_battery:
            return frame
            
        try:
            battery = drone.get_battery()
            # 배터리 색상 설정 (낮으면 빨간색)
            battery_color = (0, 255, 0) if battery > 30 else (0, 165, 255) if battery > 15 else (0, 0, 255)
            
            frame = self.draw_text_info(
                frame, f"Battery: {battery}%", position, 
                color=battery_color, font_scale=0.7, thickness=2
            )
        except Exception:
            frame = self.draw_text_info(
                frame, "Battery: N/A", position, 
                color=(0, 0, 255), font_scale=0.7, thickness=2
            )
        
        return frame
    
    def calculate_fps(self) -> float:
        """
        FPS 계산
        
        Returns:
            현재 FPS 값
        """
        import time
        
        self.frame_count += 1
        if self.frame_count == 1:
            self.fps_start_time = time.time()
        elif self.frame_count >= 30:  # 30프레임마다 FPS 계산
            current_time = time.time()
            elapsed = current_time - self.fps_start_time
            self.current_fps = self.frame_count / elapsed
            self.frame_count = 0
        
        return self.current_fps
    
    def draw_fps(self, frame: np.ndarray, position: Tuple[int, int] = (10, 60)) -> np.ndarray:
        """
        FPS 정보 표시
        
        Args:
            frame: 입력 프레임
            position: 표시 위치 (x, y)
            
        Returns:
            FPS가 표시된 프레임
        """
        if not self.show_fps:
            return frame
            
        fps = self.calculate_fps()
        # FPS 색상 설정 (낮으면 빨간색)
        fps_color = (0, 255, 0) if fps > 20 else (0, 165, 255) if fps > 10 else (0, 0, 255)
        
        frame = self.draw_text_info(
            frame, f"FPS: {fps:.1f}", position, 
            color=fps_color, font_scale=0.6, thickness=2
        )
        
        return frame
    
    def draw_debug_grid(self, frame: np.ndarray, grid_size: int = 50, 
                       color: Tuple[int, int, int] = (100, 100, 100)) -> np.ndarray:
        """
        디버깅용 격자 그리기
        
        Args:
            frame: 입력 프레임
            grid_size: 격자 크기
            color: 격자 색상 (B, G, R)
            
        Returns:
            격자가 그려진 프레임
        """
        height, width = frame.shape[:2]
        
        # 세로선
        for x in range(0, width, grid_size):
            cv2.line(frame, (x, 0), (x, height), color, 1)
        
        # 가로선
        for y in range(0, height, grid_size):
            cv2.line(frame, (0, y), (width, y), color, 1)
        
        return frame
    
    def add_debug_overlay(self, frame: np.ndarray, drone = None, 
                         detected: bool = False, bbox: Optional[Tuple[int, int, int, int]] = None, 
                         center: Optional[Tuple[int, int]] = None, area: float = 0) -> np.ndarray:
        """
        모든 디버깅 정보를 프레임에 추가
        
        Args:
            frame: 입력 프레임
            drone: 드론 객체
            detected: 객체 감지 여부
            bbox: 바운딩 박스
            center: 중심점
            area: 객체 영역 크기
            
        Returns:
            모든 디버깅 정보가 추가된 프레임
        """
        # 십자선 그리기
        frame = self.draw_crosshair(frame)
        
        # 객체 감지 정보 표시
        if detected and bbox and center:
            frame = self.draw_detection_info(frame, bbox, center, area)
        
        # 드론 상태 정보 표시
        if drone:
            frame = self.draw_drone_status(frame, drone)
        
        # FPS 표시
        frame = self.draw_fps(frame)
        
        return frame
    
    def print_detection_log(self, detected: bool, center: Optional[Tuple[int, int]] = None, 
                           area: float = 0) -> None:
        """
        감지 결과를 콘솔에 로그 출력
        
        Args:
            detected: 감지 여부
            center: 중심점
            area: 영역 크기
        """
        if detected and center:
            print(f"{Colors.GREEN}[감지] 중심: {center}, 영역: {int(area)}px{Colors.END}")
        else:
            print(f"{Colors.YELLOW}[감지] 객체 없음{Colors.END}")
    
    def reset_counters(self) -> None:
        """디버깅 카운터 리셋"""
        self.frame_count = 0
        self.fps_start_time = 0
        self.current_fps = 0.0
