"""Squirrel detection using computer vision."""

import logging
from typing import Optional, Tuple

import cv2
import numpy as np

logger = logging.getLogger(__name__)


class SquirrelDetector:
    """Detects squirrels in camera frames using computer vision."""

    def __init__(
        self,
        confidence_threshold: float = 0.5,
        center_threshold: float = 0.3,
        use_haar: bool = True,
    ):
        """Initialize the squirrel detector.

        Args:
            confidence_threshold: Minimum confidence for detection (0.0-1.0)
            center_threshold: Percentage of frame considered "center" (0.0-1.0)
            use_haar: Whether to use Haar cascade (fallback if model not found)
        """
        self.confidence_threshold = confidence_threshold
        self.center_threshold = center_threshold
        self.use_haar = use_haar

        # Try to load a pre-trained model (YOLO or similar)
        # For now, we'll use a combination of color detection and contour analysis
        # In production, you might want to use a trained model
        self._init_detector()

    def _init_detector(self) -> None:
        """Initialize the detection model."""
        # For a real implementation, you would load a trained model here
        # This is a placeholder that uses color and shape analysis
        logger.info("Initializing squirrel detector with color/shape analysis")

    def detect(self, frame: np.ndarray) -> Tuple[bool, Optional[Tuple[int, int, int, int]], float]:
        """Detect squirrels in a frame.

        Args:
            frame: Input frame (BGR format)

        Returns:
            Tuple of (detected, bounding_box, confidence)
            - detected: True if squirrel detected
            - bounding_box: (x, y, width, height) or None
            - confidence: Detection confidence (0.0-1.0)
        """
        if frame is None or frame.size == 0:
            return False, None, 0.0

        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Squirrels are typically brown/reddish-brown
        # Define ranges for brown/reddish colors
        lower_brown1 = np.array([10, 50, 50])
        upper_brown1 = np.array([20, 255, 255])
        lower_brown2 = np.array([0, 50, 50])
        upper_brown2 = np.array([10, 255, 255])

        # Create masks for brown colors
        mask1 = cv2.inRange(hsv, lower_brown1, upper_brown1)
        mask2 = cv2.inRange(hsv, lower_brown2, upper_brown2)
        mask = cv2.bitwise_or(mask1, mask2)

        # Apply morphological operations to clean up the mask
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return False, None, 0.0

        # Find the largest contour that might be a squirrel
        largest_contour = max(contours, key=cv2.contourArea)

        # Filter by size (squirrels should be reasonably sized)
        area = cv2.contourArea(largest_contour)
        min_area = (frame.shape[0] * frame.shape[1]) * 0.01  # At least 1% of frame
        max_area = (frame.shape[0] * frame.shape[1]) * 0.5  # At most 50% of frame

        if area < min_area or area > max_area:
            return False, None, 0.0

        # Get bounding box
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Calculate aspect ratio (squirrels are roughly 1:1 to 2:1)
        aspect_ratio = w / h if h > 0 else 0
        if aspect_ratio < 0.5 or aspect_ratio > 2.5:
            return False, None, 0.0

        # Calculate confidence based on area and aspect ratio
        frame_area = frame.shape[0] * frame.shape[1]
        area_ratio = area / frame_area
        confidence = min(area_ratio * 10, 1.0)  # Scale to 0-1

        # Adjust confidence based on aspect ratio (prefer 1:1 to 2:1)
        if 0.8 <= aspect_ratio <= 1.5:
            confidence *= 1.2
        confidence = min(confidence, 1.0)

        detected = confidence >= self.confidence_threshold

        return detected, (x, y, w, h), confidence

    def is_in_center(self, frame: np.ndarray, bbox: Optional[Tuple[int, int, int, int]]) -> bool:
        """Check if bounding box is in the center region of the frame.

        Args:
            frame: Input frame
            bbox: Bounding box (x, y, width, height) or None

        Returns:
            True if bbox center is in the center region
        """
        if bbox is None or frame is None:
            return False

        x, y, w, h = bbox
        frame_height, frame_width = frame.shape[:2]

        # Calculate center of bounding box
        bbox_center_x = x + w // 2
        bbox_center_y = y + h // 2

        # Calculate center region bounds
        center_region_width = int(frame_width * self.center_threshold)
        center_region_height = int(frame_height * self.center_threshold)

        center_start_x = frame_width // 2 - center_region_width // 2
        center_end_x = frame_width // 2 + center_region_width // 2
        center_start_y = frame_height // 2 - center_region_height // 2
        center_end_y = frame_height // 2 + center_region_height // 2

        # Check if bbox center is within center region
        in_center_x = center_start_x <= bbox_center_x <= center_end_x
        in_center_y = center_start_y <= bbox_center_y <= center_end_y

        return in_center_x and in_center_y

    def detect_and_check_center(
        self, frame: np.ndarray
    ) -> Tuple[bool, Optional[Tuple[int, int, int, int]], float]:
        """Detect squirrel and check if it's in the center.

        Args:
            frame: Input frame (BGR format)

        Returns:
            Tuple of (detected_in_center, bounding_box, confidence)
        """
        detected, bbox, confidence = self.detect(frame)

        if not detected or bbox is None:
            return False, None, 0.0

        in_center = self.is_in_center(frame, bbox)

        return in_center, bbox, confidence
