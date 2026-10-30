# =========================
import cv2, time, numpy as np
import mediapipe as mp

H = mp.solutions.hands
TIP = H.HandLandmark
ids = {
    "thumb": TIP.THUMB_TIP,
    "index": TIP.INDEX_FINGER_TIP,
    "middle": TIP.MIDDLE_FINGER_TIP,
    "ring": TIP.RING_FINGER_TIP,
    "pinky": TIP.PINKY_TIP,
}

# =========================
# CONTINUE WITH COMMENTS (BOILERPLATE EXPLANATION)
# =========================

# 1) Setup MediaPipe Hands (detect + track hand landmarks)
#    - hands = H.Hands(min_detection_confidence=..., min_tracking_confidence=...)
#    - draw = mp.solutions.drawing_utils (to draw dots/lines)

# 2) Decide gesture controls
#    - pairs: which finger toggles which 2 filters (middle/ring/pinky)
#    - st: 0/1 toggle state for each finger
#    - cur: currently selected filter

# 3) Thresholds + timers (to avoid accidental triggers)
#    - TT: thumb-to-finger “touch” distance
#    - TP: thumb-index “pinch” distance (capture)
#    - DEB: debounce time for toggles
#    - CAP: cooldown time for captures
#    - la/lc: last toggle/capture time, pinch_on: pinch state flag

# 4) Windows + pause mode
#    - MAIN: live window, POP: captured window
#    - paused=True shows freeze frame until ESC/close

# 5) Create apply(img, filter_name)
#    - Returns filtered image (SEPIA/NEGATIVE/BLUR/GLITCH/EDGE/CARTOON)
#    - If EDGE returns grayscale, convert back to BGR before display/save

# 6) Start webcam
#    - cap = cv2.VideoCapture(0)
#    - if not cap.isOpened(): print error and exit

# 7) Main loop
#    - If paused: show freeze, ESC/close to resume, 'q' to quit
#    - Else: read frame, flip, convert to RGB, run hands.process()

# 8) If hand detected
#    - Draw landmarks
#    - Convert landmark coords to pixel coords for tips using ids

# 9) Pinch to capture (thumb + index close)
#    - If pinch just started AND cooldown passed -> capture=True

# 10) Thumb touch to toggle filter (only when not pinching)
#    - If thumb near middle/ring/pinky AND debounce passed -> toggle cur

# 11) Apply filter + show output
#    - out = apply(img, cur)
#    - If capture: save file, set paused=True, freeze=out.copy(), show POP
#    - cv2.imshow(MAIN, out), press 'q' to quit

# 12) Cleanup
#    - cap.release(), cv2.destroyAllWindows(), hands.close()












import cv2, time, numpy as np
import mediapipe as mp
H = mp.solutions.hands
TIP = H.HandLandmark
ids = {
    "thumb": TIP.THUMB_TIP,
    "index": TIP.INDEX_FINGER_TIP,
    "middle": TIP.MIDDLE_FINGER_TIP,
    "ring": TIP.RING_FINGER_TIP,
    "pinky": TIP.PINKY_TIP,
}
hands = H.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
draw = mp.solutions.drawing_utils
pairs = {"middle":("SEPIA","NEGATIVE"), "ring":("BLUR","GLITCH"), "pinky":("EDGE","CARTOON")}
st = {k:0 for k in pairs}; cur = "SEPIA"
DEB, CAP, TT, TP = 0.6, 1.2, 30, 20
la = lc = 0; pinch_on = False
MAIN, POP = "Gesture-Controlled Photo App", "Captured (ESC / Close to resume)"
paused = False; freeze = None
SEPIA_M = np.array([[0.272,0.534,0.131],[0.349,0.686,0.168],[0.393,0.769,0.189]])
def apply(img, t):
    if t == "SEPIA": return np.clip(cv2.transform(img, SEPIA_M), 0, 255).astype(np.uint8)
    if t == "NEGATIVE": return cv2.bitwise_not(img)
    if t == "BLUR": return cv2.GaussianBlur(img, (15, 15), 0)
    if t == "GLITCH":
        h,w = img.shape[:2]; r,g,b = img[:,:,2], img[:,:,1], img[:,:,0]
        return cv2.merge([np.roll(b, -int(0.02*w), 1), g, np.roll(r, int(0.04*w), 1)])
    if t == "EDGE": return cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 80, 160)
    if t == "CARTOON":
        g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        e = cv2.adaptiveThreshold(cv2.medianBlur(g, 7), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
        c = cv2.bilateralFilter(img, 9, 75, 75)
        return cv2.bitwise_and(c, c, mask=e)
    return img
cap = cv2.VideoCapture(0)
if not cap.isOpened(): print("Error: Could not access the webcam."); exit()
cv2.namedWindow(MAIN, cv2.WINDOW_NORMAL)
while True:
    if paused:
        cv2.imshow(MAIN, freeze)
        k = cv2.waitKey(50) & 0xFF
        if k == ord("q"): break
        if k == 27:
            paused = False; pinch_on = False
            try: cv2.destroyWindow(POP)
            except: pass
            continue
        try:
            if cv2.getWindowProperty(POP, cv2.WND_PROP_VISIBLE) <= 0: paused = False; pinch_on = False
        except cv2.error:
            paused = False; pinch_on = False
        continue
    ok, img = cap.read()
    if not ok: break
    img = cv2.flip(img, 1); h, w = img.shape[:2]
    res = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    now = time.time(); capture = False
    if res.multi_hand_landmarks:
        hand = res.multi_hand_landmarks[0]; draw.draw_landmarks(img, hand, H.HAND_CONNECTIONS)
        lm = hand.landmark; tips = {k:(int(lm[v].x*w), int(lm[v].y*h)) for k,v in ids.items()}
        tx,ty = tips["thumb"]; ix,iy = tips["index"]
        pinch = abs(tx-ix) < TP and abs(ty-iy) < TP
        if pinch and not pinch_on and now-lc > CAP: pinch_on = True; capture = True; lc = now
        if not pinch and pinch_on: pinch_on = False
        if not pinch:
            t = next((k for k in pairs if abs(tx-tips[k][0]) < TT and abs(ty-tips[k][1]) < TT), None)
            if t and now-la > DEB: cur = pairs[t][st[t]]; st[t] ^= 1; la = now; print("Filter:", cur)
    out = apply(img, cur)
    if cur == "EDGE": out = cv2.cvtColor(out, cv2.COLOR_GRAY2BGR)
    if capture:
        name = f"picture_{int(now)}.jpg"; cv2.imwrite(name, out); print("Saved:", name)
        paused, freeze = True, out.copy(); cv2.imshow(POP, freeze)
    cv2.imshow(MAIN, out)
    if cv2.waitKey(1) & 0xFF == ord("q"): break
cap.release(); cv2.destroyAllWindows(); hands.close()