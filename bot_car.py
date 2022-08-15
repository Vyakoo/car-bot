from keyboard import press, release, send
from time import sleep

import cv2
import numpy as np
import mss


mss = mss.mss()

vertex1 = np.array([[0, 770], [0, 650], [600, 650], [640, 770]]) # Mask coordinates 1
vertex2 = np.array([[640, 770], [680, 650], [1280, 650], [1280, 770]]) # Mask coordinates 2

x1 = 0
y1 = 0

x2 = 0
y2 = 0

rotate_1 = 0
rotate_2 = 0


def Line1(screen, lines): 	# Drawing lines 1
	global x1
	global y1
	try:
		for line in lines:
			cor = line[0]
			cv2.line(screen, (cor[0], cor[1]), (cor[2], cor[3]), [0, 0, 255], 5)

			x1 = lines[0][0][0]
			y1 = lines[0][0][1]
	except:
		pass

def Line2(screen, lines): 	# Drawing lines 1
	global x2 
	global y2
	try:
		for line in lines:
			cor = line[0]
			cv2.line(screen, (cor[0], cor[1]), (cor[2], cor[3]), [0, 0, 255], 5)

			x2 = lines[0][0][0]
			y2 = lines[0][0][1]
	except:
		pass


def mask(screen, vertex): 	# Applying a mask
	mask = np.zeros_like(screen)
	cv2.fillPoly(mask, np.int32([vertex]), 255)
	mask1 = cv2.bitwise_and(screen, mask)
	return mask1

sleep(5)

while True: # Main cycle

	mon = {
	"top": 0,
	"left": 0,
	"width": 1280, 
	"height": 1024
	}
	windows = np.array(mss.grab(mon))


	img = cv2.cvtColor(windows, cv2.COLOR_BGR2GRAY)

	blur = cv2.GaussianBlur(img, (5,5), 0) # Image contours
	can = cv2.Canny(blur, 30, 200, 3)
	can_mask1 = mask(can, vertex1)
	can_mask2 = mask(can, vertex2)

	lines1 = cv2.HoughLinesP(can_mask1, 1, np.pi/180, 10, 300, 10)
	lines2 = cv2.HoughLinesP(can_mask2, 1, np.pi/180, 10, 300, 10) 	# Определяем линии

	Line1(windows, lines1) 	# Рисуем в функции данные левой линии 
	cv2.line(windows, (x1, y1), (550, 750), [0, 255, 50], 5) 
	length_1 = int(np.sqrt((x1 - 550) ** 2 + (y1 - 750) ** 2)) # Растояние от машины до границы

	Line2(windows, lines2) 	# Рисуем в функции данные правой линии
	cv2.line(windows, (x2, y2), (700, 750), [0, 255, 50], 5) 
	length_2 = int(np.sqrt((x2 - 700) ** 2 + (y2 - 750) ** 2)) # Растояние от машины до границы

	

	if rotate_1 > length_1 and rotate_2 < length_2: # Поворот налево
		press('a')
		press('w')
		sleep(0.2)
		release('a')
		release('w')
	elif rotate_1 < length_1 and rotate_2 > length_2: # Поворот направо
		press('d')
		press('w')
		sleep(0.2)
		release('d')
		release('w')
	elif rotate_1 < length_1 and rotate_2 < length_2: # Езда прямо
		press('s')
		sleep(0.2)
		release('s')
	else:
		press('w')
		sleep(0.05)
		release('w')
		send('s')


	rotate_2 = length_2
	rotate_1 = length_1

	cv2.imshow('img', windows) 	# Turning the window on and off
	if cv2.waitKey(1)==ord('q'):
		cv2.destroyAllWindows()
		break