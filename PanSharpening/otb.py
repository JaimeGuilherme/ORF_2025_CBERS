import otbApplication as otb
import os

input_pan = "CBERS_4A_WPM_20240908_225_117_L4_BAND0.tif"

input_xs = "CBERS_4A_WPM_20240908_225_117_L4_RGBNIR.tif"

temp_xs_resampled = "temp_xs_resampled.tif"

output_filename = "CBERS_4A_PANSHARPENED.tif"

app_super = otb.Registry.CreateApplication("Superimpose")

app_super.SetParameterString("inr", input_pan)
app_super.SetParameterString("inm", input_xs)
app_super.SetParameterString("out", temp_xs_resampled)

app_super.SetParameterString("interpolator", "bco") 

app_super.ExecuteAndWriteOutput()

app_pan = otb.Registry.CreateApplication("Pansharpening")

app_pan.SetParameterString("inp", input_pan)
app_pan.SetParameterString("inxs", temp_xs_resampled)
app_pan.SetParameterString("out", output_filename)

app_pan.SetParameterOutputImagePixelType("out", otb.ImagePixelType_uint16)

app_pan.SetParameterString("method", "rcs")

app_pan.ExecuteAndWriteOutput()

print(f"Arquivo gerado: {output_filename}")