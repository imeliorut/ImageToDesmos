import cv2 as cv
import numpy as np
import potrace


def bezier_formula(_path):
    a = []
    for i, curve in enumerate(_path):
        x1, y1 = curve.start_point.x, curve.start_point.y
        for segment in curve:
            x4, y4 = segment.end_point.x, segment.end_point.y
            if segment.is_corner:
                x2, y2, x3, y3 = segment.c.x, segment.c.y, segment.c.x, segment.c.y
            else:
                x2, y2 = segment.c1.x, segment.c1.y
                x3, y3 = segment.c2.x, segment.c2.y
            s = rf"\left(\left(1-t\right)^[3]\left({x1}\right)\ +3\left(1-t\right)^[2]t\left({x2}\right)+3\left(1-t\right)t^[2]\left({x3}\right)+t^[3]\left({x4}\right),\ \left(1-t\right)^[3]\left({y1}\right)\ +3\left(1-t\right)^[2]t\left({y2}\right)+3\left(1-t\right)t^[2]\left({y3}\right)+t^[3]\left({y4}\right)\right)"
            s = s.replace('[', '{').replace(']', '}')
            a.append(s)
            x1, y1 = segment.end_point.x, segment.end_point.y
    return a


def get_bezier_formula(file):
    img_data = file.read()
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_GRAYSCALE)
    img = cv.blur(img, (2, 2))
    edges = cv.Canny(img, 100, 150)
    border_size = 15
    edges = cv.copyMakeBorder(
        edges,
        top=border_size,
        bottom=border_size,
        left=border_size,
        right=border_size,
        borderType=cv.BORDER_CONSTANT,
        value=[0, 0, 0]
    )
    kernel = np.ones((10, 10), np.uint8)
    edges = cv.dilate(edges, kernel, iterations=1)
    kernel = np.ones((10, 10), np.uint8)
    edges = cv.erode(edges, kernel, iterations=1)
    edges = ~edges
    edges = cv.flip(edges, 0)
    bmp = potrace.Bitmap(edges)
    path = bmp.trace()
    return bezier_formula(path), edges.shape
