import os
import cv2
import uuid
from flask import Flask, render_template, request, Response
from utils.detector import ObjectDetector

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

detector = ObjectDetector()

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

def generate_video_frames(source='upload'):
    """
    Generate video frames for streaming
    
    :param source: Source of video frames ('webcam')
    """
    try:
        if source == 'upload':
            # Process uploaded video
            video_path = request.form.get('video_path')
            frames = detector.process_video(video_path)
        else:
            # Process webcam
            frames = detector.process_webcam()
        
        for frame in frames:
            # Encode frame
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except Exception as e:
        print(f"Error in frame generation: {e}")


@app.route('/video_feed')
def video_feed():
    """Stream video frames"""
    return Response(generate_video_frames('webcam'), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
