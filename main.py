import torch
import cv2
import numpy as np

trace = []
trace_size = 3


def mark_frame(frame, det):
    # x, y, w, height, confidence, class
    xyxycc = np.array(det.xyxy[0].cpu())
    for i in range(xyxycc.shape[0]):
        trace.append(xyxycc[i, 0:4])
        p1, p2 = (int(xyxycc[i, 0]), int(xyxycc[i, 1])), (int(xyxycc[i, 2]), int(xyxycc[i, 3]))
        cv2.rectangle(frame, p1, p2, (0, 0, 255), thickness=3, lineType=cv2.LINE_AA)

    for box in trace:
        x = int((box[0] + box[2]) / 2)
        y = int((box[1] + box[3]) / 2)
        min_x = max(x - trace_size, 0)
        min_y = max(y - trace_size, 0)
        max_x = min(x + trace_size, frame.shape[1] - 1)
        max_y = min(y + trace_size, frame.shape[0] - 1)
        p1, p2 = (min_x, min_y), (max_x, max_y)
        cv2.rectangle(frame, p1, p2, (0, 0, 255), thickness=-1)

    return frame

model = torch.hub.load("/home/jere/git/golf_tracer_web_app/app/yolov5", 'custom',
                       "/home/jere/git/yolov5/runs/train/exp4/weights/best.pt", source='local')

# define a video capture object
vid = cv2.VideoCapture(0)

while (True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    det = model(frame)
    frame = mark_frame(frame, det)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()