from PIL import Image
from lib.lips_marger import detection
import cv2, imutils, io
import numpy as np


def imageProcessor(image, colors):
    """
    """

    blob = image.read()
    B, G, R = colors.split(',')

    b = io.BytesIO(blob)
    pimg = Image.open(b).convert('RGB')

    # converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
    dataframe = detection(frame, B, G, R)
    if dataframe is not None:
        frame = dataframe
    frame = imutils.resize(frame, width=300)
    imgencode = cv2.imencode('.jpg', frame)[1]

    return imgencode
