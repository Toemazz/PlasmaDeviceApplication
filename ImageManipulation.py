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

logging.basicConfig(filename="PlasmaDevice.log", level=logging.INFO)


# Method: Used to create a .gif file from a  number of .jpg images
def jpg_to_gif(file_dir, output_file_name):
    """
    :param file_dir: File directory
    :param output_file_name: Output filename
    :return: GIF file
    """
    logging.info("JPG -> GIF: Starting.....")

    files = [os.path.join(file_dir, file_name) for file_name in os.listdir(file_dir) if
             file_name.endswith(".jpg") and file_name.startswith("rgb")]

    if files:
        # Create GIF
        with imageio.get_writer(output_file_name, mode="I") as writer:
            for img in files:
                writer.append_data(imageio.imread(img))
        print("GIF created")
    else:
        print("Unable to create GIF")

    logging.info("JPG -> GIF: Finishing.....")


# Method: Used to create a .mp4 file from a  number of .jpg images
def jpg_to_mp4(file_dir, output_file_name):
    """
    :param file_dir: File directory
    :param output_file_name:  Output filename
    :return: .mp4 file
    """
    logging.info("JPG -> MP4: Starting.....")

    files = [os.path.join(file_dir, file_name) for file_name in os.listdir(file_dir) if file_name.endswith(".jpg")]

    if files:
        images = [cv2.imread(files[i], 0) for i in range(len(files))]
        width, height = images[0].shape

        fourcc = cv2.VideoWriter_fourcc(*"MPEG")
        video = cv2.VideoWriter(filename=output_file_name, fourcc=fourcc, fps=5.0, frameSize=(width, height), isColor=True)

        for i in range(len(images)):
            video.write(images[i])

        cv2.destroyAllWindows()
        video.release()
        print("MP4 file created")
    else:
        print("Unable to create MP4")
    logging.info("JPG -> MP4: Finishing.....")


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
    print("Image re-sized")
    logging.info("Re-Size Image: Finishing.....")


# Method: Used to scale pixel values to between an upper and lower limit
def scale_pixels(avg_pixels, scale_min=0, scale_max=255):
    """
    :param avg_pixels: Averaged pixel values
    :param scale_min: Minimum scaled value (Default=0)
    :param scale_max: Maximum scaled value (Default=255)
    :return: avg_pixels: Scaled averaged pixel values
    """
    logging.info("Scale Pixels: Starting.....")
    pixel_min, pixel_max = np.min(avg_pixels), np.max(avg_pixels)

    logging.info("Scale Pixels: Convert pixel values to a range between 0 and 255")

    for i in range(np.size(avg_pixels, axis=0)):
        for j in range(np.size(avg_pixels, axis=1)):
            pixel_val = avg_pixels[i, j]
            scaled_pixel_val = (pixel_val - pixel_min) * (scale_max - scale_min) / (pixel_max - pixel_min)
            scaled_pixel_val = np.floor(scaled_pixel_val)
            avg_pixels[i, j] = scaled_pixel_val

    logging.info("Scale Pixels: Starting.....")
    return avg_pixels


# Method: Used to the centre point of an image
def get_image_centre_point(img):
    """
    :param img: Image file
    :return: Centre point of the image
    """
    height, width, channels = img.shape

    # Get center point
    return int(np.floor(width / 2)), int(np.floor(height / 2))
