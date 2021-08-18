import cv2 as cv
import numpy as np
import math

class Scanner:
    def __init__(self,image,corners):
        self.__image = image
        self.__original_corners = np.array(corners).astype(np.float32)
        self.__length_of_scanned_document = self.__calculate_length()
        self.__width_of_scanned_document = self.__calculate_width()
        self.transformed_corners = self.__get_transformed_corners()

    def __calculate_distance(self, point_1, point_2):
        return int(math.sqrt((point_1[0]-point_2[0])**2+(point_1[1]-point_2[1])**2))

    def __calculate_length(self):
        return self.__calculate_distance(self.__original_corners[0],self.__original_corners[1])

    def __calculate_width(self):
        return self.__calculate_distance(self.__original_corners[0],self.__original_corners[2])

    def __get_transformed_corners(self):    
        return np.array([[0,0],[self.__length_of_scanned_document,0],[0,self.__width_of_scanned_document],[self.__length_of_scanned_document,self.__width_of_scanned_document]]).astype(np.float32)

    def __trim_borders(self,image):
        return image[5:self.__width_of_scanned_document-5,5:self.__length_of_scanned_document-5]

    def scan_document(self):
       transformation_matrix, _ = cv.findHomography(self.__original_corners,self.transformed_corners)
       transformed_image = cv.warpPerspective(self.__image, transformation_matrix, (self.__image.shape[1], self.__image.shape[0]))
       trimmed_image = self.__trim_borders(image=transformed_image)
       scanned_document = cv.resize(trimmed_image,(int(self.__length_of_scanned_document*1.3),int(self.__width_of_scanned_document*1.3)))
       return scanned_document
