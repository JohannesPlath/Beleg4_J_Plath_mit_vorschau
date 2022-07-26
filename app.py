import os
from pathlib import Path
from io import BytesIO
from pprint import pprint

import PIL
from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi.responses import FileResponse, JSONResponse, StreamingResponse

import images_service
from resp_models import ResponseMessage, ImageList, Unprocessable_entity, Response_html, Response_meta, \
    ResponseMessageNoLabel, ResponseMessageTrue

app = FastAPI()

WSI_DIR = "image_bucked"
WSI_DIR_PATH = Path(WSI_DIR)
WSI_DIR_PATH.mkdir(exist_ok=True)
THUMBNAIL_WIDTH = 500
THUMBNAIL_HEIGHT = 500
THUMBNAIL_DETAIL_MAX = ((THUMBNAIL_HEIGHT * 3) / 4) -1
fallback_x_location = 100
fallback_y_location = 100
fallback_thumb_height = 200
fallback_thumb_width = 200
fallback_height_factor = 100
fallback_width_factor = 100

should_print = True

app.mount("/js", StaticFiles(directory="frontend/js"), name="js")
templates = Jinja2Templates(directory="frontend/htmls")


def check_meta_data(fname, x_location, y_location, widthfactor, heightfactor, zoomlevel):
    meta_data = images_service.wsi_meta(fname)
    global fallback_x_location
    global fallback_y_location
    global fallback_height_factor
    global fallback_width_factor
    if not isinstance(x_location, int):
        fallback_x_location = round(int(meta_data.get('openslide.level[0].width')) / 2)
    else:
        fallback_x_location = x_location
    if not isinstance(y_location, int):
       fallback_y_location = int(meta_data.get('openslide.level[0].width')) / 2,
    else:
        fallback_y_location = y_location
    if not isinstance(widthfactor, int):
            fallback_width_factor = 200
    else:
        fallback_width_factor = widthfactor
    if not isinstance(heightfactor, int):
         fallback_height_factor = 200
    else:
        fallback_height_factor = heightfactor


def check_x(x, thumbnail):
    if (x > thumbnail.width):
        print("humbnail.width + x ", thumbnail.width, " ", x )
        print("x ", x )
        x = thumbnail.width - 5
    return x

    #print("@ Check x,y ", x, " ", y)


def check_y(y, thumbnail):
    if (y > thumbnail.height):
        print("thumbnail.height ", thumbnail.height)
        print("Y ", y)
        y = thumbnail.height - 5
    return y


def check_x_y(x, y, thumbnail):
    if (x > thumbnail.width):
        x = thumbnail.width
    if (y > thumbnail.height):
        y = thumbnail.height
    return x, y

def stream_response(image):
    in_memory_file = BytesIO()
    image.save(in_memory_file, format="png", optimized=True, quality=95)
    in_memory_file.seek(0)
    return StreamingResponse(in_memory_file, media_type="image/png", status_code=200)


@app.get(path="/",
         summary="Response an overview HTML page",
         response_class=HTMLResponse,
         responses={
             200: {
                 "content": {
                     "html-page": {"schema": {"type": "html", "format": "complete HTML page"}}
                 },
                 "descripption": "complete and interactive html-page",
             },
             404: {"model": ResponseMessage},
         })
async def _(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get(path="/viewer",
         summary="Response a HTML Page. It should be possible to interact with saved slides",
         response_model=Response_html,
         response_class=HTMLResponse,
         responses={
             200: {
                 "content": {
                     "html-page": {"schema": {"type": "html", "format": "complete HTML page"}}
                 },
                 "descripption": "complete and interactive html-page",
             },
             404: {"model": ResponseMessage},
         })
async def _(request: Request):
    return templates.TemplateResponse("viewer.html", {"request": request})


@app.get(
    path="/api/images",
    summary="list of availible images",
    response_model=ImageList,
    responses={
        200: {
            "model": ImageList,
            "description": "JSON model with list of available images",
        },
        404: {"model": ResponseMessage},
    },
)
async def get_all():
    image_list = images_service.get_list_of_availible_images()
    response_content = ImageList(images=image_list)
    return JSONResponse(content=response_content.dict(), status_code=200)

@app.get(
    path="/api/thumbnail/{fname}",
    summary="Return the thumbnail of an image",
    response_class=FileResponse,
    responses={
        200: {
            "content": {
                "images/png": {"schema": {"type": "media/image", "format": ".tiff"}}
            },
            "description": "The Image was found and responses.",
        },
        404: {"model": ResponseMessage},
        422: {"model": Unprocessable_entity}
    },
)
async def get_thumnail(
        fname: str,
):
    #print("@ get_thumbnail + fname", fname)
    thumbnail = images_service.wsi_thumbnail(fname, THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT)
    return stream_response(thumbnail)

@app.get(
    path="/api/label/{fname}",
    summary="Return the label of an image",
    response_class=FileResponse,
    responses={
        200: {
            "content": {
                "images/png": {"schema": {"type": "media/image", "format": ".tiff"}}
            },
            "description": "The Image was found and responses.",
        },
        404: {"model": ResponseMessage},
        420: {"model": ResponseMessageNoLabel},
    },
)
async def get_label(
        fname: str,
):
    label = images_service.wsi_label(fname)
    if (label == None):
        return FileResponse(path=r"./images/no-photo-available-icon-10.png", status_code=420)
    return stream_response(label)

@app.get(
    path="/api/meta/{fname}",
    summary="returns the meta-data of an image",
    response_model=ImageList,
        responses={
            200: {
                "model": Response_meta,
                "description": "JSON model with list of available images",
            },
            404: {"model": ResponseMessage},
        },
)
async def get_meta_data(
        fname: str,
):
    meta_data = images_service.wsi_meta(fname)
    if should_print:
        print(" -------> @ getMeta")
        pprint( dict(meta_data))
    #return meta_data
    response_content = {"wsi_meta": [dict(meta_data)]}
    return JSONResponse(content=response_content, status_code=200)


# @app.get(
#     path="/api/images/{fname}",
#     summary="Return a image",
#     response_class=FileResponse,
#     responses={
#         200: {
#             "content": {
#                 "images/png": {"schema": {"type": "media/image", "format": ".tiff"}}
#             },
#             "description": "The Image was found and responses.",
#         },
#         404: {"model": ResponseMessage},
#         422: {"model": Unprocessable_entity}
#     },
# )
# async def read_item(fname: str):
#     file_resp = images.images_service.get_specificPicture(fname)
#     if (file_resp):
#         return file_resp
#     else:
#         response_message = {"message": " image '{}' does not exist on the server".format(fname)},
#         return JSONResponse(response_message, status_code=404)
#
#
@app.post(
    path="/api/images",
    summary="uploading an image",
    status_code=201,
    response_model=ResponseMessageTrue,
    responses={
        201: {"model": ResponseMessageTrue},
        409: {"model": ResponseMessage}
    },
)
async def post_specific(image: UploadFile):
    given_content = await image.read()
    if os.path.exists(fr"image_bucked/{image.filename}"):
        # response_content = ResponseMessage(message=f"given image {image.filename} already exist on DB"),
        # print(response_content)
        # return JSONResponse(content=response_content.dict(), status_code=409)
        response_content = f"Operation denied... given image {image.filename} already exist on DB",
        return JSONResponse(content=response_content, status_code=409)
    else:
        excess, tmp = images_service.addPic(image, given_content)

        if excess:
            return JSONResponse(content=tmp, status_code=201)
        else:  # 415 Unsupported Media Type (en-US)
            return JSONResponse(content=tmp, status_code=415)

@app.get(
    path="/api/images/{actualWsi}/placeholder/{x_location}/{y_location}/{width}/{height}/{zoomlevel}",
    summary="responses a specific image with given detail",
    status_code=200,
    response_class=FileResponse,
    responses={
            200: {
                "content": {
                    "images/png": {"schema": {"type": "string", "format": "binary"}}
                },
                "description": "The Image was found and responses.",
            },
            404: {"model": ResponseMessage},
            422: {"model": Unprocessable_entity}
        },
)
async def get_detailed_image(
        actualWsi: str,
        x_location: int,
        y_location: int,
        width: int,
        height: int,
        zoomlevel:int,
):
    if should_print:
        print("x_location ", x_location)
        print("y_location ", y_location)
        print("zoomlevel ", zoomlevel)
        metadata = images_service.wsi_meta(actualWsi)
        print("metadata.get('openslide.level['+ zoomlevel +'].height') ", metadata.get(f'openslide.level[{zoomlevel}].height'))
        print("metadata.get('openslide.level['+ zoomlevel +'].width') ", metadata.get(f'openslide.level[{zoomlevel}].width'))
        print("@app.get arrived")

    region = images_service.wsi_region(actualWsi, zoomlevel, x_location, y_location, width, height)
    return stream_response(region)




@app.get(path="/api/thumb_detail/{fname}/{x_location_factor}/{y_location_factor}/{widthfactor}/{heightfactor}/{zoomlevel}",
    summary="Return the thumbnail of an image",
    response_class=FileResponse,
    responses={
        200: {
            "content": {
                "images/png": {"schema": {"type": "media/image", "format": ".tiff"}}
            },
            "description": "The Image was found and responses.",
        },
        404: {"model": ResponseMessage},
        422: {"model": Unprocessable_entity}
    },
)
async def get_thumbnail_detail(
        fname: str,
        x_location_factor: float,
        y_location_factor: float,
        widthfactor: float,
        heightfactor: float,
        zoomlevel:int,
):
    print("@ get_thumb_detail + fname", fname, x_location_factor, y_location_factor, widthfactor, heightfactor)
    thumbnail = images_service.wsi_thumbnail(fname, THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT)
    x_location = round(x_location_factor * thumbnail.width)
    y_location = round((y_location_factor * thumbnail.height))
    shown_marked_width = round((thumbnail.width * widthfactor))
    shown_marked_height = round(thumbnail.height * heightfactor)
    check_meta_data(fname, x_location, y_location, shown_marked_width, shown_marked_height, zoomlevel)
    detailed = thumbnail.load()
    max_x_value = x_location + shown_marked_width
    if should_print:
        print("x_location_factor ", x_location_factor)
        print("y_location_factor ", y_location_factor)
        print("widthfactor, ", widthfactor)
        print("heightfactor, ", heightfactor)
        print("shown_marked_height ", shown_marked_width)
        print("shown_marked_height ", shown_marked_height)
        print("thumbnail.width ", thumbnail.width)
        print("x_location ", x_location)
        print("thumbnail.heigth ", thumbnail.height)
        print("y_location ", y_location)

    if max_x_value > thumbnail.width:
        print("allert max_x_value " , max_x_value)
        max_x_value = thumbnail.width - 5
    for x in range(x_location , max_x_value):            # oberer Balken
        for y in range(y_location - 2, y_location + 2 ):
            detailed[x, y] = (250, 0, 0)
    for x in range(x_location, max_x_value):             # unterer Balken
        for y in range(y_location + shown_marked_height - 5, y_location + shown_marked_height ):
            detailed[x, y] = (250, 0, 0)
    for x in range(x_location, x_location + 5):                 # linker Balken
        for y in range(y_location , y_location + shown_marked_height ):
            detailed[x, y] = (250, 0, 0)
    for x in range(x_location + shown_marked_width - 5, max_x_value ):  # rechter Balken
        for y in range(y_location , y_location + shown_marked_height ):
            detailed[x, y] = (250, 0, 0)
    return stream_response(thumbnail)


# if __name__ != '__app__':
    # result = images_service.wsi_region("CMU-1.tiff", 0, 20000, 22000, 1200, 1200)
    # thumbnail = images_service.wsi_thumbnail("CMU-1.tiff", THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT)
    # meta = images_service.wsi_meta("JP2K-33003-1.tiff")
    # label = images_service.wsi_label("Leica-1(1).tiff")
    #print("pprint meta openslide.level[0].height ", meta.get("level[0].height"))
    #get_thumbnail_detail("CMU-1-Small-Region.tiff", 1, 1, 100, 100, 0)
    #print("pprint meta levelCount ", meta.get("levelcount"))

