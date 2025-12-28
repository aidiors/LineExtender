# LineExtender

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Code Style](https://img.shields.io/badge/Code%20Style-PEP8-green)](https://peps.python.org/pep-0008/)

> **Disclaimer**: This tool is for educational and research purposes only. You are solely responsible for compliance with all applicable laws and regulations. Consult legal counsel before deployment in any production environment.

A real-time computer vision tool that detects and extends dominant lines on screen through a transparent overlay.

## Table of Contents
- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## About

LineExtender demonstrates practical applications of:
- Real-time screen capture via Windows GDI
- Line detection using Hough Transform with OpenCV
- Transparent overlay rendering with Pygame
- Dynamic parameter tuning through GUI controls


## Installation

**Prerequisites**:
- Windows 10/11
- Python 3.8 or higher

```bash
git clone https://github.com/aidiors/LineExtender.git
cd LineExtender
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

1. Start the application with target window name:
```bash
python src/main.py --window "Application Title"
```

2. Controls:
   - Press `INSERT` key to terminate application
   - Adjust detection parameters using OpenCV settings window

## Configuration

All parameters can be tuned at runtime through the OpenCV control panel:

| Parameter          | Description                                  | Valid Range |
|--------------------|----------------------------------------------|-------------|
| Capture Size       | Region size around cursor (pixels)           | 120-800     |
| Hough Threshold    | Sensitivity of line detection                | 1-140       |
| Min Line Length    | Minimum line segment length to consider     | 1-200       |
| Max Line Gap       | Maximum gap between line segments to merge  | 1-100       |

Default values are optimized for general use cases. Save optimal settings by modifying `constants.py`.

---

**Note for Russian speakers**:  
Полная документация на русском языке доступна в файле [README_RU.md](README_RU.md)