import cv2
import numpy as np
import torch
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_path='best.pt'):
        """
        Initialize YOLO object detector
        
        :param model_path: Path to YOLO model weights
        """
        self.model = YOLO(model_path)
        self.classes = self.model.names

    def detect_objects(self, frame):
        """
        Detect objects in a frame and return annotated frame
        
        :param frame: Input image/frame
        :return: Frame with detections and list of detected objects
        """
        # Run detection
        results = self.model(frame)[0]
        
        # Create a copy of the frame for annotation
        annotated_frame = frame.copy()
        
        # Track detected objects
        detected_objects = set()
        missing_objects = set(self.classes.values())

        # Process detections
        for result in results.boxes:
            # Extract detection details
            x1, y1, x2, y2 = result.xyxy[0]
            conf = result.conf[0]
            cls = int(result.cls[0])
            label = self.classes[cls]
            
            # Only process detections with confidence > 0.5
            if conf > 0.5:
                # Draw bounding box
                cv2.rectangle(annotated_frame, 
                              (int(x1), int(y1)), 
                              (int(x2), int(y2)), 
                              (0, 255, 0), 2)
                
                # Put label and confidence
                label_text = f'{label} {conf:.2f}'
                cv2.putText(annotated_frame, label_text, 
                            (int(x1), int(y1 - 10)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, 
                            (0, 255, 0), 2)
                
                # Track detected objects
                detected_objects.add(label)
                if label in missing_objects:
                    missing_objects.remove(label)

        # Add missing object indicators
        for obj in missing_objects:
            
            cv2.rectangle(annotated_frame, 
                          (10, 30 * (list(missing_objects).index(obj) + 1)), 
                          (300, 30 * (list(missing_objects).index(obj) + 1) + 25), 
                          (0, 0, 255), 2)
            cv2.putText(annotated_frame, 
                        f'No {obj}', 
                        (20, 30 * (list(missing_objects).index(obj) + 1) + 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, 
                        (0, 0, 255), 2)

        return annotated_frame, detected_objects, missing_objects

    def process_webcam(self):
        """
        Process webcam stream
        
        :yield: Processed frames with detections
        """
        cap = cv2.VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Detect objects
            annotated_frame, _, _ = self.detect_objects(frame)
            
            yield annotated_frame
        
        cap.release()
