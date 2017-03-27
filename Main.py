# Engineer: Thomas Reaney
# College: National University of Ireland Galway
# Date: 16/03/2017
from Tests import *
from OpenCV import *
from ImageManipulation import *


# Method: Used to run the image processing on the recorded images
def run_application(file_dir, file_name):
    """
    :param file_dir: File directory
    :param file_name: File name
    :return: Image after image processing
    """
    # Extract features from the RGB images
    feature_extraction(file_dir, file_name, 200)
    # Re-size the original image
    resize_image(file_name, file_name)
    # Apply circle detection to re-sized image
    plasma_center, img = circle_detection(file_name, dp=2, min_dist=10,
                                          param1=15, param2=135,
                                          min_radius=100, max_radius=150)

    if plasma_center:
        ideal_center = get_image_centre_point(img)
        draw_line_between_two_points(img, plasma_center, ideal_center)
        # Check if the run is a pass or fail
        result = check_pass_fail_(plasma_center, ideal_center)

        if result:
            # Set text to PASS and colour to green
            text = "PASS"
            colour = (0, 255, 0)
        else:
            # Set text to FAIL and colour to red
            text = "FAIL"
            colour = (0, 0, 255)

        # Add ideal limits to image
        img = add_limits_to_image(img, colour)
    # If the centre point of a circle is not detected
    else:
        # Set text to FAIL and colour to red
        text = "FAIL"
        colour = (0, 0, 255)
        cv2.putText(img=img, text="Unable to detect circle", org=(20, 460),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1, color=colour, thickness=2)

    # Add PASS/FAIL text to the image
    cv2.putText(img=img, text=text, org=(20, 50),
                fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1.5, color=colour, thickness=2)
    # Save file
    cv2.imwrite(file_name, img)


run_application("C://PlasmaDeviceApplication/Raw/2017-03-14 14-26-31/",
                "C://PlasmaDeviceApplication/Results/2017-03-14 14-26-31/Output.jpg")
