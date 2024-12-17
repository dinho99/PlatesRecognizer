# PlatesRecognizer
This repo I tried to detect and recognize plate license for managing a supermarket parking lot.

This project is a computer vision application to detect and recognize plate license. The system is implemented in Python and utilizes OpenCV for images processing and pytessercat to extract the text from the image.

## Prerequisites
- Python 3.6+
- OpenCV
- pytesseract

## Features
- License Plate Detection: Utilizes a Haar Cascade model to identify license plates in images or video frames.
- Text Recognition: Extracts license plate text using Tesseract OCR, configured for small, high-precision text regions.
- Vehicle Entry and Exit Logging:
  Records the entry time of vehicles when a license plate is detected.
  Logs the exit time of vehicles when they leave the parking lot.
- Data Storage: Maintains a complete history of license plate activities, including timestamps for entry and exit.
