"""Extract the SST colorbar into a hue->value lookup table (sst_ecco2_cbar.png, 0..32 degC)."""
import json, sys, colorsys
import numpy as np
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
im = np.asarray(Image.open(src).convert("RGB")).astype(float) / 255
h, w, _ = im.shape
# find the bar: rows/cols with high saturation
sat = im.max(2) - im.min(2)
rows = np.where((sat > 0.5).sum(1) > w * 0.6)[0]
cols = np.where((sat > 0.5).sum(0) > len(rows) * 0.6)[0]
y = int(np.median(rows))
x0, x1 = cols.min(), cols.max()
strip = im[rows.min():rows.max() + 1, x0:x1 + 1].mean(0)
lut = []
n = 64
for i in range(n):
    r, g, b = strip[int(i / (n - 1) * (len(strip) - 1))]
    hh, ss, vv = colorsys.rgb_to_hsv(r, g, b)
    lut.append({"t": i / (n - 1), "value": round(32 * i / (n - 1), 2),
                "hue": round(hh * 360, 1), "rgb": [int(r * 255), int(g * 255), int(b * 255)]})
json.dump({"name": "Sea Surface Temperature", "unit": "°C", "min": 0, "max": 32, "lut": lut}, open(out, "w"), indent=1)
print("bar rows", rows.min(), rows.max(), "cols", x0, x1)
print("hues:", [e["hue"] for e in lut[::8]])
