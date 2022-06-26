import cv2
import os

def getDataset(name):
	path = "./dataset/" + name
	cascadePath = "./cascades/haarcascade_frontalface_default.xml"
	detector = cv2.CascadeClassifier(cascadePath)

	try:
		os.makedirs(path)
	except:
		print('Directory Already Created')

	cam = cv2.VideoCapture(0)
	cam.set(3, 640)  # set video widht
	cam.set(4, 480)  # set video height

	minW = 0.1 * cam.get(3)
	minH = 0.1 * cam.get(4)
	total = 0
	font2 = cv2.FONT_HERSHEY_DUPLEX
	while True:
		ret, frame = cam.read()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		rects = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=7, minSize=(int(minW), int(minH)))

		for (x, y, w, h) in rects:
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			new_img = (gray[y:y + h, x:x + w]).copy()

		cv2.putText(frame,"Number of images:" + str(total), (10, 20), font2, 1, (0, 255, 0), 1)

		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		try:
			p = str(path+"/"+str(total).zfill(5)+".jpg")
			cv2.imwrite(p, new_img)
			total += 1
		except:
			pass

		if key == ord("q") or key == 27 or total >= 10:
			break

	print("[INFO] {} face images stored".format(total))
	print("[INFO] cleaning up...")
	cv2.destroyAllWindows()
	return total
	# cam.stop()
