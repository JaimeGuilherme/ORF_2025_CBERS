# Remote Sensing Toolbox – PanSharpening & Image Quality Metrics

Este repositório contém ferramentas em Python para:
- PanSharpening de imagens multiespectrais usando diferentes métodos;
- Cálculo de estatísticas de qualidade entre imagens de referência e imagens processadas;
- Comparações por histograma entre duas imagens.

A estrutura do repositório está organizada em duas pastas principais:

PanSharpening/
Estatistics/

## 1. PanSharpening

A pasta PanSharpening contém scripts para realizar PanSharpening utilizando dois métodos distintos.

### otb.py
Script que usa o Orfeo Toolbox (OTB) para PanSharpening.

Métodos suportados:
- Brovey
- PCA
- Bayesian
- RCS
- HPF

Requer OTB instalado e acessível pelo PATH ou via OSGeo4W.

### rsgis.py
PanSharpening usando RSGISLib, executado via Docker.

Para usar este método, baixe a imagem oficial:

docker pull petebunting/rsinfo_rsgislib_build

O script faz processamento raster utilizando as ferramentas internas do RSGISLib.

## 2. Estatistics

A pasta Estatistics contém scripts para análise e comparação de imagens.

### histogram.py
Calcula a diferença entre histogramas de duas imagens por meio de:
- Máscara poligonal aplicada sobre a imagem;
- Cálculo de histogramas dentro e fora da região;
- Distância de Wasserstein (Earth Mover’s Distance).

### params_calc.py
Calcula métricas de avaliação clássicas de qualidade entre uma imagem de referência e uma imagem processada.

Métricas implementadas:
- SD (Standard Deviation)
- Q-Index (Wald)
- ERGAS

Recursos adicionais:
- Reprojeção automática da imagem avaliada para a grade da imagem de referência;
- Suporte a múltiplas bandas;
- Resampling bilinear;
- Barra de progresso durante o processamento.

## Dependências gerais

Python:
- numpy
- rasterio
- scipy
- pillow

Para PanSharpening:
- Orfeo Toolbox (OTB)
- Docker + imagem petebunting/rsinfo_rsgislib_build

Instalação recomendada:
pip install numpy rasterio scipy pillow

## Estrutura do repositório

PanSharpening/
    otb.py
    rsgis.py

Estatistics/
    histogram.py
    params_calc.py

README.md

## Objetivo geral

Este repositório fornece ferramentas completas para:
- Processar imagens multiespectrais e pancromáticas;
- Executar PanSharpening por diversos métodos;
- Avaliar quantitativamente a qualidade da fusão;
- Comparar histogramas e estatísticas entre imagens.
