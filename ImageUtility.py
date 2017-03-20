# Engineer: Thomas Reaney
# College: National University of Ireland Galway
# Date: 12/03/2016
import imageio
import os
import cv2
import numpy as np
import logging
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image

logging.basicConfig(filename="ImageUtility.log", level=logging.INFO)


# Method: Used to create a .gif file from a  number of .jpg images
def jpg_to_gif(file_dir, output_file_name):
    """
    :param file_dir: File directory
    :param output_file_name: Output filename
    :return: GIF file
    """
    logging.info("JPG -> GIF: Starting.....")

    files = [file_name for file_name in os.listdir(file_dir) if file_name.endswith(".jpg")]

    # Create GIF
    with imageio.get_writer(output_file_name, mode="I") as writer:
        for img in files:
            writer.append_data(imageio.imread(img))
    logging.info("JPG -> GIF: Finishing.....")


# Method: Used to create a .avi file from a  number of .jpg images
def jpg_to_avi(file_dir, output_file_name):
    """
    :param file_dir: File directory
    :param output_file_name:  Output filename
    :return: .avi file
    """
    logging.info("JPG -> AVI: Starting.....")

    files = [file_name for file_name in os.listdir(file_dir) if file_name.endswith(".jpg")]

    width, height = cv2.imread(files[0], 0).shape
    images = [cv2.imread(files[i], 0) for i in range(len(files))]

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    video = cv2.VideoWriter(filename=output_file_name, fourcc=fourcc, fps=1, frameSize=(width, height), isColor=True)

    for i in range(len(images)):
        video.write(images[i])

    cv2.destroyAllWindows()
    video.release()
    logging.info("JPG -> AVI: Finishing.....")


# Method: Used to create a 3D representation of an image
def plot_image_in_3d(filename):
    """
    :param filename: Filename of the image
    :return: 3D representation of the image
    """
    img = cv2.imread(filename, 0)
    img = cv2.bitwise_not(img)
    x_val, y_val, z_val = [], [], []

    for y in range(len(img)):
        for x in range(len(img[y])):
            x_val.append(int(x))
            y_val.append(int(y))
            z_val.append(int(img[y][x]))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    cmap = plt.get_cmap("jet")
    ax.plot_trisurf(x_val, y_val, z_val, cmap=cmap, linewidth=0.2)
    ax.set_xlabel("Row")
    ax.set_ylabel("Column")
    ax.set_zlabel("Colour")

    plt.show()


# Method: Used to resize image
def resize_image(input_file_name, output_file_name, ratio=8):
    """
    :param input_file_name: Input file name
    :param output_file_name: Output file name
    :param ratio: Scale ratio
    :return: Re-sized image
    """
    logging.info("Re-Size Image: Starting.....")
    # Open image file
    img = Image.open(input_file_name)
    # Scale width and height
    width, height = int(img.size[0]), int(img.size[1])
    new_width, new_height = width*ratio, height*ratio
    # Resize image
    logging.info("Re-Size Image: Image Size Before: (" + str(width) + ", " + str(height) + ")")
    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    logging.info("Re-Size Image: Image Size After: (" + str(new_width) + ", " + str(new_height) + ")")
    # Save image
    img.save(output_file_name)
    logging.info("Re-Size Image: Finishing.....")


# Method: Used to the centre point of an image
def get_image_centre_point(img):
    """
    :param img: Image file
    :return: Centre point of the image
    """
    height, width, channels = img.shape

    # Get center point
    return int(np.floor(width / 2)), int(np.floor(height / 2))


# Method: Used to draw a line between two points
def draw_line_between_two_points(img, point_1, point_2):
    cv2.line(img=img, pt1=point_1, pt2=point_2, color=(0, 0, 0), thickness=2)

    return img
