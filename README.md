# Earth Information Jukebox

**NASA Space Apps Challenge 2026 — "The Earth Information Jukebox"**

A browser-based jukebox that **listens to NASA Earth Information Center (EIC) visualizations in real time**.
Pick a visualization, and a scan line sweeps the animated map while the sound is generated live from the pixels
on screen. Nothing is pre-recorded.

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
| Scan | **north → south**, one latitude row at a time, or **west → east inside a fixed latitude band** (tropics, 30–60°N, 30–60°S) | west → east |
| Colorbar as sound | an **octave** played by two bassoon-like woodwinds, D2 = 0 °C · D3 = 32 °C, sounding softly the whole time as a **pitch reference** | — |
| Data as sound | **one bowed cello tone**: pitch = mean temperature of the row, landing on **dominant-seventh chord tones** (D · F♯ · A · C · D), so it never forms a semitone or second against the reference. `M` = exact continuous pitch | new light = upper voice, lights out = lower voice, **a perfect fifth apart** |
| Loudness | share of ocean in the row, so land and ice latitudes fall quiet | share of purple vs orange pixels |
| Texture | a pizzicato octave double-stop marks the start of each sweep | yearly maps: each lit city under the scan line rings a soft bell, so more cities give denser twinkling |

The jukebox switches modes on its own: it detects whether the night-lights animation is showing the yearly
maps or the change map.

## Why these mappings (design notes)

- **Value → frequency.** Pitch is the most precise and most widely used dimension in sonification, and "higher = more" is
  intuitive without training.
- **The colorbar is a fixed consonant interval.** A sighted viewer always has the colorbar on screen as a reference. A listener
  gets the same thing: the colorbar's two ends are an octave, the most universal and least harsh interval, and they keep
  sounding in the background. The data tone is always heard *relative to* those two edges.
- **The data is a single tone with a real timbre.** One bowed cello line, not a chord, synthesized from 32 harmonics with
  body resonances and vibrato. The cello was chosen for the ocean because currents are continuous, slow and directional,
  which is what legato bowing sounds like.
- **No harsh intervals.** Against an octave reference, a freely gliding tone would pass through semitones and seconds.
  In musical mode the temperature snaps to the dominant-seventh chord tones inside the octave, so each sweep becomes an arpeggio
  that rises toward the warm equator and falls toward the poles. Press **M** for exact, continuous pitch.
- **Scan along the structure of the data.** Sea temperature is organised by latitude, so the SST scan runs north → south.
- **Audio legend first.** Sighted people read the colorbar before the map. Pressing **L** plays the colorbar as sound
  from low to high, so blind and low-vision users can learn the scale before they listen.

## Accessibility

- Fully keyboard-operable: `Space` play/pause · arrow keys move a **listening probe** (`Shift` = faster) · `Esc` release ·
  `L` audio legend · `D` text description of the current frame · `M` musical/exact · `1`/`2` switch visualization.
- The probe plays the value under it and writes its location and value (e.g. "4°S, 4°W: 29.5 °C") to an ARIA live region,
  so screen-reader users get the readout. The app itself never speaks over the music.
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
