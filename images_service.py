import os
from typing import List
from ctypes import cdll
from ctypes.util import find_library

_lib = cdll.LoadLibrary(find_library("libopenslide-0.dll"))
from pprint import pprint

import openslide
import argparse
from fastapi.responses import FileResponse

should_print = True

abspath = r"./image_bucked/"
extention_list: List[str] = [".TIFF", ".tiff", ".svs", ".SVS", ".tif", ".TIF"]


def search_4_specific_extention(local_path, extention):
    return [_ for _ in os.listdir(local_path) if _.endswith(extention)]


def get_list_of_availible_images():
    if os.path.exists(abspath) == True:
        result: List = []
        for x in extention_list:
            tmp = (
                search_4_specific_extention(abspath, x))  # "{}{}{}".format (png_list, PNG_list, jpeg_list, JPEG_list)
            result = result + tmp
        # print(result)
        return result
    else:
        return "no Images exists in specified path"


def get_specificPicture(pic_name: str):
    # print("picName: ", pic_name)
    if os.path.exists(abspath + r"/" + pic_name) == True:
        return FileResponse(path=abspath + r"/" + pic_name, status_code=200)
    else:
        return None


def valid_media_typ(file):
    isvalid = False
    for x in extention_list:
        # print("x: ", x, "Filename: ", file.filename )
        if file.filename.endswith(x):
            isvalid = True
    return isvalid


def add_pic(pic, pic_as_byte):
    file_location = fr"{abspath}/{pic.filename}"
    if valid_media_typ(pic):
        with open(file_location, "wb+") as file_object:
            file_object.write(pic_as_byte)
        return True, {"message": f"file '{pic.filename}' uploaded at '{file_location}'"}
    else:
        return False, {"message": f" Operation denied... file '{pic.filename}' has an irregular type/ending"}


def wsi_region(input_file, level, x_location, y_location, width, height):
    if should_print:
        print("@  wsi_region")
        print("path: ", "./image_bucked/" + input_file)
        print("level, x_location, y_location, width, height ", level, " ", x_location, " ", y_location, " ", width, " ",
              height)
    try:
        actual_slide = openslide.OpenSlide("./image_bucked/" + input_file)
        img = actual_slide.read_region((x_location, y_location), level, (width, height))
        # img.save("test_bucked/new_Region_" + input_file)
        return img
    except:
        return None


def wsi_thumbnail(input_file, width, height):
    if should_print:
        print("thumbnail @ wsi_thumbnail")
    try:
        actual_slide = openslide.OpenSlide("./image_bucked/" + input_file)
        img = actual_slide.get_thumbnail((width, height))
        # img.save("test_bucked/new_Thumbnail_" + input_file)
        return img
    except:
        return None


def wsi_label(input_file):
    actual_slide = openslide.OpenSlide(abspath + input_file)
    result = None
    try:
        result = actual_slide.associated_images["label"]
        # result.save("test_bucked/new_label_" + input_file)
        return result
    except:
        return result


def wsi_meta(input_file):
    if should_print:
        print("arrived @ meta")
    actual_slide = openslide.OpenSlide("./image_bucked/" + input_file)
    return actual_slide.properties

# if __name__ != '__images_service':
#     wsi_region("CMU-1.tiff", 0, 20000, 22000, 1200, 1200)
