import os
import glob
import numpy as np
from PIL import Image, ImageDraw
from scipy.stats import wasserstein_distance
import rasterio

def f_dist(histogram1, histogram2):
    bins = np.arange(len(histogram1))
    return wasserstein_distance(bins, bins, u_weights=histogram1, v_weights=histogram2)

def prepare_mask(polygon, image, value):
    height, width = image.shape
    mask = Image.new('L', (width, height), value)
    ImageDraw.Draw(mask).polygon(polygon, outline=1, fill=abs(value - 1))
    mask = np.array(mask).astype(bool)
    return mask

def compute_histogram(mask, image):
    region = image[mask]
    hist, _ = np.histogram(region.ravel(), bins=256, range=[0, 255])
    return hist

def carregar_tif_e_ecw(pasta='.'):
    tif_files = glob.glob(os.path.join(pasta, '*.tif')) + glob.glob(os.path.join(pasta, '*.tiff'))
    ecw_files = glob.glob(os.path.join(pasta, '*.ecw'))

    if not tif_files:
        raise RuntimeError("Nenhum arquivo TIF encontrado na pasta.")
    if not ecw_files:
        raise RuntimeError("Nenhum arquivo ECW encontrado na pasta.")

    return tif_files[0], ecw_files[0]

def ler_raster_grayscale(path):
    with rasterio.open(path) as src:
        band1 = src.read(1).astype(np.float32)

        min_val = np.nanmin(band1)
        max_val = np.nanmax(band1)
        if max_val > min_val:
            band1 = (band1 - min_val) / (max_val - min_val) * 255.0
        else:
            band1[:] = 0.0

        band1 = np.clip(band1, 0, 255).astype(np.uint8)

    return band1

if __name__ == "__main__":
    caminho_tif1 = r".\CBERS_4A_WPM_20240908_225_117_L4_INPE.tif"
    caminho_tif2 = r".\Manaus.tif"

    print("Usando TIF1:", caminho_tif1)
    print("Usando TIF2:", caminho_tif2)

    image_gray1 = ler_raster_grayscale(caminho_tif1)
    image_gray2 = ler_raster_grayscale(caminho_tif2)

    points = [
        (633, 312), (630, 351), (623, 389), (611, 426), (594, 462), (573, 495),
        (548, 525), (519, 552), (488, 575), (453, 594), (417, 608), (379, 618),
        (340, 623), (301, 623), (262, 618), (224, 608), (188, 594), (153, 575),
        (122, 552), (93, 525), (68, 495), (47, 462), (30, 426), (18, 389),
        (11, 351), (9, 311), (11, 272), (18, 234), (30, 197), (47, 161),
        (68, 128), (93, 98), (122, 71), (153, 48), (188, 29), (224, 15),
        (262, 5), (301, 0), (340, 0), (379, 5), (417, 15), (453, 29),
        (488, 48), (519, 71), (548, 98), (573, 128), (594, 161), (611, 197),
        (623, 234), (630, 272)
    ]

    mask_poly1 = prepare_mask(points, image_gray1, 0)

    if image_gray1.shape == image_gray2.shape:
        mask_poly2 = mask_poly1
    else:
        h1, w1 = image_gray1.shape
        h2, w2 = image_gray2.shape
        sx = w2 / w1
        sy = h2 / h1
        points2 = [(int(round(x * sx)), int(round(y * sy))) for (x, y) in points]
        mask_poly2 = prepare_mask(points2, image_gray2, 0)

    histogram_tif = compute_histogram(mask_poly1, image_gray1)
    histogram_ecw = compute_histogram(mask_poly2, image_gray2)

    dist = f_dist(histogram_tif, histogram_ecw)
    print("Distância de Wasserstein entre TIF e ECW na região do polígono:", dist)
