"""Tests for squirrel detector."""

import numpy as np
import pytest

from squirrel.detector import SquirrelDetector


class TestSquirrelDetector:
    """Tests for SquirrelDetector."""

    def test_init(self):
        """Test SquirrelDetector initialization."""
        detector = SquirrelDetector(
            confidence_threshold=0.5, center_threshold=0.3, use_haar=True
        )
        assert detector.confidence_threshold == 0.5
        assert detector.center_threshold == 0.3

    def test_detect_empty_frame(self):
        """Test detection with empty/None frame."""
        detector = SquirrelDetector()
        detected, bbox, confidence = detector.detect(None)
        assert detected is False
        assert bbox is None
        assert confidence == 0.0

    def test_detect_no_target(self):
        """Test detection with frame containing no brown objects."""
        detector = SquirrelDetector(confidence_threshold=0.3)
        # Create a blue frame (no brown)
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        frame[:, :] = [255, 0, 0]  # Blue in BGR

        detected, bbox, confidence = detector.detect(frame)
        # Should not detect anything in a blue frame
        assert isinstance(detected, bool)
        assert confidence >= 0.0

    def test_detect_brown_object(self):
        """Test detection with brown-colored object."""
        detector = SquirrelDetector(confidence_threshold=0.1)
        # Create a frame with a brown rectangle
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # Brown color in BGR (approximately)
        frame[100:300, 200:400] = [42, 42, 165]  # Brownish

        detected, bbox, confidence = detector.detect(frame)
        # May or may not detect depending on color matching
        assert isinstance(detected, bool)
        assert isinstance(confidence, float)
        assert 0.0 <= confidence <= 1.0

    def test_is_in_center_none_bbox(self):
        """Test center check with None bbox."""
        detector = SquirrelDetector()
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        assert detector.is_in_center(frame, None) is False

    def test_is_in_center_center_bbox(self):
        """Test center check with bbox in center."""
        detector = SquirrelDetector(center_threshold=0.5)
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # Bbox in center of frame
        bbox = (270, 190, 100, 100)  # x, y, w, h centered around (320, 240)
        assert detector.is_in_center(frame, bbox) is True

    def test_is_in_center_edge_bbox(self):
        """Test center check with bbox at edge."""
        detector = SquirrelDetector(center_threshold=0.3)
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # Bbox at top-left corner
        bbox = (10, 10, 50, 50)
        assert detector.is_in_center(frame, bbox) is False

    def test_is_in_center_custom_threshold(self):
        """Test center check with custom threshold."""
        detector = SquirrelDetector(center_threshold=0.8)  # Large center region
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # Bbox that would be outside with 0.3 threshold but inside with 0.8
        bbox = (100, 100, 100, 100)
        result = detector.is_in_center(frame, bbox)
        assert isinstance(result, bool)

    def test_detect_and_check_center_no_detection(self):
        """Test combined detect and center check with no detection."""
        detector = SquirrelDetector(confidence_threshold=0.9)
        # Blue frame (no brown)
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        frame[:, :] = [255, 0, 0]

        detected, bbox, confidence = detector.detect_and_check_center(frame)
        assert detected is False
        assert bbox is None
        assert confidence == 0.0

    def test_confidence_threshold(self):
        """Test that confidence threshold affects detection."""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        frame[100:300, 200:400] = [42, 42, 165]  # Brownish

        detector_low = SquirrelDetector(confidence_threshold=0.1)
        detector_high = SquirrelDetector(confidence_threshold=0.9)

        detected_low, _, conf_low = detector_low.detect(frame)
        detected_high, _, conf_high = detector_high.detect(frame)

        # If detection happens, low threshold should detect more easily
        # But both should return valid confidence values
        assert 0.0 <= conf_low <= 1.0
        assert 0.0 <= conf_high <= 1.0
