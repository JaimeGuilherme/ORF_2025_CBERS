import os
from osgeo import gdal
import rsgislib
import rsgislib.imageutils


pan_img = '/data/CBERS_4A_WPM_20240908_225_117_L4_BAND0.tif'

ms_imgs = [
    '/data/CBERS_4A_WPM_20240908_225_117_L4_BAND1.tif',
    '/data/CBERS_4A_WPM_20240908_225_117_L4_BAND2.tif',
    '/data/CBERS_4A_WPM_20240908_225_117_L4_BAND3.tif',
    '/data/CBERS_4A_WPM_20240908_225_117_L4_BAND4.tif',
]

def resample_to_match_pan(src_img, pan_img, out_img):

    pan_ds = gdal.Open(pan_img)
    if pan_ds is None:
        raise RuntimeError(f'Não consegui abrir imagem PAN: {pan_img}')

    pan_proj = pan_ds.GetProjection()
    pan_gt = pan_ds.GetGeoTransform()
    x_size = pan_ds.RasterXSize
    y_size = pan_ds.RasterYSize

    minx = pan_gt[0]
    maxy = pan_gt[3]
    maxx = minx + pan_gt[1] * x_size
    miny = maxy + pan_gt[5] * y_size

    gdal.Warp(
        out_img,
        src_img,
        format='GTiff',
        outputBounds=(minx, miny, maxx, maxy),
        xRes=pan_gt[1],
        yRes=abs(pan_gt[5]),
        dstSRS=pan_proj,
        resampleAlg=gdal.GRA_Bilinear
    )

    pan_ds = None

ms_resampled_imgs = []
for i, ms in enumerate(ms_imgs, start=1):
    out_ms = f'/data/CBERS_4A_WPM_20240908_225_117_L4_MS{i}_2m.tif'
    resample_to_match_pan(ms, pan_img, out_ms)
    ms_resampled_imgs.append(out_ms)

stack_img = '/data/CBERS_4A_WPM_20240908_225_117_L4_StackMSPAN.kea'

imgs_to_stack = ms_resampled_imgs + [pan_img]

rsgislib.imageutils.stack_img_bands(
    imgs_to_stack,
    None,
    stack_img,
    0.0,
    0.0,
    'KEA',
    rsgislib.TYPE_16UINT
)

sharpened_img = '/data/CBERS_4A_WPM_20240908_225_117_L4_StackMSPAN_Sharp.kea'

rsgislib.imageutils.pan_sharpen_hcs(
    input_img=stack_img,
    output_img=sharpened_img,
    gdalformat='KEA',
    datatype=rsgislib.TYPE_16UINT
)

rsgislib.imageutils.pop_img_stats(
    sharpened_img,
    True,
    0,
    True
)

print('Imagem resultante:', sharpened_img)