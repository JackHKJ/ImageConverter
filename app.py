# Author: K.J.
# Import
from os import path, sep
import os
from PIL import Image
from pathvalidate import sanitize_filepath

# Validate whether the given filename is usable in current os


def check(filePath):
    if os.path.exists(filePath):
        return True
    if filePath == sanitize_filepath(filePath):
        return True
    return False


# Check file exists, if so, read config, check validity and load into environment
def loadConfig():

    DEFAULT_OUTPUT_FOLDER = "$Converted"
    DEFAULT_OUTPUT_FORMAT = "png"
    VALID_FORMAT = ['png', 'jpeg', 'webp']
    # VALID_FILE_PATTERN = re.compile("\\/?%*:|\"<>")

    if path.exists("config.txt"):
        my_config = open('config.txt', 'r')
        try:
            output_folder_name = my_config.readline().strip()
            # if VALID_FILE_PATTERN.match(output_folder_name):
            if check(output_folder_name):
                print("Using output folder: {}".format(output_folder_name))
                DEFAULT_OUTPUT_FOLDER = output_folder_name
            else:
                print("Invalid folder name, using default: {}".format(
                    DEFAULT_OUTPUT_FOLDER))
            output_format = my_config.readline().strip().lower()
            if output_format in VALID_FORMAT:
                print("Using output format: {}".format(output_format))
                DEFAULT_OUTPUT_FORMAT = output_format
            else:
                print("Invalid format, using default: {}".format(
                    DEFAULT_OUTPUT_FORMAT))

        except FileNotFoundError:
            print("Cannot load config, using default settings")
    return DEFAULT_OUTPUT_FOLDER, DEFAULT_OUTPUT_FORMAT


def findAllFile(base):
    for root, _, fs in os.walk(base):
        for f in fs:
            yield root, root + os.sep + f


if __name__ == "__main__":
    DEFAULT_OUTPUT_FOLDER, DEFAULT_OUTPUT_FORMAT = loadConfig()
    # if output folder already exists, break
    if path.exists('.' + os.sep + DEFAULT_OUTPUT_FOLDER):
        print("Output folder detected, terminating!")
        exit()

    base = '.'
    for this_pwr, this_file in findAllFile(base):
        # New file path according to the settings
        converted_path = '.' + os.sep + DEFAULT_OUTPUT_FOLDER + \
            this_file[1:this_file.rfind('.')] + '.' + DEFAULT_OUTPUT_FORMAT 
        converted_pwr = '.' + os.sep + DEFAULT_OUTPUT_FOLDER + this_pwr[1:]
        print(converted_path)
        # If already exist, skip
        if path.exists(converted_path):
            continue
        # Open - Convert - Close
        try:
            print(converted_pwr)
            if not path.exists(converted_pwr):
                os.makedirs(converted_pwr)
            im = Image.open(this_file).convert("RGB")
            im.save(converted_path, DEFAULT_OUTPUT_FORMAT)
            im.close()
        except Exception as e:
            print(e)
            # Not a image file, continue
            print("skipped")
            continue
