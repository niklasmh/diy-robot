import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import sys
import os

isPI = os.uname().nodename == "raspberrypi"
flipY = False
flipX = False
folder = "images/"
camera_image = folder + "camera1.png"
floor_image = folder + "floor4.png"
debug = False
try:
    if len(sys.argv) > 1:
        camera_image = folder + f"camera{int(sys.argv[1])}.png"
        debug = True
    if len(sys.argv) > 2:
        floor_image = folder + f"floor{int(sys.argv[2])}.png"
except:
    print("CLI arguments: <camera-number> <floor-number>")

# Find the ideal canny bounds
base_image = cv.imread(floor_image)
grey_image = cv.cvtColor(base_image, cv.COLOR_BGR2GRAY)
v = np.median(grey_image)


def canny(img, l, u, output, plot=False):
    # Apply canny
    image = cv.Canny(img, l, u)
    if debug:
        if plot:
            plt.imshow(image, 'gray')
        if output:
            plt.imsave(fname=output, arr=image, cmap='gray', format='png')
    return image


def capture(output):
    from picamera import PiCamera
    camera = PiCamera()
    camera.capture(output,)
    camera.close()


def locate(assumed_position=[0, 0], capture_new_image=False, sigma=0.33):
    """
    Find the most probable position of the robot.
    """
    global camera_image
    lower = 20  # int(max(0, (1.0 - sigma) * v))
    upper = 10  # int(min(255, (1.0 + sigma) * v))
    print(lower, upper)

    if isPI:
        camera_image = "static/camera.png"
        if capture_new_image:
            capture("static/camera.png", resize=(56, 56))

    # Make a canny of part of the floor
    # around the assumed position
    # TODO: Crop image
    # TODO: Rotate image
    img = cv.imread(floor_image, 0)
    if flipX:
        img = cv.flip(img, 1)
    if flipY:
        img = cv.flip(img, 0)
    floor = canny(img, lower, upper, folder + "canny_floor.png", True)

    # Make a canny of the camera shot
    img = cv.imread(camera_image, 0)
    if flipX:
        img = cv.flip(img, 1)
    if flipY:
        img = cv.flip(img, 0)
    height, width = img.shape[:2]
    camera = canny(img, lower, upper, folder + "canny_camera.png")

    # Add canny image to webserver
    if isPI:
        plt.imsave(fname="static/canny_camera.png",
                   arr=camera, cmap='gray', format='png')

    if debug:
        print("Canny done")

    # Set general hough transform template
    ght = cv.createGeneralizedHoughBallard()
    ght.setTemplate(camera)
    ght.setVotesThreshold(250)

    # Find the position in the image!
    [positions, votes] = ght.detect(floor)
    if positions is None:
        print("Could not find any matches!")
        return np.array([])
    positions = positions[0]

    if debug:
        print("Gotten positions")
        print("Plotting!")
        xs = [int(position[0]) for position in positions[1:]]
        ys = [int(position[1]) for position in positions[1:]]
        plt.scatter(x=xs, y=ys, c='r')

        xs = [int(position[0]) for position in positions[:1]]
        ys = [int(position[1]) for position in positions[:1]]
        plt.scatter(x=xs, y=ys, c='g')

        plt.savefig(folder + "result.png")

    # Calculate the actual position relative to
    # the origin of the floor
    # TODO: Calc position
    return positions[0][:2]


if __name__ == '__main__':
    locate([10, 10])
