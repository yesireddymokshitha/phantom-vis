import cv2
import mediapipe as mp
import math
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)  # Detect up to 2 hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)  # Start webcam capture

# Set camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

fullscreen = False
cv2.namedWindow("PhantomVis", cv2.WINDOW_NORMAL)

# Variables for smoothing movement
prev_cx, prev_cy = 0, 0
smooth_factor = 0.2
pulse = 0  # Controls animation pulse


def rotate_point(cx, cy, x, y, angle):
    # Rotate a point (x,y) around center (cx,cy) by angle
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    # Apply rotation matrix
    nx = cos_a * (x - cx) - sin_a * (y - cy) + cx
    ny = sin_a * (x - cx) + cos_a * (y - cy) + cy

    return int(nx), int(ny)


def draw_controlled_cube(img, ix, iy, tx, ty, rx, ry, lx, ly):
    # Draw a cube controlled by one hand
    
    # Center of cube based on index & thumb
    cx = (ix + tx) // 2
    cy = (iy + ty) // 2

    # Cube size based on hand spread
    size = int(math.hypot(lx - tx, ly - ty))
    size = max(40, min(size, 200))  # Clamp size

    # Rotation angle based on finger direction
    angle = math.degrees(math.atan2(iy - ty, ix - tx))
    angle += (rx - cx) * 0.05  # Add tilt using ring finger

    s = size // 2
    offset = int(s * 0.7)  # Depth offset

    # Define front square
    front = [(cx - s, cy - s), (cx + s, cy - s),
             (cx + s, cy + s), (cx - s, cy + s)]

    # Define back square (shifted for 3D effect)
    back = [(x + offset, y - offset) for (x, y) in front]

    # Rotate both faces
    front = [rotate_point(cx, cy, x, y, angle) for (x, y) in front]
    back = [rotate_point(cx, cy, x, y, angle) for (x, y) in back]

    overlay = img.copy()

    # Fill cube faces with transparency
    cv2.fillPoly(overlay, [np.array(front)], (255, 255, 0))
    cv2.fillPoly(overlay, [np.array(back)], (255, 255, 0))
    cv2.addWeighted(overlay, 0.3, img, 0.7, 0, img)

    # Draw cube edges
    for i in range(4):
        thickness = 3 if i == 0 else 2
        cv2.line(img, front[i], front[(i + 1) % 4], (255, 255, 0), thickness)
        cv2.line(img, back[i], back[(i + 1) % 4], (255, 255, 0), 2)
        cv2.line(img, front[i], back[i], (255, 255, 0), 2)

    # Add slight shading to back face
    shade = img.copy()
    cv2.fillPoly(shade, [np.array(back)], (0, 0, 0))
    cv2.addWeighted(shade, 0.15, img, 0.85, 0, img)


def draw_energy_ball(img, cx, cy, size, pulse):
    # Draw glowing energy ball between two hands
    
    overlay = img.copy()

    # Animate glow size using sine wave
    glow_size = int(size + 10 * math.sin(pulse))

    # Draw multiple glow layers
    for i in range(6, 0, -1):
        cv2.circle(overlay, (cx, cy), glow_size + i * 8, (0, 0, 255), -1)

    cv2.addWeighted(overlay, 0.3, img, 0.7, 0, img)

    # Draw core of energy ball
    cv2.circle(img, (cx, cy), glow_size, (0, 0, 255), -1)
    cv2.circle(img, (cx, cy), glow_size, (0, 255, 255), 2)


while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Mirror image

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)  # Detect hands

    hand_data = []

    if results.multi_hand_landmarks:
        h, w, _ = frame.shape

        for handLms in results.multi_hand_landmarks:
            # Extract key finger positions
            ix, iy = int(handLms.landmark[8].x * w), int(handLms.landmark[8].y * h)   # Index
            tx, ty = int(handLms.landmark[4].x * w), int(handLms.landmark[4].y * h)   # Thumb
            rx, ry = int(handLms.landmark[16].x * w), int(handLms.landmark[16].y * h) # Ring
            lx, ly = int(handLms.landmark[20].x * w), int(handLms.landmark[20].y * h) # Pinky

            # Center of hand
            cx = (ix + tx + lx) // 3
            cy = (iy + ty + ly) // 3

            # Hand size based on spread
            dist = int(math.hypot(lx - tx, ly - ty))
            size = max(40, min(dist, 200))

            # Angle of hand orientation
            angle = math.degrees(math.atan2(ly - iy, lx - ix))

            # Store all hand data
            hand_data.append((ix, iy, tx, ty, rx, ry, lx, ly, cx, cy, size, angle))

            # Draw hand skeleton
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    shape_name = ""

    if len(hand_data) == 1:
        # One hand → control cube
        ix, iy, tx, ty, rx, ry, lx, ly, cx, cy, size, angle = hand_data[0]
        draw_controlled_cube(frame, ix, iy, tx, ty, rx, ry, lx, ly)
        shape_name = "CUBE"

    elif len(hand_data) == 2:
        # Two hands → energy ball interaction
        (ix1, iy1, tx1, ty1, rx1, ry1, lx1, ly1, cx1, cy1, s1, a1) = hand_data[0]
        (ix2, iy2, tx2, ty2, rx2, ry2, lx2, ly2, cx2, cy2, s2, a2) = hand_data[1]

        # Distance between hands
        hand_dist = math.hypot(cx2 - cx1, cy2 - cy1)

        MERGE_THRESHOLD = 60  # Threshold for merging effect

        # Midpoint between hands
        target_cx = (cx1 + cx2) // 2
        target_cy = (cy1 + cy2) // 2

        # Smooth movement of energy ball
        prev_cx = int(prev_cx + (target_cx - prev_cx) * smooth_factor)
        prev_cy = int(prev_cy + (target_cy - prev_cy) * smooth_factor)

        # Size based on distance
        size = int(hand_dist / 2)
        size = max(20, min(size, 200))

        if hand_dist < MERGE_THRESHOLD:
            # Hands close → compressed energy
            if size > 10:
                draw_energy_ball(frame, prev_cx, prev_cy, size, pulse)
            shape_name = ""
        else:
            # Hands apart → visible energy ball
            draw_energy_ball(frame, prev_cx, prev_cy, size, pulse)
            shape_name = "ENERGY"

        pulse += 0.2  # Animate pulse

    # Display shape name
    if shape_name:
        cv2.putText(
            frame, shape_name, (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1,
            (0, 0, 0), 3
        )

    cv2.imshow("PhantomVis", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('f'):
        # Toggle fullscreen
        fullscreen = not fullscreen

        if fullscreen:
            cv2.setWindowProperty("PhantomVis", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        else:
            cv2.setWindowProperty("PhantomVis", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
            cv2.resizeWindow("PhantomVis", 1280, 720)

    if key == ord("q") or key == 27:
        break  # Exit on 'q' or ESC

cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)