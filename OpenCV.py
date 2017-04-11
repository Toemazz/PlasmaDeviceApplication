# Engineer: Thomas Reaney
# College: National University of Ireland Galway
# Date: 12/03/2017
from ImageManipulation import *
import cv2

logging.basicConfig(filename="PlasmaDevice.log", level=logging.INFO)


# Method: Used for manual edge detection
def manual_edge_detection(in_file_name, out_file_name, lower, upper):
    """
    :param in_file_name: Input file name
    :param out_file_name: Output file name
    :param lower: Lower limit
    :param upper: Upper limit
    :return: Image with edges detected
    """
    img = cv2.imread(in_file_name, 0)
    img = cv2.Canny(img, lower, upper)
    cv2.imwrite(out_file_name, img)


# Method: Used for automatic edge detection
def auto_edge_detection(file_name, sigma=0.33):
    """
    :param file_name: File name of image
    :param sigma: Edge detection value
    :return: Image with edges detected
    """
    logging.info("Automatic Edge Detection: Starting......")
    img = cv2.imread(file_name, 0)
    # Calculates the median of the pixel intensities
    med = np.median(img)
    # Calculates best possible lower and upper thresholds
    lower = int(max(0, (1.0 - sigma) * med))
    upper = int(min(255, (1.0 + sigma) * med))
    output = cv2.Canny(img, lower, upper)

    cv2.imshow("Automatic Edge Detection", output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    logging.info("Automatic Edge Detection: Finishing......")


# Method: Used to create an image using pixel averaging
def pixel_averaging(file_dir, output_file_name):
    """
    :param file_dir: File directory
    :param output_file_name: File name of final image
    :return: Reconstructed greyscale image
    """
    logging.info("Pixel Averaging: Starting.....")
    num_images = 0
    total_pixels = np.zeros((60, 80))
    # Get list of .jpg files
    files = [file_name for file_name in os.listdir(file_dir) if
             file_name.endswith(".jpg") and file_name.startswith("rgb")]

    if files:
        for file_name in files:
            file_name = os.path.join(file_dir, file_name)
            image = cv2.imread(file_name)
            height, width, channels = image.shape
            if channels > 1:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            for i in range(height):
                for j in range(width):
                    total_pixels[i, j] += image[i, j]
            num_images += 1
        print("Pixel averaging completed")
    else:
        raise FileNotFoundError
    logging.info("Pixel Averaging: Calculate the average for each pixel on each image")

    # Average the pixels
    mean_pixels = np.floor(np.divide(total_pixels, num_images))
    # Scale the pixels to between 0 and 255
    scaled_pixels = scale_pixels(mean_pixels)
    # Save image
    cv2.imwrite(output_file_name, scaled_pixels)
    logging.info("Pixel Averaging: Finishing.....")


# Method: Used to create an image using image blending
def image_blending(file_dir, output_file_name):
    """
    :param file_dir: File directory
    :param output_file_name: File name of final image
    :return: Reconstructed greyscale image
    """
    logging.info("Image Blending: Starting.....")
    # Get list of .jpg files
    files = [file_name for file_name in os.listdir(file_dir) if
             file_name.endswith(".jpg") and file_name.startswith("rgb")]
    # Parameters for image blending
    beta = float(1.0 / len(files))
    alpha = 1.0 - beta

    logging.info("Image Blending: Blend all images in the file directory specified")

    if files:
        # Initialise blended image to first image
        blended_img = 0

        for i in range(len(files)):
            files[i] = os.path.join(file_dir, files[i])
            if i == 0:
                img1 = cv2.imread(files[i])
                img2 = img1
            else:
                img1 = cv2.imread(files[i])
                img2 = cv2.imread(files[i-1])
            # Blend images
            blended_img = cv2.addWeighted(src1=img1, alpha=alpha, src2=img2, beta=beta, gamma=1)
        # Save image
        cv2.imwrite(output_file_name, blended_img)
        print("Image blending completed")
    else:
        raise FileNotFoundError
    logging.info("Image Blending: Finishing.....")


# Method: Used to create an image using thresholding
def thresholding(file_dir, output_file_name, threshold=200):
    """
    :param file_dir: File directory
    :param output_file_name: Name of output file name
    :param threshold: Threshold for removing noise
    :return: Reconstructed greyscale image
    """
    logging.info("Feature Extraction: Starting.....")
    # Get list of .jpg files
    files = [file_name for file_name in os.listdir(file_dir) if
             file_name.endswith(".jpg") and file_name.startswith("rgb")]
    # Initialise white image
    output_img = np.zeros((60, 80, 1), np.uint8)
    output_img[:] = 255

    logging.info("Feature Extraction: Set the pixels with an intensity above the threshold to black")

    if files:
        for file_name in files:
            file_name = os.path.join(file_dir, file_name)
            img = cv2.imread(file_name)

            height, width, channels = img.shape
            # If not greyscale, convert to greyscale
            if channels > 1:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Apply threshold
            for i in range(height):
                for j in range(width):
                    if img[i, j] > threshold:
                        # Set to black
                        output_img[i, j] = 0
        # Save image
        cv2.imwrite(output_file_name, output_img)
        print("Feature extraction completed")
    else:
        raise FileNotFoundError
    logging.info("Feature Extraction: Starting.....")


# Method: Used to add the
def add_limits_to_image(img, colour, inner_radius=130, outer_radius=200):
    """
    :param img: Input image
    :param inner_radius: Inner radius size
    :param outer_radius: Outer radius size
    :param colour: Colour for limits on images
    :return: Image with limits
    """
    logging.info("Add Limits to Image: Starting.....")
    # Get centre point
    center = get_image_centre_point(img)
    # Add center point to the image
    cv2.circle(img=img, center=center, radius=2,  color=colour, thickness=2)
    # Add inner circle to the image
    cv2.circle(img=img, center=center, radius=inner_radius, color=colour, thickness=2)
    # Add outer circle to the image
    cv2.circle(img=img, center=center, radius=outer_radius, color=colour, thickness=2)

    print("Limits added to image")
    logging.info("Add Limits to Image: Finishing.....")
    return img


# Method: Used to detect circles
def circle_detection(file_name, dp, min_dist, param1, param2, min_radius, max_radius):
    """
    :param file_name: Name of image file
    :param dp: Image resolution
    :param min_dist: Minimum distance between the centers of the detected circles
    :param param1: Upper Canny edge detection threshold
    :param param2: Accumulator threshold
    :param min_radius: Minimum radius
    :param max_radius: Maximum radius
    :return: Detected center point, Image with detected circles
    """
    logging.info("Circle Detection: Starting......")
    img = cv2.imread(file_name, 0)
    #  Smooth edges
    img = cv2.medianBlur(img, 5)
    # Detect circles
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT,
                               dp=dp, minDist=min_dist,
                               param1=param1, param2=param2,
                               minRadius=min_radius, maxRadius=max_radius)
    center = ()
    # Convert to greyscale
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        if len(circles[0, :]) > 0:
            # Randomly pick a center point if there is more than one
            circle = circles[0, :][0]
            center = (int(circle[0]), int(circle[1]))
            print("Circle Detection: Detected circles added to image")
    else:
        print("Circle Detection: No circles found in image")
    logging.info("Circle Detection: Finishing......")
    return center, img


# Method: Used to draw a line between two points
def draw_line_between_two_points(img, point_1, point_2):
    """
    :param img: Input image
    :param point_1: Point 1
    :param point_2: Point 2
    :return: Output image
    """
    # Draw line
    cv2.line(img=img, pt1=point_1, pt2=point_2, color=(0, 0, 0), thickness=2)

    return img
