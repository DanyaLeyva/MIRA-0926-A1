# MIRA-0926-A1

**MIRA (Motion Intelligence & Recognition Assistant)** is a vision-based research system designed to investigate human movement analysis, pose-estimation reliability, and simplified biomechanical measurements using consumer camera hardware.

The project combines computer vision, human movement analysis, and biomechanics to explore how pose-estimation accuracy affects downstream movement measurements.

## Research Focus

**Vision-Based Biomechanical Analysis and Pose Estimation Reliability**

MIRA investigates how different human pose-estimation methods perform when analyzing movement and how differences in their estimated body landmarks influence biomechanical calculations.

The project focuses on comparing **MediaPipe and OpenPose** through controlled experiments involving joint-angle measurements, tracking stability, and simplified hip-joint torque estimation.

## Research Questions

**RQ1 — Joint-Angle Reliability**

How do MediaPipe and OpenPose compare in the accuracy and stability of joint-angle measurements across different movements and camera conditions?

**RQ2 — Biomechanical Analysis**

How do differences in pose-estimation measurements affect simplified estimates of hip-joint torque?

**RQ3 — Camera Conditions**

How do camera distance, angle, and other recording conditions affect the reliability of pose-estimation measurements?

## Project Objectives

- Develop a real-time computer-vision pipeline using consumer camera hardware.
- Implement human pose estimation using MediaPipe and OpenPose.
- Calculate joint angles from detected body landmarks.
- Compare joint-angle accuracy and tracking stability between pose-estimation methods.
- Investigate how measurement differences influence simplified biomechanical calculations.
- Evaluate processing performance and reliability under different recording conditions.
- Document experimental results, limitations, and potential applications in biomechanics and human–robot interaction.

## Technologies

**Current implementation:**

- Python
- OpenCV
- MediaPipe
- NumPy
- Git and GitHub

**Planned:**

- OpenPose
- Additional data-analysis and visualization tools as needed

## Research Methodology

### 1. Pose Estimation

Use MediaPipe and OpenPose to estimate body landmarks from the same movement recordings.

### 2. Joint-Angle Measurements

Calculate joint angles using detected landmark coordinates.

Initial development focuses on elbow-angle measurements, followed by hip, knee, and shoulder angles.

### 3. Pose-Estimation Comparison

Compare the two approaches using:

- Joint-angle measurement accuracy against reference measurements
- Tracking stability and measurement variability
- Missing or unreliable landmarks
- Processing speed
- Performance under different camera conditions

### 4. Biomechanical Analysis

Investigate how pose-estimation differences affect simplified biomechanical calculations, particularly estimated hip-joint torque.

The analysis will use clearly defined assumptions and simplified mechanical models. These estimates will not be treated as direct measurements of actual joint torque.

### 5. Experimental Evaluation

Conduct controlled experiments, compare results, and document the limitations of each approach.

## Current Implementation

**Status: Initial MediaPipe Pipeline Completed**

MIRA currently supports:

- Real-time webcam input using OpenCV
- Human pose detection using MediaPipe
- Skeleton and body landmark visualization
- Color-coded skeleton connections
- Landmark smoothing to reduce tracking jitter
- Left and right elbow-angle calculations
- Basic landmark visibility checks

The current pipeline has been tested using a MacBook webcam.

Formal accuracy evaluation, OpenPose integration, and biomechanical torque estimation have not yet been completed.

## Project Structure

```text
MIRA-0926-A1/
├── models/
│   └── pose_landmarker_lite.task
├── src/
│   └── vision/
│       ├── camera.py
│       ├── pose_detector.py
│       └── joint_angles.py
├── tests/
├── paper/
├── sandbox/
├── main.py
├── requirements.txt
└── README.md
```

## Installation and Running MIRA

### 1. Clone the Repository

```bash
git clone https://github.com/DanyaLeyva/MIRA-0926-A1.git
cd MIRA-0926-A1
```

### 2. Create a Python Environment

MIRA is currently developed using Python 3.12.

```bash
conda create -n mira python=3.12
conda activate mira
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Current MediaPipe Pipeline

```bash
python -m src.vision.camera
```

Allow camera access if prompted.

The application displays the detected skeleton and elbow-angle measurements in real time.

Press `q` to exit.

_These instructions run the current MediaPipe implementation. OpenPose integration is planned for a later development stage._

## Development Progress

**Completed:**

- Initial research direction and system architecture
- GitHub repository and development environment
- Webcam integration
- MediaPipe pose-detection pipeline
- Skeleton visualization
- Landmark smoothing
- Initial elbow-angle measurements

**In Progress / Planned:**

- Quantitative evaluation of elbow-angle accuracy
- OpenPose integration and comparison
- Additional joint-angle measurements
- Simplified hip-joint torque model
- Controlled experiments
- Experimental results and analysis
- Public application deployment
- Final research paper and demonstration

## Future Applications

MIRA's research may support future work involving:

- Human movement assessment
- Biomechanics
- Assistive and wearable robotics
- Human–robot interaction
- Vision-based movement monitoring

These are potential applications rather than capabilities currently demonstrated by the system.

## Project Documentation

Research logs, literature reviews, development decisions, and experimental documentation are maintained in the [MIRA GitHub Wiki](https://github.com/DanyaLeyva/MIRA-0926-A1/wiki).

## Author

Danya Leyva  
Computer Science Student  
California State University, Dominguez Hills
