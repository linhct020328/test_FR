import cv2
import os

def start_dataset(face_id, name):
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video width
    cam.set(4, 480)  # set video height

    face_detector = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')
    font2 = cv2.FONT_HERSHEY_DUPLEX
    count = 0
    try:
        os.makedirs("dataset")
    except:
        print('Directory Already Created')

    while True:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 7)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
            new_img = (gray[y:y + h, x:x + w])

        cv2.putText(frame, "Number of images:" + str(count), (10,20), font2, 1, (0, 255, 0), 1)

        cv2.imshow('frame', frame)
        try:
            p = "dataset/User." + str(face_id) + '.' + str(count) + '.jpg'#+ '.' + name
            cv2.imwrite(p, new_img)
            count += 1
        except:
            pass

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == 27 or count >= 100:
            break

    print("[INFO] {} face images stored".format(count))
    print("[INFO] cleaning up...")
    cv2.destroyAllWindows()
    return count
