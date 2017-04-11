# Engineer: Thomas Reaney
# College: National University of Ireland Galway
# Date: 16/03/2017
from Tests import *
from OpenCV import *
from DropBox import *
from ImageManipulation import *
import time


# Method: Used to run the thermal image processing application
def main(input_dir, output_dir, download_dbox_dir, upload_dbox_dir):
    """
    :param input_dir: Raw files local directory
    :param output_dir: Results files local directory
    :param download_dbox_dir: DropBox directory for downloading
    :param upload_dbox_dir: DropBox directory for uploading
    :return: 
    """
    # Default min and max radii
    center_radius = 2
    min_radius = 130
    max_radius = 200
    # If the base local directory doesn't exist, make the new directory
    if not os.path.exists(input_dir):
        os.mkdir(input_dir)
    # Download files
    # start = time.time()
    # download_files(input_dir, download_dbox_dir)
    # end = time.time()
    # print("Download Time: " + str(int(end-start)) + "s")

    for file_dir in os.listdir(input_dir):
        run_dir = os.path.join(input_dir, file_dir)
        print("\n" + run_dir)

        out_dir_path = os.path.join(output_dir, file_dir)
        if not os.path.exists(out_dir_path):
            os.mkdir(out_dir_path)

        # Extract features from the RGB images
        fe_out_file_path = os.path.join(out_dir_path, "1_Output_FeatureExtraction.jpg")
        thresholding(run_dir, fe_out_file_path)

        # Re-size the original image
        rs_out_file_path = os.path.join(out_dir_path, "2_Output_ResizedImage.jpg")
        resize_image(fe_out_file_path, rs_out_file_path)

        # Apply circle detection to re-sized image
        plasma_center, img = circle_detection(rs_out_file_path, dp=2, min_dist=10,
                                              param1=15, param2=135,
                                              min_radius=100, max_radius=150)
        cd_out_file_path = os.path.join(out_dir_path, "3_Output_DetectedCircles.jpg")
        cv2.imwrite(cd_out_file_path, img)

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

            # Draw detected circles
            cv2.circle(img=img, center=plasma_center, radius=min_radius, color=colour, thickness=2)
            cv2.circle(img=img, center=plasma_center, radius=max_radius, color=colour, thickness=2)
            # Draw the centre point of the circle
            cv2.circle(img=img, center=plasma_center, radius=center_radius, color=colour, thickness=2)
        # If the centre point of a circle is not detected
        else:
            # Set text to FAIL and colour to red
            text = "FAIL"
            colour = (0, 0, 255)
            cv2.putText(img=img, text="Unable to detect circle", org=(20, 460),
                        fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1, color=colour, thickness=2)

        # Add ideal limits to image
        blue = (255, 0, 0)
        img = add_limits_to_image(img, blue)

        # Add PASS/FAIL text to the image
        cv2.putText(img=img, text=text, org=(20, 50),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1.5, color=colour, thickness=2)

        # Save final step of image processing
        fi_out_file_path = os.path.join(out_dir_path, "4_FinalImage.jpg")
        cv2.imwrite(fi_out_file_path, img)
        # Save final output image
        out_file_path = os.path.join(out_dir_path, "Output.jpg")
        cv2.imwrite(out_file_path, img)
        # Create gif from images
        jp_out_file_path = os.path.join(out_dir_path, "Output.gif")
        jpg_to_gif(run_dir, jp_out_file_path)

    # Upload results to DropBox
    # start = time.time()
    # upload_files(output_dir, upload_dbox_dir)
    # end = time.time()
    # print("Upload Time: " + str(int(end - start)) + "s")


main("C://PlasmaDeviceApplication/Raw/",
     "C://PlasmaDeviceApplication/Results/",
     "/PlasmaDeviceApplication/",
     "/PlasmaDeviceApplication/Results/")
