"""ML-based squirrel, skunk, and raccoon detection using YOLO v8."""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np

try:
    from ultralytics import YOLO

    ULTRALYTICS_AVAILABLE = True
except ImportError:
    ULTRALYTICS_AVAILABLE = False

logger = logging.getLogger(__name__)

# Class mappings
CLASS_NAMES = {
    0: "squirrel",
    1: "skunk",
    2: "raccoon",
}

CLASS_IDS = {name: idx for idx, name in CLASS_NAMES.items()}


class MLDetector:
    """YOLO v8 based detector for squirrels, skunks, and raccoons."""

    def __init__(
        self,
        model_path: Optional[str] = None,
        confidence_threshold: float = 0.25,
        center_threshold: float = 0.3,
        device: str = "cpu",
    ):
        """Initialize the ML detector.

        Args:
            model_path: Path to YOLO model file (.pt). If None, uses default location.
            confidence_threshold: Minimum confidence for detection (0.0-1.0)
            center_threshold: Percentage of frame considered "center" (0.0-1.0)
            device: Device to use ('cpu', 'cuda', '0', '1', etc.)
        """
        if not ULTRALYTICS_AVAILABLE:
            raise ImportError(
                "ultralytics is not available. Install with: pip install ultralytics"
            )

        self.confidence_threshold = confidence_threshold
        self.center_threshold = center_threshold
        self.device = device

        # Default model path
        if model_path is None:
            # Look for model in various locations
            possible_paths = [
                Path("models/wildlife_detector.pt"),
                Path("training/runs/wildlife_detection/weights/best.pt"),
                Path("models/best.pt"),
            ]
            model_path = None
            for path in possible_paths:
                if path.exists():
                    model_path = str(path)
                    break

            if model_path is None:
                # Use pre-trained YOLO v8 as fallback (will need fine-tuning)
                logger.warning(
                    "No trained model found. Using pre-trained YOLO v8 (not trained on wildlife). "
                    "Train a model first for accurate detection."
                )
                model_path = "yolov8n.pt"

        logger.info(f"Loading YOLO model from: {model_path}")
        self.model = YOLO(model_path)
        self.model.to(device)

        logger.info(
            f"ML Detector initialized. Classes: {list(CLASS_NAMES.values())}, "
            f"Confidence threshold: {confidence_threshold}"
        )

    def detect(
        self, frame: np.ndarray
    ) -> Tuple[bool, Optional[Tuple[int, int, int, int]], float, Optional[str]]:
        """Detect wildlife in a frame.

        Args:
            frame: Input frame (BGR format)

        Returns:
            Tuple of (detected, bounding_box, confidence, class_name)
            - detected: True if any target class detected
            - bounding_box: (x, y, width, height) or None
            - confidence: Detection confidence (0.0-1.0)
            - class_name: 'squirrel', 'skunk', 'raccoon', or None
        """
        if frame is None or frame.size == 0:
            return False, None, 0.0, None

        # Run inference
        results = self.model(frame, conf=self.confidence_threshold, verbose=False)

        if not results or len(results) == 0:
            return False, None, 0.0, None

        # Get first result (should only be one for single image)
        result = results[0]

        if result.boxes is None or len(result.boxes) == 0:
            return False, None, 0.0, None

        # Find the best detection (highest confidence)
        best_box = None
        best_conf = 0.0
        best_class = None

        for box in result.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])

            # Only consider our target classes (0=squirrel, 1=skunk, 2=raccoon)
            if cls_id in CLASS_NAMES and conf > best_conf:
                best_box = box
                best_conf = conf
                best_class = CLASS_NAMES[cls_id]

        if best_box is None:
            return False, None, 0.0, None

        # Get bounding box coordinates
        xyxy = best_box.xyxy[0].cpu().numpy()
        x1, y1, x2, y2 = xyxy
        x, y = int(x1), int(y1)
        w, h = int(x2 - x1), int(y2 - y1)

        return True, (x, y, w, h), best_conf, best_class

    def detect_all(
        self, frame: np.ndarray
    ) -> List[Tuple[str, Tuple[int, int, int, int], float]]:
        """Detect all wildlife in a frame.

        Args:
            frame: Input frame (BGR format)

        Returns:
            List of (class_name, bounding_box, confidence) tuples
        """
        if frame is None or frame.size == 0:
            return []

        # Run inference
        results = self.model(frame, conf=self.confidence_threshold, verbose=False)

        if not results or len(results) == 0:
            return []

        result = results[0]

        if result.boxes is None or len(result.boxes) == 0:
            return []

        detections = []
        for box in result.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])

            # Only consider our target classes
            if cls_id in CLASS_NAMES:
                xyxy = box.xyxy[0].cpu().numpy()
                x1, y1, x2, y2 = xyxy
                x, y = int(x1), int(y1)
                w, h = int(x2 - x1), int(y2 - y1)
                detections.append((CLASS_NAMES[cls_id], (x, y, w, h), conf))

        return detections

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
    ) -> Tuple[bool, Optional[Tuple[int, int, int, int]], float, Optional[str]]:
        """Detect wildlife and check if it's in the center.

        Args:
            frame: Input frame (BGR format)

        Returns:
            Tuple of (detected_in_center, bounding_box, confidence, class_name)
        """
        detected, bbox, confidence, class_name = self.detect(frame)

        if not detected or bbox is None:
            return False, None, 0.0, None

        in_center = self.is_in_center(frame, bbox)

        if in_center:
            return True, bbox, confidence, class_name
        else:
            return False, None, 0.0, None
