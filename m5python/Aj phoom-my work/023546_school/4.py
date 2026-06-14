import cv2 as cv
img = cv.imread('m5python/Aj phoom-my work/023546_school/R.jpg')

def click_posistion(event,x,y,flages,param):
    if event == cv.EVENT_LBUTTONDOWN:
        cv.putText(img,'totoro',(x,y),1,3,(255,223,194),3)
        cv.imshow('click puttext',img)
cv.imshow('click puttext',img)
cv.setMouseCallback('click puttext',click_posistion)
cv.waitKey(0)
cv.destroyAllWindows()