import cv2
from datetime import datetime
from utils import get_path_to_data, create_connection

def get_connection_to_camera():
    cap = cv2.VideoCapture("rtsp://obabichev-camera-1:9ETR9wu53b3S8CgEUAc7HAmQSFBCs9xW@192.168.0.132:554/stream2")
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FPS, 2)
    return cap


def create_detector():
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
    return detector


def running_loop(camera, detector):
    if camera.isOpened():
        ret, frame = camera.read()
        rects = detector.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=10, minSize=(75, 75))
        return frame, rects
    return None


def save_image(frame, file_name)->None:
    # save image
    path = get_path_to_data() / "processed" / "image_with_cats" / file_name
    cv2.imwrite(str(path), frame)


def save_res(rects, db_conn, file_name):
    for (i, (x, y, w, h)) in enumerate(rects):
        sql = f"INSERT INTO projects(id_frame,id_on_frame,x,y,w,h) VALUES({file_name+str(i)}, {i}, {x}, {y}, {w}, {h})"
        cur = db_conn.cursor()
        cur.execute(sql)
        db_conn.commit()
    return cur.lastrowid


if __name__ == "__main__":
    camera = get_connection_to_camera()
    database = get_path_to_data() / "processed" / "results.db"
    db_conn = create_connection(database)
    detector = create_detector()
    while True:
        res = running_loop(camera, detector)
        if res is not None:
            frame, rects = res
            file_name = datetime.now().second
            if rects:
                save_image(frame, file_name)
                save_res(rects, db_conn, file_name)

    camera.release()

