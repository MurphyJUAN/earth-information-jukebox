# Earth Information Jukebox

**NASA Space Apps Challenge 2026 — "The Earth Information Jukebox"**

A browser-based jukebox that **listens to NASA Earth Information Center (EIC) visualizations in real time**.
Pick a visualization, and a scan line sweeps the animated map from west to east while the sound is generated
live from the pixels on screen. Nothing is pre-recorded.

▶ Run it: open `index.html` through any static web server (e.g. `python3 -m http.server`) and press **Space**.

## Core idea: read the colorbar backwards

The EIC visualizations are rendered images, not raw data. But every one of them ships with a **colorbar**, and that
colorbar is the key that turns color back into science. For every pixel we look up its color in the
visualization's own colorbar, recover the **physical value** (for example 8 °C) and sonify *that value*, not the color.

This matters because a rainbow colorbar is perceptually uneven. Mapping RGB straight to sound would inherit
those distortions, while mapping the recovered value keeps the sound faithful to the data.

## Visualizations

| | Sea Surface Temperature & Currents ([SVS 3912](https://svs.gsfc.nasa.gov/3912/)) | Night Lights 2012–2023, EIC version ([SVS 5313](https://svs.gsfc.nasa.gov/5313/)) |
|---|---|---|
| Colorbar type | continuous, 0–32 °C rainbow | diverging: orange = lights out · white = no change · purple = new lights |
| Color → value | pixel **hue** matched to the extracted colorbar (`tools/extract_lut.py`). Hue is used instead of RGB because the flow lines are shaded darker and lighter, but they keep their hue | hue/saturation classification into *city light*, *new light*, *lights out* |
| Pitch | **temperature** (A2 → A5) | new light = upper voice, lights out = lower voice, **a perfect fifth apart** |
| Left / right | longitude | longitude |
| Loudness | share of ocean in the column, so **continents are heard as silence** | share of purple vs orange pixels |
| Texture | low drone follows the **global mean** temperature through the year | yearly maps: each lit city under the scan line rings a soft bell, so more cities give denser twinkling |

The jukebox switches modes on its own: it detects whether the night-lights animation is showing the yearly
maps or the change map.

## Why these mappings (design notes)

- **Value → pitch.** Pitch is the most precise and most widely used dimension in sonification, and "higher = more" is
  intuitive without training. We kept **space** too: stereo pan carries longitude, so listeners hear *where* as well as *how much*.
- **Root + perfect fifth.** Every tone is a dyad. The perfect fifth (3:2) is the most consonant interval, so the sound
  stays pleasant whatever the data does. This answers the challenge's warning that direct pixel-to-sound becomes noise.
  For the diverging night-lights colorbar, the fifth also carries meaning: its two notes are the two ends of the colorbar,
  so loss and growth at the same place literally form one chord.
- **Musical vs raw.** By default pitches snap to a minor pentatonic scale, which contains the fifth and has no
  clashing intervals. Press **M** for raw, continuous pitch when exact values matter more than music.
- **Audio legend first.** Sighted people read the colorbar before the map. Pressing **L** plays the colorbar as sound
  from low to high, so blind and low-vision users can learn the scale before they listen.

## Accessibility

- Fully keyboard-operable: `Space` play/pause · arrow keys move a **listening probe** (`Shift` = faster) · `Esc` release ·
  `L` audio legend · `D` spoken description of the current frame · `M` musical/raw · `1`/`2` switch visualization.
- The probe speaks its location and value (e.g. "4°S, 4°W: 29.5 °C") through an ARIA live region, so it works with
  screen readers, and through built-in speech synthesis when the *Voice* option is on.
- **Describe** (`D`) summarizes the frame in words: approximate date, global mean, mean temperature per latitude band,
  and the share of ocean above 28 °C. For night lights it gives the percentage of new lights vs lights out.
- Each visualization comes with a text description of the data and of the sound mapping.

## How it works

```
EIC video ─▶ <video> ─▶ canvas downsample (180×90 / 480×135) ─▶ colorbar inversion ─▶ per-column stats
                                                                             │
                     Web Audio: dyad oscillators · stereo panner · lowpass · convolution reverb ◀─┘
```

- `index.html`: the whole app (vanilla JS, Web Audio API, no build step).
- `tools/extract_lut.py`: finds the colorbar strip in `sst_ecco2_cbar.png` and samples it into a
  64-entry hue → value lookup table (`media/web/sst_lut.json`).
- `media/web/*.mp4`: the SVS movies, transcoded to small H.264 files with ffmpeg so that browsers can play them.

## Limitations and next steps

- Values are recovered from rendered, compressed video. They are approximate, especially at coastlines and where flow lines are thin.
- The SST date is mapped linearly over the animation's documented time range (2007-03-25 → 2008-03-03), so it is approximate.
- The night-lights EIC wall version shows the globe twice side by side, so the stereo sweep crosses the world twice.
- Next: more EIC visualizations (aerosols as one instrument per aerosol type, lightning as percussion), and
  automatic colorbar detection for any SVS page.

## Credits

Visualizations and data: NASA Goddard Scientific Visualization Studio — SVS 3912 (ECCO2 model, MIT/JPL) and
SVS 5313 (VIIRS night lights). Built for NASA Space Apps Challenge 2026.
