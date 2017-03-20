# Engineer: Thomas Reaney
# College: National University of Ireland Galway
# Date: 26/01/2017
import os
import logging
import dropbox
from dropbox.files import FileMetadata

logging.basicConfig(filename="DropboxUtility.log", level=logging.INFO)


# Method: Used to get the Dropbox token for accessing remote directory
def get_dropbox_token():
    """
    :return: Dropbox token
    """
    with open("token.txt") as f:
        token = f.read()

    return str(token)


# Method: Used to get file to be uploaded to Dropbox
def get_files_from_local_dir(file_dir):
    """
    :param file_dir: Local file directory
    :return: List of file names from local file directory
    """
    # Add .jpg files and .gif files to a list
    if os.path.exists(file_dir) and os.path.isdir(file_dir):
        files_to_upload = []
        for root, dirs, files in os.walk(file_dir):
            if root == file_dir:
                for filename in files:
                    if filename.endswith(".jpg") or filename.endswith(".gif"):
                        files_to_upload.append(filename)
        return files_to_upload
    # Return empty list if the file directory does not exist
    else:
        logging.error(file_dir, "does not exist")
        return []


# Method: Used to get files from Dropbox directory to download
def get_files_from_dbox_dir(dbox_dir):
    """
    :param dbox_dir: Dropbox directory
    :return: List of file names from Dropbox directory
    """
    token = get_dropbox_token()
    dbox = dropbox.Dropbox(token)

    path = os.path.join(dbox_dir)
    if "//" in path:
        path = path.replace("//", "/")
    try:
        response = dbox.files_list_folder(path)
    except dropbox.exceptions.ApiError as err:
        logging.error("Download Error: Unable to get files for download. " + str(err))
        return []
    else:
        # Collect file names of files to be downloaded
        down_files = []
        for entry in response.entries:
            down_files.append(entry.name)
        return down_files


# Method: Used to get dat from file as bytes
def get_file_data(filename):
    """
    :param filename: File Name
    :return: File Data
    """
    with open(filename, "rb") as f:
        file_data = f.read()

    return file_data


# Method: Used to upload files from a local directory to Dropbox
def upload_files(local_dir, dbox_dir):
    """
    :param local_dir: Local Directory
    :param dbox_dir: Dropbox Directory
    """
    logging.info("Upload: Starting....")
    # Get token and set up dropbox connection
    token = get_dropbox_token()
    dbox = dropbox.Dropbox(token)

    # Get files from local directory to upload
    up_files = get_files_from_local_dir(local_dir)

    for up_file in up_files:
        path = os.path.join(dbox_dir, up_file)
        if "//" in path:
            path = path.replace("//", "/")
        up_file_data = get_file_data(up_file)

        try:
            mode = dropbox.files.WriteMode.add
            dbox.files_upload(up_file_data, path=path, mode=mode, mute=True)
            logging.info("Upload: " + up_file + " uploaded to " + path)
        except dropbox.exceptions.ApiError as err:
            logging.error("Upload Error: (File: " + up_file + ") " + str(err))
    logging.info("Upload: Finishing....")


# Method: Used to download files from Dropbox to local directory
def download_files(local_dir, dbox_dir):
    """
    :param local_dir: Local directory
    :param dbox_dir: Dropbox directory
    """
    logging.info("Download: Starting....")
    # Get token and set up dropbox connection
    token = get_dropbox_token()
    dbox = dropbox.Dropbox(token)

    # Get files to be downloaded
    down_files = get_files_from_dbox_dir(dbox_dir)

    for down_file in down_files:
        dbox_path = os.path.join(dbox_dir, down_file)
        if "//" in dbox_path:
            dbox_path = dbox_path.replace("//", "/")

        try:
            metadata, response = dbox.files_download(dbox_path)
            logging.info("Download: " + down_file + " downloaded to " + dbox_path)
            with open(os.path.join(local_dir, down_file), "wb") as f:
                f.write(response.content)
        except dropbox.exceptions.HttpError as err:
            logging.error("Download Error: (File: " + down_file + ") " + str(err))
    logging.info("Download: Finishing....")


# Method: Used to delete files from Dropbox directory
def delete_files_from_dropbox_dir(dbox_dir):
    """
    :param dbox_dir: Dropbox directory
    """
    logging.info("Delete: Starting....")
    # Get token and set up dropbox connection
    token = get_dropbox_token()
    dbox = dropbox.Dropbox(token)

    del_files = get_files_from_dbox_dir(dbox_dir)

    for del_file in del_files:
        del_path = os.path.join(dbox_dir, del_file)
        if "//" in del_path:
            del_path = del_path.replace("//", "/")

        try:
            dbox.files_delete(del_path)
        except dropbox.exceptions.ApiError as err:
            logging.error("Delete Error : " + str(err))
    logging.info("Delete: Finishing....")


# Method: Used to delete files from local directory
def delete_files_from_local_dir(local_dir):
    """
    :param local_dir: Local directory
    """
    logging.info("Delete: Starting....")

    for del_file in os.listdir(local_dir):
        del_path = os.path.join(local_dir, del_file)
        try:
            os.remove(del_path)
        except OSError as err:
            logging.error("Delete Error: (File: " + del_file + ") " + str(err))
    logging.info("Delete: Finishing....")


def test():
    # upload_files("C:/FYP/", "/Live/")
    # download_files("C:/FYP/Download/", "/Live/")
    # delete_files_from_dropbox_dir("/Live/")
    delete_files_from_local_dir("C:/FYP/Download/")


test()
