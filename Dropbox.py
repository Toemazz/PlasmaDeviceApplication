# Engineer: Thomas Reaney
# College: National University of Ireland Galway
# Date: 26/01/2017
import os
import sys
import logging
import dropbox
from dropbox.files import FileMetadata

logging.basicConfig(filename="PlasmaDevice.log", level=logging.INFO)


# Method: Used to get the DropBox token for accessing remote directory
def get_dropbox_token():
    """
    :return: DropBox token
    """
    try:
        with open("token.txt") as f:
            token = f.read()
    except FileNotFoundError:
        print("Unable to find token file")
        sys.exit(0)

    return str(token)


# Method: Used to get file to be uploaded to DropBox
def get_files_from_local_dir(file_dir):
    """
    :param file_dir: Local file directory
    :return: List of file names from local file directory
    """
    # Add files to a list
    if os.path.exists(file_dir) and os.path.isdir(file_dir):
        files_to_upload = []
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                temp_root = "/".join(root.strip("/").split('/')[1:])
                files_to_upload.append(os.path.join(temp_root, file))
        print("Files to upload got from local directory")
        return files_to_upload
    # Return empty list if the file directory does not exist
    else:
        print("No files found")
        sys.exit(0)


# Method: Used to get files from DropBox directory to download
def get_files_from_dropbox_dir(dbox_dir):
    """
    :param dbox_dir: DropBox directory
    :return: List of file names from DropBox directory
    """
    token = get_dropbox_token()
    dbox = dropbox.Dropbox(token)

    path = os.path.join(dbox_dir)
    if "//" in path:
        path = path.replace("//", "/")
    if "\\" in path:
        path = path.replace("\\", "/")

    try:
        response = dbox.files_list_folder(path, recursive=True)
    except dropbox.exceptions.ApiError:
        print("Unable to get files for download")
        sys.exit(0)
    else:
        # Collect file names of files to be downloaded
        down_files = []
        for entry in response.entries:
            down_files.append(entry.path_display)
        print("Files downloaded from DropBox")
        return down_files


# Method: Used to get data from file as bytes
def get_file_data(filename):
    """
    :param filename: File Name
    :return: File Data
    """
    try:
        with open(filename, "rb") as f:
            file_data = f.read()
    except FileExistsError:
        print("Unable to get file data")
        file_data = b""

    return file_data


# Method: Used to upload files from a local directory to DropBox
def upload_files(local_dir, dbox_dir):
    """
    :param local_dir: Local Directory
    :param dbox_dir: DropBox Directory
    """
    # Get token and set up DropBox connection
    token = get_dropbox_token()
    dbox = dropbox.Dropbox(token)

    # Get files from local directory to upload
    up_files = get_files_from_local_dir(local_dir)

    if len(up_files) == 0:
        print("No files in the directory to be uploaded to DropBox")
    else:
        for up_file in up_files:
            path = os.path.join(dbox_dir, up_file)
            if "//" in path:
                path = path.replace("//", "/")
            if "\\" in path:
                path = path.replace("\\", "/")

            up_file_data = get_file_data(up_file)

            try:
                mode = dropbox.files.WriteMode.add
                dbox.files_upload(up_file_data, path=path, mode=mode, mute=True)
                print("UPLOADED\t", up_file)
                logging.info("DropBox.py: " + up_file + " uploaded to " + path)
            except dropbox.exceptions.ApiError:
                logging.info("DropBox.py: " + up_file + " unable to be uploaded")
        print("Files uploaded to DropBox")


# Method: Used to download files from DropBox to local directory
def download_files(local_dir, dbox_dir):
    """
    :param local_dir: Local directory
    :param dbox_dir: DropBox directory
    """
    # Get token and set up dropbox connection
    token = get_dropbox_token()
    dbox = dropbox.Dropbox(token)

    # Get files to be downloaded
    down_files = get_files_from_dropbox_dir(dbox_dir)

    if not down_files:
        print("No files in DropBox directory")
    else:
        # Add files to local directory
        for down_file in down_files:
            try:
                metadata, response = dbox.files_download(down_file)
                logging.info("DropBox.py: " + down_file + " downloaded to " + local_dir)
                filename = down_file.split("/")[-1]
                down_path = os.path.join(local_dir, down_file.split("/")[-2])

                if not os.path.exists(down_path):
                    os.mkdir(down_path)

                down_path_with_file = os.path.join(down_path, filename)
                with open(down_path_with_file, "wb") as f:
                    f.write(response.content)
                print("DOWNLOADED\t", down_path_with_file)
            except dropbox.exceptions.HttpError:
                logging.error("DropBox.py: " + down_path_with_file + " unable to be downloaded")
            except dropbox.exceptions.ApiError:
                pass
        print("Files downloaded from DropBox")


# Method: Used to delete files from DropBox directory
def delete_files_from_dropbox_dir(dbox_dir):
    """
    :param dbox_dir: DropBox directory
    """
    # Get token and set up DropBox connection
    token = get_dropbox_token()
    dbox = dropbox.Dropbox(token)

    # Get files to delete from DropBox
    del_files = get_files_from_dropbox_dir(dbox_dir)

    if len(del_files) == 0:
        print("No files in DropBox directory to be deleted")
    else:
        # Delete each file from DropBox
        for del_file in del_files:
            del_path = os.path.join(dbox_dir, del_file)
            if "//" in del_path:
                del_path = del_path.replace("//", "/")

            try:
                dbox.files_delete(del_path)
            except dropbox.exceptions.ApiError:
                logging.info("DropBox.py: " + del_file + " unable to be deleted")
        print("Files deleted from DropBox directory")


# Method: Used to delete files from local directory
def delete_files_from_local_dir(local_dir):
    """
    :param local_dir: Local directory
    """
    if len(os.listdir(local_dir)) == 0:
        print("No files to be deleted from the local directory")
    else:
        # Delete files from local directory
        for del_file in os.listdir(local_dir):
            del_path = os.path.join(local_dir, del_file)
            try:
                os.remove(del_path)
            except OSError:
                logging.info("DropBox.py: " + del_file + " unable to be deleted")
        print("Files deleted from local directory")
