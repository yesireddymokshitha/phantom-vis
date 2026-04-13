# PhantomVis

PhantomVis is a real-time, browser-based hand tracking visualizer powered by MediaPipe. It transforms hand gestures into interactive 3D-style visuals, creating an immersive, futuristic interface directly in your webcam.

---

## Overview

PhantomVis uses computer vision to detect hand landmarks and render dynamic visual effects:

* One hand generates a holographic shape (cube or sphere)
* Two hands enable dynamic scaling and interaction
* Smooth motion tracking with visual feedback
* Fully runs in the browser with no backend

---

## Features

### Real-Time Hand Tracking

* Powered by MediaPipe Hands
* Tracks up to two hands simultaneously
* Smooth and responsive gesture detection with stabilization

### Gesture-Based Modes

* **Single Hand Mode**

  * Displays selected shape on the palm (Cube / Sphere)
  * Cube aligns with hand orientation
  * Sphere anchors to palm center with dynamic size

* **Dual Hand Mode**

  * Shape appears between both hands
  * Size dynamically scales with distance between palms
  * Continuous interaction with both hands

### Shape System

* **Cube Mode**

  * Fully volumetric holographic cube
  * Perfect geometric proportions (no distortion)
  * Rotates with hand orientation (single hand) or auto-rotates (two hands)
  * Cyan energy core with layered glow

* **Sphere Mode**

  * High-density particle energy sphere (~2200 particles)
  * Internal motion simulation with depth illusion
  * Continuous rotation for dynamic effect
  * Red/orange plasma-style visuals

### Fingertip Interaction

* Energy tethers connect fingertips to shapes
* 5-point interaction (single hand)
* 10-point interaction (dual hand)
* Dynamic glow and animated connection lines

### Visual Effects

* Neon holographic UI (cyan + red energy themes)
* Advanced glow layering and gradients
* Particle-based rendering system
* Depth illusion and volumetric lighting
* Subtle scanline overlay for sci-fi aesthetic

### HUD Interface

* Live hand count
* Active shape display
* Dynamic size metrics
* Status tracking (Idle / Tracking)
* Shape toggle UI (Cube / Sphere)

---

## Tech Stack

* HTML5 Canvas
* JavaScript (Vanilla)
* MediaPipe Hands
* WebRTC (`getUserMedia`)

---

## How It Works

1. Webcam feed is captured using `getUserMedia`
2. MediaPipe processes each frame and extracts hand landmarks
3. Landmarks are mapped onto canvas coordinates
4. Visual systems render based on detected gestures:

   * **Cube**

     * Uses projected geometry and rotation math
     * Multi-layer glow rendering with edge highlights

   * **Sphere**

     * Particle simulation inside a clipped circular boundary
     * Depth-based rendering with rotation and twinkling effects

   * **Interaction**

     * Fingertips dynamically connect to object surfaces
     * Smooth interpolation ensures stable visuals

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

| Gesture       | Action                    |
| ------------- | ------------------------- |
| One hand      | Spawn shape on palm       |
| Two hands     | Scale shape between hands |
| Toggle button | Switch Cube / Sphere      |

---

## Performance Notes

* Optimized particle system (~2200 particles for sphere)
* Frame-based scanline rendering (not constant)
* Smooth interpolation (LERP) for stable tracking
* Efficient clipping for volumetric effects
* Minimal CPU overhead with canvas-based rendering

---

## Browser Support

* Chrome (recommended)
* Edge
* Firefox (may have minor performance differences)

Webcam access is required.

---

## Known Limitations

* Requires good lighting for accurate tracking
* Performance may drop on low-end devices
* Mobile browsers may have limited support
* High particle count may affect weaker GPUs

---

## Future Improvements

* Advanced gesture recognition (pinch, grab, swipe)
* Additional shapes and visual modes
* Audio-reactive energy systems
* WebGL / Three.js acceleration
* AR-style spatial anchoring
* Multi-user interaction

---

## Author

Yesireddy Mokshitha
