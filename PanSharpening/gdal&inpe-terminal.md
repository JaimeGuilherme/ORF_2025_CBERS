---
sidebar_position: 3
description: ''
title: 'Pansharpening'
---

## Pré-requisitos (GDAL)


Para os processo abaixo é necessário ter o gdal instalado na máquina, para isso:

### Windows 
1. Acesse o site [GISInternals](https://www.gisinternals.com/index.html).
:::danger Site Bloqueado
Até o momento em que essa documentação foi escrita, o site GISInternals está bloqueado no Brasil, pode ser acessado usando VPN privadas.
:::

2. Baixe e instale o gdal-3.10.0-1930-core.msi (ou versão mais recente)

3. Instale o gdal-3.10.0-1930-core.msi

4. Adicione o caminho do gdal na variável de ambiente PATH

    1. Copie o caminho onde foi instalado o gdal (provavelmente C:\Program Files (x86)\GDAL ou C:\Program Files\GDAL)

    2. Vá nas variáveis de ambiente e adicione o caminho do gdal

5. Instalar as wheels do GDAL para Python

    1. Acesse o site [https://github.com/cgohlke/geospatial-wheels/releases](https://github.com/cgohlke/geospatial-wheels/releases)

    2. Baixe a wheel compatível com a versão do GDAL e do Python instalados

    3. Instale a wheel via pip install, como:

        ```bash
        pip install .\GDAL-3.10.1-cp313-cp313-win_amd64.whl
        ```

### Linux

```bash	
sudo apt-get update
sudo apt-get install gdal-bin
sudo apt-get install libgdal-dev
```

## Convertendo de 10 Bits para 8 Bits

As imagens CBERS tem 10 Bits, para fazermos o pansharpening, vamos converter para 8 Bits, para isso vamos usar o comando

```bash
gdal_translate -scale 0 1023 0 255 -ot Byte %TIF_ENTRADA% %TIF_SAIDA%
```

Para rodar para todas as imagens:

**O comando a seguir ira rodar o comando anterior para todas as imagens .tif na pasta atual e a saída, terminada em _8bit.tif, será salva na pasta 8bit, criada durante o processo.**
### Windows (rodar no PowerShell, não funciona no Prompt de Comando)

```bash
New-Item -ItemType Directory -Path "8bit" -ErrorAction SilentlyContinue
Get-ChildItem -Filter "*.tif" | ForEach-Object {
    $output = "8bit\" + $_.BaseName + "_8bit.tif"
    gdal_translate -scale 0 1023 0 255 -ot Byte $_.FullName $output
}
```

### Linux

```bash
mkdir -p 8bit
for file in *.tif; do
    base=$(basename "$file" .tif)
    output="8bit/${base}_8bit.tif"
    gdal_translate -scale 0 1023 0 255 -ot Byte "$file" "$output"
done
```

:::caution Caso prefira manter em 10bit
Caso prefira não converter, pode renomear a pasta 8bit para 10bit e dispor as bandas como eram antes da conversão. Atente para não confundir o nome dos arquivos
:::


## Criar raster virtual com todas as bandas

Na pasta 8bit/10bit, vamos criar um raster virtual com todas as bandas, para isso vamos usar os comandos abaixo:

### Windows (rodar no PowerShell, não funciona no Prompt de Comando)

1. Definir os nomes de saída

```bash
python -c "import glob; print(glob.glob('CBERS_4A_WPM_*.tif')[0].replace('BAND0', 'FUSION').replace('.tif', ''))" > output_name_fusion.txt
$output_name_fusion = Get-Content "output_name_fusion.txt" | Select-Object -First 1
python -c "import glob; print(glob.glob('CBERS_4A_WPM_*.tif')[0].replace('BAND0', 'FUSION_PAN').replace('.tif', ''))" > output_name_pan.txt
$output_name_pan= Get-Content "output_name_pan.txt" | Select-Object -First 1
```

2. Rodar

:::danger COMANDO NO CMD
O comando a seguir (e apenas ele) deve ser rodado no CMD e não no PowerShell
:::
```bash
dir /b /s *.tif >file_list.txt
```

3. Excluir manualmente a banda 0 (correspondente ao pan) do arquivo file_list.txt

4. Rodar o comando gdal para gerar o raster virtual:

```bash
gdalbuildvrt -separate -resolution average -r nearest -input_file_list file_list.txt "$output_name_fusion.vrt"
```

### Linux

1. Definir os nomes de saída

```bash
python3 -c "import glob; print(glob.glob('CBERS_4A_WPM_*.tif')[0].replace('BAND0', 'FUSION').replace('.tif', ''))" > output_name_fusion.txt
output_name_fusion=$(head -n 1 output_name_fusion.txt)

python3 -c "import glob; print(glob.glob('CBERS_4A_WPM_*.tif')[0].replace('BAND0', 'FUSION_PAN').replace('.tif', ''))" > output_name_pan.txt
output_name_pan=$(head -n 1 output_name_pan.txt)
```

2. Rodar

```bash
find . -type f -name "*.tif" ! -name "*BAND0*" > file_list.txt
```

3. Rodar o comando gdal para gerar o raster virtual:

```bash
gdalbuildvrt -separate -resolution average -r nearest -input_file_list file_list.txt "$output_name_fusion.vrt"
```

## Pansharpening

:::caution Numpy
Para os comandos a seguir, o numpy deve estar instalado.
```bash
pip install numpy
```
:::

Para fazer o pansharpening, vamos usar:

```bash
gdal_pansharpen "$input_pan" "$output_name_fusion.vrt" "$output_name_pan.tif" -r cubic -of GTiff
```

## Reprojetar

As imagens CBERS saem em sistema de projeção próprio, para reprojetar:

```bash
gdalwarp -overwrite -t_srs EPSG:3857 -tr 2.0 2.0 -r lanczos -of GTiff "$output_name_pan.tif" "${output_name_pan}_3857.tif"
```