import signal
import sys
import time
import cv2
import win32api
import win32con
import pyautogui
import numpy
import skimage.metrics

def signal_term_handler(signal, frame):
    print("Terminated")
    sys.exit(0)

def mouseClick(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def throwFishingLine(x, y):
    mouseClick(x, y)
    win32api.SetCursorPos((x, y + 100))

def getFishingLineImage(x, y):
    image = pyautogui.screenshot(region=(x - 30, y - 30, 60, 60))#top left corner, width, height
    image.save("prova.png")
    image = numpy.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return image

def getFishingLine(x, y):
    win32api.SetCursorPos((x, y))
    mouseClick(x, y)

def imageCompare(image1, image2):
    #convert to gray scale
    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)


def fishing():
    #get mouse positions
    (x, y) = win32api.GetCursorPos()

    mouseClick(x, y)
    time.sleep(0.5)

    throwFishingLine(x, y)

    time.sleep(1)
    first = getFishingLineImage(x, y)
    catch = False

    #file = open("prove.txt", "w")

    while(not(catch)):
        newImage = getFishingLineImage(x, y)
        (score, diff) = skimage.metrics.structural_similarity(first, newImage, full = True)
        diff = (diff * 255).astype("uint8")
        #file.write("SSIM: {}".format(score) + "\n")
        print("SSIM: {}".format(score) + ", "  + str(score))
        if(score < 0.8):
            catch = True
        #time.sleep(0.5)

    #file.close()
    getFishingLine(x, y)


    #mouseClick(x, y)
    #win32api.SetCursorPos((x, y + 100))
    #pyautogui.moveTo(x, y+100)
    #time.sleep(1)
    #win32api.SetCursorPos([x, y])

    #while(1):
        #print(str(x) + ", " + str(y))

def main():

    signal.signal(signal.SIGTERM, signal_term_handler)

    while(1):
        fishing()


if __name__ == "__main__":
    main()