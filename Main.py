# Engineer: Thomas Reaney
# College: National University of Ireland Galway
# Date: 16/03/2017
from Tests import *
from OpenCV import *
from DropBox import *
from ImageManipulation import *


def main(input_dir, output_dir, download_dbox_dir, upload_dbox_dir):
    # If the base local directory doesn't exist, make the new directory
    if not os.path.exists(input_dir):
        os.mkdir(input_dir)
    # Download files
    # download_files(base_local_dir, download_dbox_dir)

    for file_dir in os.listdir(input_dir):
        run_dir = os.path.join(input_dir, file_dir)
        print(run_dir, "\n")

        out_dir_path = os.path.join(output_dir, file_dir)
        if not os.path.exists(out_dir_path):
            os.mkdir(out_dir_path)

        # Extract features from the RGB images
        fe_out_file_path = os.path.join(out_dir_path, "1_Output_FeatureExtraction.jpg")
        feature_extraction(run_dir, fe_out_file_path)

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
        # Save final step of image processing
        fi_out_file_path = os.path.join(out_dir_path, "4_FinalImage.jpg")
        cv2.imwrite(fi_out_file_path, img)
        # Save final output image
        out_file_path = os.path.join(out_dir_path, "Output.jpg")
        cv2.imwrite(out_file_path, img)

    # Upload results to DropBox
    # upload_files(output_dir, upload_dbox_dir)


main("C://PlasmaDeviceApplication/Raw/",
     "C://PlasmaDeviceApplication/Results/",
     "/PlasmaDeviceApplication/",
     "/PlasmaDeviceApplication/Results/")
