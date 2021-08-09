import cv2
from numpy.lib.function_base import copy
# import image using opencv
# img = cv2.imread('doc.jpg') #second parameter 0,1 or 2 to get that color channel of the image
import numpy as np
import math
import matplotlib as mp
import tkinter as tk
from detector import Document_Detector
from scanner import Scanner


URL = "http://192.168.79.41:8080/video"
# cam = cv2.VideoCapture(URL)
captured_image = None
document_corners = None

while True:
    # check, img = cam.read()
    img = cv2.imread("doc2.jpg")
    detector = Document_Detector(image=img)
    unmarked_image,detected_img,corners = detector.detect_document(from_camera=1)
        
    cv2.imshow('IPWebcam', detected_img)
    if cv2.waitKey(1) == ord("1"):
      captured_image = unmarked_image
      document_corners = corners
      cv2.destroyAllWindows()
      break

final_corners = []
for i in range(len(document_corners)):
  final_corners.append([document_corners[i][0][0],document_corners[i][0][1]])
final_corners = sorted(final_corners, key = lambda x:x[1])
arranged_corners = []
arranged_corners.append(min(final_corners[0],final_corners[1],key=lambda x:x[0]))
arranged_corners.append(max(final_corners[0],final_corners[1],key=lambda x:x[0]))
arranged_corners.append(min(final_corners[2],final_corners[3],key=lambda x:x[0]))
arranged_corners.append(max(final_corners[2],final_corners[3],key=lambda x:x[0]))

cp = copy(captured_image)

cv2.circle(cp,tuple(arranged_corners[0]),20,(0,0,255),-1)
cv2.circle(cp,tuple(arranged_corners[1]),20,(0,0,255),-1)
cv2.circle(cp,tuple(arranged_corners[2]),20,(0,0,255),-1)
cv2.circle(cp,tuple(arranged_corners[3]),20,(0,0,255),-1)
cv2.line(cp,tuple(arranged_corners[0]),tuple(arranged_corners[1]),(0,255,0),3)
cv2.line(cp,tuple(arranged_corners[0]),tuple(arranged_corners[2]),(0,255,0),3)
cv2.line(cp,tuple(arranged_corners[3]),tuple(arranged_corners[1]),(0,255,0),3)
cv2.line(cp,tuple(arranged_corners[3]),tuple(arranged_corners[2]),(0,255,0),3)
drawing = False
cv2.imshow('Captured_Image',cp)
def move_corner(event,x,y,flags,param):
  global drawing
 
  if event == cv2.EVENT_LBUTTONDOWN:
    drawing = True

  elif event == cv2.EVENT_MOUSEMOVE:
    if drawing == True:
      for i in range(4):
        dist = int(math.sqrt((arranged_corners[i][0]-x)**2+(arranged_corners[i][1]-y)**2))
        if(dist<=20):
          arranged_corners[i][0] = x
          arranged_corners[i][1] = y
          break
      cp = copy(captured_image)
      cv2.circle(cp,tuple(arranged_corners[0]),20,(0,0,255),-1)
      cv2.circle(cp,tuple(arranged_corners[1]),20,(0,0,255),-1)
      cv2.circle(cp,tuple(arranged_corners[2]),20,(0,0,255),-1)
      cv2.circle(cp,tuple(arranged_corners[3]),20,(0,0,255),-1)
      cv2.line(cp,tuple(arranged_corners[0]),tuple(arranged_corners[1]),(0,255,0),3)
      cv2.line(cp,tuple(arranged_corners[0]),tuple(arranged_corners[2]),(0,255,0),3)
      cv2.line(cp,tuple(arranged_corners[3]),tuple(arranged_corners[1]),(0,255,0),3)
      cv2.line(cp,tuple(arranged_corners[3]),tuple(arranged_corners[2]),(0,255,0),3)
      cv2.imshow('Captured_Image',cp)
  elif event == cv2.EVENT_LBUTTONUP:
    drawing = False

cv2.namedWindow('Captured_Image')
cv2.setMouseCallback('Captured_Image', move_corner)
cv2.waitKey(0)
cv2.destroyAllWindows()


print(final_corners)
print(arranged_corners)
scanner = Scanner(captured_image,arranged_corners)
scanned_document = scanner.scan_document()

cv2.imshow("helo",scanned_document)
# cv2.imshow('IPWebca',img)
# cv2.line(img, (353, 422), (837,737), (255,0,0), 3, cv2.LINE_AA)






# cv2.imshow("hello",thresh)

# cv2.imshow("Detected Lines (in red) - Standard Hough Line Transform", lines)
cv2.waitKey(0)
cv2.destroyAllWindows()