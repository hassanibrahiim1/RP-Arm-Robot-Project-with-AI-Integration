import cv2
import numpy as np
import time
import serial

# Color ranges in HSV
COLOR_RANGES = {
    "red":   [([0, 120, 70], [10, 255, 255]), ([170, 120, 70], [180, 255, 255])],
    "green": [([36, 50, 70], [89, 255, 255])],
    "blue":  [([90, 50, 70], [128, 255, 255])],
    "yellow":[([20, 100, 100], [30, 255, 255])],
    "black": [([0, 0, 0], [180, 255, 50])]
}

def get_mask(hsv, color):
    masks = []
    for lower, upper in COLOR_RANGES[color]:
        lower = np.array(lower)
        upper = np.array(upper)
        masks.append(cv2.inRange(hsv, lower, upper))
    mask = masks[0]
    for m in masks[1:]:
        mask = mask | m
    return mask

def detect_object(frame, color):
    frame = cv2.flip(frame, 1)  # Flip the frame horizontally to fix mirroring
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = get_mask(hsv, color)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cx = x + w // 2
        cy = y + h // 2
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.circle(frame, (cx, cy), 5, (255,0,0), -1)
        height, width, _ = frame.shape
        pan = int(cx * 180 / width)
        tilt = int(cy * 180 / height)
        return True, pan, tilt, frame
    return False, 0, 0, frame

def main():
    ser = serial.Serial('COM7', 115200, timeout=1)
    cap = cv2.VideoCapture(0)
    time.sleep(2)
    color = input("Enter target color (red, green, blue, yellow, black): ").strip().lower()
    if color not in COLOR_RANGES:
        print("Color not supported.")
        return

    print("Press 'q' to quit, 'c' to confirm sending angles to servo.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detected, pan, tilt, out_frame = detect_object(frame, color)

        if detected:
            cv2.putText(out_frame, f"Detected {color} object -> pan: {pan}, tilt: {tilt}",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(out_frame, "Press 'c' to confirm, 'q' to quit",
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        else:
            cv2.putText(out_frame, f"No {color} object detected.",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Detection", out_frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            print("Search canceled.")
            break
        elif key == ord('c') and detected:
            print(f"Confirmed. Sending: a{pan}, b{tilt}")
            ser.write(f"a{pan}\n".encode())
            time.sleep(0.1)
            ser.write(f"b{tilt}\n".encode())
            time.sleep(1)  # Allow time before next frame

    cap.release()
    cv2.destroyAllWindows()
    ser.close()

if __name__ == "__main__":
    main()
