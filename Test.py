import os
from collections import defaultdict
from datetime import datetime


def get_files_in_folder(raw_file_dir, res_file_dir):

    if os.path.exists(raw_file_dir):
        for folder in os.listdir(raw_file_dir):
            raw_path = "/".join([raw_file_dir, folder])

            if os.path.isdir(raw_path):
                res_path = "/".join([res_file_dir, folder])

                if not os.path.exists(res_path):
                    os.mkdir(res_path)

                for file in os.listdir(raw_path):
                    if file.endswith(".jpg"):
                        print(file)


get_files_in_folder("C://FYP_Application/Raw/", "C://FYP_Application/Results/")


date_format = "%Y-%m-%d %H-%M-%S"
now_string = datetime.now().strftime(date_format)
now_object = datetime.strptime(now_string, date_format)

print(now_string)
print(now_object)
