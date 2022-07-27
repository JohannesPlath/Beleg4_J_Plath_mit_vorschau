from typing import List

from pydantic import Field, BaseModel


class ImageList(BaseModel):
    images: List[str] = Field(
        example=[
            "  Sketchpad.tiff ",
            "  220px-Cupboard.tiff ",
            "  DSC_0022.svs ",
            "  DSC_0008.svs"],
        description="example List of available Images"
    )

class ResponseMessageTrue(BaseModel):
    message: str = Field(
        example=[
            "required kind of data: *.TIFF, *.tiff, *.svs, *.SVS, *.tif, *.TIF",
            "if passed, response:",
           "file 'CMU-3_test_Kopie.tiff' uploaded at './image_bucked//CMU-3_test_Kopie.tiff'"],
        description="image excepted",
    )

class ResponseMessage(BaseModel):
    message: str = Field(
        example="Operation denied... & reason",
        description="Sth. went wrong",
    )



class ResponseMessageNoLabel(BaseModel):
    message: str = Field(
        example="Operation denied. No Label availible",
        description="Sth. went wrong",
    )


class Unprocessable_entity(BaseModel):
    message: str = Field(
        example="operation denied..., wrong media type ",
        description="could be wrong parameter, ...",
    )


class Response_html(BaseModel):
    HTMLResponse: str = Field(
        example='"<!DOCTYPE html> ' +
                '<html lang="de">'  +
                '<head>"',
        description="complete interactive HTML-Page",
    )


class Response_meta(BaseModel):
    details: List = Field(
        example=[
            {'aperio.AppMag': '40',
             'aperio.DSR ID': 'homer',
             'aperio.Date': '07/16/09',
             'aperio.Filename': '6797',
             'aperio.Filtered': '3',
             'aperio.Focus Offset': '-0.001000',
             'aperio.ICC Profile': 'ScanScope v1',
             'aperio.ImageID': '6797',
             'aperio.Left': '39.010742',
             'aperio.LineAreaXOffset': '0.000000',
             'aperio.LineAreaYOffset': '0.000000',
             'aperio.LineCameraSkew': '-0.003035',
             'aperio.MPP': '0.2498',
             'aperio.OriginalWidth': '16000',
             'aperio.Originalheight': '17597',
             'aperio.ScanScope ID': 'SS1283',
             'aperio.StripeWidth': '1000',
             'aperio.Time': '18:15:06',
             'aperio.Title': 'univ missouri 07.15.09',
             'aperio.Top': '14.299895',
             'aperio.User': '93d70f65-3b32-4072-ba6a-bd6785a781be',
             'openslide.comment': 'Aperio Image Library v10.0.50\r\n'
                                  '16000x17597 [0,100 15374x17497] (256x256) J2K/YUV16 '
                                  'Q=70|AppMag = 40|StripeWidth = 1000|ScanScope ID = '
                                  'SS1283|Filename = 6797|Title = univ missouri '
                                  '07.15.09|Date = 07/16/09|Time = 18:15:06|User = '
                                  '93d70f65-3b32-4072-ba6a-bd6785a781be|MPP = 0.2498|Left '
                                  '= 39.010742|Top = 14.299895|LineCameraSkew = '
                                  '-0.003035|LineAreaXOffset = 0.000000|LineAreaYOffset = '
                                  '0.000000|Focus Offset = -0.001000|DSR ID = '
                                  'homer|ImageID = 6797|OriginalWidth = '
                                  '16000|Originalheight = 17597|Filtered = 3|ICC Profile = '
                                  'ScanScope v1',
             'openslide.level-count': '3',
             'openslide.level[0].downsample': '1',
             'openslide.level[0].height': '17497',
             'openslide.level[0].tile-height': '256',
             'openslide.level[0].tile-width': '256',
             'openslide.level[0].width': '15374',
             'openslide.level[1].downsample': '4.0003745252176746',
             'openslide.level[1].height': '4374',
             'openslide.level[1].tile-height': '256',
             'openslide.level[1].tile-width': '256',
             'openslide.level[1].width': '3843',
             'openslide.level[2].downsample': '8.0017903103069656',
             'openslide.level[2].height': '2187',
             'openslide.level[2].tile-height': '256',
             'openslide.level[2].tile-width': '256',
             'openslide.level[2].width': '1921',
             'openslide.mpp-x': '0.24979999999999999',
             'openslide.mpp-y': '0.24979999999999999',
             'openslide.objective-power': '40',
             'openslide.quickhash-1': '3380de13dab8823ca49131e7ed031bd8c0dbacda93909facdbd45d641a1453ac',
             'openslide.vendor': 'aperio',
             'tiff.ImageDescription': 'Aperio Image Library v10.0.50\r\n'
                                      '16000x17597 [0,100 15374x17497] (256x256) J2K/YUV16 '
                                      'Q=70|AppMag = 40|StripeWidth = 1000|ScanScope ID = '
                                      'SS1283|Filename = 6797|Title = univ missouri '
                                      '07.15.09|Date = 07/16/09|Time = 18:15:06|User = '
                                      '93d70f65-3b32-4072-ba6a-bd6785a781be|MPP = '
                                      '0.2498|Left = 39.010742|Top = '
                                      '14.299895|LineCameraSkew = '
                                      '-0.003035|LineAreaXOffset = '
                                      '0.000000|LineAreaYOffset = 0.000000|Focus Offset = '
                                      '-0.001000|DSR ID = homer|ImageID = '
                                      '6797|OriginalWidth = 16000|Originalheight = '
                                      '17597|Filtered = 3|ICC Profile = ScanScope v1',
             'tiff.ResolutionUnit': 'inch'}
        ],
        description="methadata of anspecific image"
)