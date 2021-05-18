import signal
import sys
import time
import os
import cv2
if(sys.platform == "win32"):
    import win32api
    import win32con
import pyautogui
import numpy
import skimage.metrics

def signal_term_handler(signal, frame):
    print("Terminated")
    sys.exit(0)

def mouseClickWindows(x, y):
    if (sys.argv[1] == "terraria"):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    if (sys.argv[1] == "minecraft"):
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)

def mouseClickLinux(x, y):
    #pyautogui.moveTo(x, y)
    #os.system("xdotool click 1") # left click
    if (sys.argv[1] == "minecraft"):
        pyautogui.click(button="right")

def throwFishingLine(x, y):
    print("throw")
    if(sys.platform == "win32"):
        mouseClickWindows(x, y)
        win32api.SetCursorPos((x, y + 100))

    if (sys.platform == "linux"):
        mouseClickLinux(x, y)
        #pyautogui.move(x, y + 100)

def getFishingLineImage(x, y):
    image = pyautogui.screenshot(region=(x - 50, y - 50, 100, 100))#top left corner, width, height
    #image.save("prova.png")
    image = numpy.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return image

def getFishingLine(x, y):
    print("get")
    if(sys.platform == "win32"):
        win32api.SetCursorPos((x, y))
        mouseClickWindows(x, y)

    if (sys.platform == "linux"):
        #pyautogui.move(x, y)
        mouseClickLinux(x, y)

def fishing():

    if (sys.platform == "win32"):
        (x, y) = win32api.GetCursorPos()
    if (sys.platform == "linux"):
        (x, y) = pyautogui.position()

    throwFishingLine(x, y) # start fishing
    time.sleep(0.5)

    #time.sleep(1)
    first = getFishingLineImage(x, y) # get the first fishing image
    catch = False
    #time.sleep(1)

    while(not(catch)):
        newImage = getFishingLineImage(x, y) # get the actual fishing image
        (score, diff) = skimage.metrics.structural_similarity(first, newImage, full = True) # compare the two images
        diff = (diff * 255).astype("uint8")
        print("SSIM: {}".format(score) + ", "  + str(score))
        if(score < 0.87): # if the similarity is less than 0.8
            catch = True # catch the fish

    getFishingLine(x, y)

def main():

    signal.signal(signal.SIGTERM, signal_term_handler)

    # get mouse positions
    if (sys.platform == "win32"):
        (x, y) = win32api.GetCursorPos()
        mouseClickWindows(x, y)  # focus on the game
        time.sleep(0.5)

    if (sys.platform == "linux"):
        (x, y) = pyautogui.position()
        #mouseClickLinux(x, y)
        time.sleep(0.5)

    while(1):
        fishing()
        time.sleep(0.5)


if __name__ == "__main__":
    main()