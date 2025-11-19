import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling

def calcular_sd_q(img1, img2):
    if img1.shape != img2.shape:
        raise RuntimeError(f"tamanhos diferentes: {img1.shape} vs {img2.shape}")
    x = img1.ravel()
    y = img2.ravel()
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]
    diff = x - y
    sd = np.std(diff)
    mx = np.mean(x)
    my = np.mean(y)
    vx = np.var(x)
    vy = np.var(y)
    cxy = np.mean((x - mx) * (y - my))
    num = 4 * cxy * mx * my
    den = (vx + vy) * (mx**2 + my**2)
    if den == 0:
        q = 0.0
    else:
        q = num / den
    return sd, q

def calcular_ergas(img_ref, img_fus, ratio):
    if img_ref.shape != img_fus.shape:
        raise RuntimeError(f"tamanhos diferentes: {img_ref.shape} vs {img_fus.shape}")
    if img_ref.ndim == 2:
        img_ref = img_ref[np.newaxis, ...]
        img_fus = img_fus[np.newaxis, ...]
    bandas = img_ref.shape[0]
    soma = 0.0
    for b in range(bandas):
        r = img_ref[b].ravel()
        f = img_fus[b].ravel()
        mask = np.isfinite(r) & np.isfinite(f)
        r = r[mask]
        f = f[mask]
        diff = f - r
        mse = np.mean(diff**2)
        rmse = np.sqrt(mse)
        media_ref = np.mean(r)
        termo = (rmse / media_ref) ** 2
        soma += termo
    ergas = 100 * ratio * np.sqrt(soma / bandas)
    return ergas

if __name__ == "__main__":
    caminho_ref = r".\CBERS_4A_WPM_20240908_225_117_L4_GDAL_8BITS.tif"
    caminho_fus = r".\Manaus.tif"

    print("Usando TIF de referência (grade):", caminho_ref)
    print("Usando TIF de referência:", caminho_fus)

    with rasterio.open(caminho_ref) as ds_ref, rasterio.open(caminho_fus) as ds_fus:
        bandas = min(ds_ref.count, ds_fus.count)
        img_ref = ds_ref.read(indexes=list(range(1, bandas + 1))).astype(np.float32)
        img_fus_resampled = np.empty((bandas, ds_ref.height, ds_ref.width), dtype=np.float32)

        for i in range(bandas):
            src_array = ds_fus.read(i + 1).astype(np.float32)
            reproject(
                source=src_array,
                destination=img_fus_resampled[i],
                src_transform=ds_fus.transform,
                src_crs=ds_fus.crs,
                dst_transform=ds_ref.transform,
                dst_crs=ds_ref.crs,
                dst_height=ds_ref.height,
                dst_width=ds_ref.width,
                resampling=Resampling.bilinear
            )

    sd, q = calcular_sd_q(img_ref, img_fus_resampled)
    ergas = calcular_ergas(img_ref, img_fus_resampled, 4)

    print("SD:", sd)
    print("Q-index:", q)
    print("ERGAS:", ergas)
