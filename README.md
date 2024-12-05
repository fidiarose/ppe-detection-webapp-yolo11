# YOLO PPE Detection Web App

## Prerequisites
- Python 3.8+
- pip
- Webcam 

## Installation

1. Clone the repository
```bash
git clone https://github.com/fidiarose/ppe-detection-webapp-yolo11.git
cd ppe-detection-webapp-yolo11
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Download YOLO model
- I use my own pre-trained model from YOLO11 (best.pt)
- You can use another pre-trained yolo model, such as yolo11n.pt or replace with your own

## Running the Application
```bash
python app.py
```

Open a web browser and navigate to 'http://localhost:port'
