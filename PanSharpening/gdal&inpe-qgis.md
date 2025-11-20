# README -- Workflow de Pansharpening e Pré-processamento no QGIS (Sem Terminal)

Este repositório descreve um fluxo completo de pré-processamento e
pansharpening de imagens CBERS no **QGIS**, utilizando apenas
ferramentas da interface gráfica, sem uso de linha de comando.

## 1. Pré-requisitos (QGIS)

-   QGIS 3.22 ou superior
-   Ferramentas nativas de raster
-   Plugins opcionais: SCP, OTB

## 2. Conversão de 10 bits para 8 bits

Use Raster → Conversion → Translate: - Scale: 0--1023 para 0--255 -
Output type: Byte

## 3. Criar VRT com bandas multiespectrais

Raster → Miscellaneous → Build Virtual Raster: - Separate bands -
Resolution: average - Resampling: nearest neighbour

## 4. Pansharpening no QGIS

### GDAL nativo

Processing Toolbox → GDAL → Pansharpen

### Plugin CBERS (INPE)

CBERS → Pansharpening

### Orfeo Toolbox (OTB)

Processing → OTB → Optical → Pansharpening

### RSGISLib (se instalado)

Processing → RSGISLib → Image Enhancement → Pansharpening

## 5. Reprojeção

Raster → Projections → Warp (Reproject): - CRS: EPSG:3857 - Resampling:
Lanczos
