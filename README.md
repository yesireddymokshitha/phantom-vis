# PhantomVis

PhantomVis is a real-time, browser-based hand tracking visualizer powered by MediaPipe. It transforms hand gestures into interactive 3D-style visuals, creating an immersive, futuristic interface directly in your webcam.

---

## Overview

PhantomVis uses computer vision to detect hand landmarks and render dynamic visual effects:

- One hand generates a rotating holographic cube  
- Two hands create a reactive energy sphere  
- Smooth motion tracking with visual feedback  
- Fully runs in the browser with no backend  

---

## Features

### Real-Time Hand Tracking
- Powered by MediaPipe Hands
- Tracks up to two hands simultaneously
- Smooth and responsive gesture detection

### Gesture-Based Modes
- **Single Hand Mode**
  - Displays a glowing 3D cube
  - Rotation based on finger orientation
- **Dual Hand Mode**
  - Generates an energy sphere between hands
  - Size dynamically scales with distance
- **Compression Mode**
  - Energy ball compresses when hands move closer

### Visual Effects
- Neon yellow holographic UI
- Particle-based energy system (1000 particles)
- Glow effects and soft shadows
- Scanline overlay for sci-fi aesthetic

### HUD Interface
- Live hand count
- Active mode indicator
- Dynamic size metrics
- Status tracking (Idle / Tracking)

---

## Tech Stack

- HTML5 Canvas
- JavaScript (Vanilla)
- MediaPipe Hands
- WebRTC (getUserMedia)

---

## How It Works

1. Webcam feed is captured using `getUserMedia`
2. MediaPipe processes each frame and extracts hand landmarks
3. Landmarks are mapped onto canvas coordinates
4. Visual systems render based on detected gestures:
   - Cube: uses geometric rotation and projection
   - Energy Ball: particle simulation within a circular boundary

---

## Installation

No installation required.

### Run Locally

1. Copy the code into an `index.html` file  
2. Open it in a modern browser (Chrome recommended)  
3. Allow camera access  
4. Start interacting  

---

## Controls

| Gesture        | Action              |
|----------------|--------------------|
| One hand       | Spawn cube         |
| Two hands far  | Create energy ball |
| Two hands near | Compress energy    |

---

## Performance Notes

- Optimized particle rendering using batching
- Frame-based scanline effect (not constant)
- Smooth interpolation for hand center tracking
- Efficient clipping for energy sphere rendering

---

## Browser Support

- Chrome (recommended)
- Edge
- Firefox (may have minor performance differences)

Webcam access is required.

---

## Known Limitations

- Requires good lighting for accurate tracking  
- Performance may drop on low-end devices  
- Mobile browsers may have limited support  

---

## Future Improvements

- Gesture recognition (pinch, swipe, grab)
- More visual modes and effects
- Audio-reactive visuals
- Multi-user interaction
- WebGL acceleration

---

## Author

Yesireddy Mokshitha