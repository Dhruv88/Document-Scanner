import cv2 as cv
from numpy.lib.function_base import copy
import numpy as np

class Document_Detector:
    def __init__(self, image):
        self.__image = image
        self.__processed_image = None
        self.__largest_contour = None
        self.__corners = None

    def __is_landscape(self):
        return self.__image.shape[0] < self.__image.shape[1]

    def __rotate_image_if_is_landscape(self):
        if self.__is_landscape():
            self.__image = cv.rotate(self.__image,rotateCode=cv.ROTATE_90_CLOCKWISE)

    def __resize_image(self, new_size=(400,720)):
        self.__image = cv.resize(self.__image, (400, 720))

    def __color_to_grayscale(self):
        self.__processed_image = cv.cvtColor(self.__image,cv.COLOR_BGR2GRAY)

    def __blur_image(self, kernel_size=(3,3)):
        self.__processed_image = cv.GaussianBlur(self.__processed_image, kernel_size,0,0, cv.BORDER_DEFAULT)
        self.__processed_image = cv.medianBlur(self.__processed_image, 5)

    def __detect_edges(self):
        self.__processed_image = cv.Laplacian(self.__processed_image,cv.CV_8U,ksize=3)
        
    def __make_binary_image_and_dilate(self):
        ret, self.__processed_image = cv.threshold(self.__processed_image,0,255,cv.THRESH_OTSU)
        kernel = np.ones((3,3),np.uint8)
        self.__processed_image = cv.dilate(self.__processed_image,kernel,iterations=3)
    
    def __essential_preprocessing(self):
        self.__rotate_image_if_is_landscape()
        self.__resize_image()
        self.__color_to_grayscale()
    
    def __preprocessing_for_camera_image(self):
        self.__essential_preprocessing()
        self.__blur_image(kernel_size=(11,11))
        self.__make_binary_image_and_dilate()
    
    def __preprocessing_for_gallery_image(self):
        self.__essential_preprocessing()
        self.__blur_image()
        self.__detect_edges()
        self.__make_binary_image_and_dilate()
    
    def __prepare_preprocessed_image(self,from_camera=0):
        if from_camera:
            self.__preprocessing_for_camera_image()
        else:
            self.__preprocessing_for_gallery_image()
    def __find_largest_contour(self):
        contours, hierarchy = cv.findContours(self.__processed_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        self.__largest_contour = sorted(contours,  key=lambda x: cv.contourArea(x), reverse=True)[:1]
        # print(self.__largest_contour)

    def __extract_corners(self):
        epsilon = 0.051 * cv.arcLength(self.__largest_contour[0], True)
        self.__corners = cv.approxPolyDP(self.__largest_contour[0], epsilon, True)
    
    def __is_document_rectangle(self):
        return len(self.__corners)==4
    
    def __mark_document_boundary(self):
        cv.drawContours(self.__image, [self.__corners], 0, [0,255,0], 3)


    def detect_document(self, from_camera=0):
        self.__prepare_preprocessed_image(from_camera)
        # cv.imshow('IPWebca', self.image)
        self.__find_largest_contour()
        self.__extract_corners()
        unmarked_image = copy(self.__image)
        if self.__is_document_rectangle():
            self.__mark_document_boundary()
        return (unmarked_image,self.__image,self.__corners)
    




    

    
