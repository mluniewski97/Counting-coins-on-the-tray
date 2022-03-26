import numpy as np
import cv2 as cv

img = cv.imread('tray1.jpg', 0)

# Pieniadze

img = cv.medianBlur(img,5)
cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1.4, 40, param1=200, param2=60, minRadius=20, maxRadius=45)
circles = np.uint16(np.around(circles))

# Linie

img = cv.imread('tray1.jpg', cv.IMREAD_COLOR)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
edges = cv.Canny(gray, 50, 150, apertureSize=3)
lines = cv.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=10, maxLineGap=30)

minX = 9999
maxX = 0
minY = 9999
maxY = 0
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv.line(cimg, (x1, y1), (x2, y2), (255, 0, 0), 2)
    if x1 < minX:
        minX = x1
    if x2 < minX:
        minX = x1

    if y1 < minY:
        minY = y1
    if y2 < minY:
        minY = y1

    if x1 > maxX:
        maxX = x1
    if x2 > maxX:
        maxX = x1

    if y1 > maxY:
        maxY = y1
    if y2 > maxY:
        maxY = y1

# MONETY

coinIn = 0
moneyIn = 0.0
coinOut = 0
moneyOut = 0.0

for i in circles[0, :]:  # BGR
    small = False
    # zewnetrzne
    if i[2] < 33:
        cv.circle(cimg, (i[0], i[1]), i[2], (255, 0, 0), 2)
        small = True
    else:
        cv.circle(cimg, (i[0], i[1]), i[2], (0, 0, 255), 2)

    # wewnetrzne
    if minX < i[0] and i[0] < maxX and minY < i[1] and i[1] < maxY:
        cv.circle(cimg, (i[0], i[1]), 2, (0, 255, 0), 3)
        coinIn = coinIn + 1
        if small:
            moneyIn = moneyIn + 0.05
        else:
            moneyIn = moneyIn + 5.0
    else:
        cv.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)
        coinOut = coinOut + 1
        if small:
            moneyOut = moneyOut + 0.05
        else:
            moneyOut = moneyOut + 5.0

result = "Liczba monet w tacy: " + str(coinIn) + "\t\n" + "Liczba monet poza taca: " + str(coinOut) + "\t\n"\
         + "Ilosc zl w tacy: " + str(round(moneyIn,2)) + " PLN \t\n" + "Ilosc zl poza taca: " + str(round(moneyOut,2)) + " PLN"
print(result)
cv.imshow('detected circles',cimg)
cv.waitKey(0)
cv.destroyAllWindows()


