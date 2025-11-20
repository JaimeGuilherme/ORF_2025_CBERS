# Sobre os Métodos Disponíveis nesta pasta

Este repositório disponibiliza **duas formas distintas** de realizar o
pré-processamento, fusão de bandas e pansharpening das imagens CBERS.

## 🔹 1. Método Manual no QGIS (Interface Gráfica)

Há um README dedicado explaining todo o fluxo diretamente pela interface
do QGIS, incluindo: - Conversão de 10 para 8 bits\
- Criação de VRT\
- Pansharpening usando GDAL, OTB, CBERS e outros algoritmos\
- Reprojeção das imagens

Ideal para quem deseja um processo visual, sem uso de terminal.

## 🔹 2. Método via Terminal (GDAL e Scripts)

Também está disponível um README específico com o fluxo completo usando
GDAL e scripts em terminal (Windows, CMD, Linux), incluindo: - Automação
de conversões\
- Criação de VRT com gdalbuildvrt\
- Pansharpening com gdal_pansharpen\
- Reprojeção com gdalwarp

Recomendado para automações, pipelines e grandes volumes de dados.

------------------------------------------------------------------------

## 📁 Organização

-   **README_QGIS.md** → método manual no QGIS\
-   **README_TERMINAL.md** → método via linha de comando\
-   **README.md** (este arquivo) → visão geral dos dois fluxos
