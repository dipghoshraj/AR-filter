import numpy as np
import dlib, cv2, re

# Loading Face detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("identifiers/facial_model_trained.dat")


def image_crop(frame, points, masked=False, crooped =True):
    """
    """

    if masked:
        mask = np.zeros_like(frame)
        mask = cv2.fillPoly(mask, [points], (255,255,255))
        frame = cv2.bitwise_and(frame, mask)

        # cv2.imshow("lip mask", frame)
    if crooped:
        bbox = cv2.boundingRect(points)
        x,y,w,h = bbox
        img_crop = frame[y: y+h, x: x+w]
        img_crop = cv2.resize(img_crop, (0,0), None, 0.5, 0.5)
        return img_crop
    else:
        return mask


def get_face_points(gray_frame, face):
    """
    """
    land_mark = predictor(gray_frame, face)
    face_points = []
    for n in range(68):
        x, y = land_mark.part(n).x, land_mark.part(n).y
        face_points.append([x,y])

    return face_points


def merge_images(frame, lips_point_upper, lips_point_bottom, color_b, color_g, color_r):
    lips_point_upper = np.array(lips_point_upper)
    lips_point_bottom = np.array(lips_point_bottom)

    crop_img_lip1 = image_crop(frame, lips_point_upper, masked=True, crooped=False)
    crop_img_lip2 = image_crop(frame, lips_point_bottom, masked=True, crooped=False)

    imgcolorlips_1 = np.zeros_like(crop_img_lip1)
    imgcolorlips_1[:] = color_b, color_g, color_r

    imgcolorlips_upper = cv2.bitwise_and(crop_img_lip1, imgcolorlips_1)
    imgcolorlips_lower = cv2.bitwise_and(crop_img_lip2, imgcolorlips_1)

    imgcolorlips_upper = cv2.GaussianBlur(imgcolorlips_upper, (7,7), 10)
    imgcolorlips_lower = cv2.GaussianBlur(imgcolorlips_lower, (7,7), 10)

    imgcolorlips_upper = cv2.addWeighted(frame, 0.7, imgcolorlips_upper, 0.3, 0)
    imgcolorlips_lower = cv2.addWeighted(imgcolorlips_upper, 0.7, imgcolorlips_lower, 0.3, 0)

    return imgcolorlips_lower


def detection(frame, color_b, color_g, color_r):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(frame)
    
    if faces:
        for face in faces:
            final_face = face_analysis(face, color_b, color_g, color_r, gray_frame, frame)
            return final_face
    return None


def face_analysis(face, color_b, color_g, color_r, gray_frame, frame ):
    x1, y1 = face.left(), face.top()
    x2, y2 = face.right(), face.bottom()
    face_points = get_face_points(gray_frame, face)
    
    index_list_lip1 = [48, 60,67, 66,65,64,54, 55,56,57,58,59]
    index_list_lip2 = [48,60,49,50,51,52,53,54,64,63,62,61]
    lips_point_upper = [face_points[index] for index in index_list_lip1]
    lips_point_bottom = [face_points[index] for index in index_list_lip2]
    
    marged_img_op = merge_images(frame, lips_point_upper, lips_point_bottom, color_b, color_g, color_r)
    return marged_img_op


def increase_brightness(img, value=60):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img