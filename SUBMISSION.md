# Space Apps 2026 submission draft — Earth Information Jukebox

> Draft text to paste into the project submission form. Check the field names and length limits against the official form.

## Project name
Earth Information Jukebox

## High-level summary
Earth Information Jukebox turns NASA Earth Information Center visualizations into live sound that a blind listener
can follow and a sighted listener can enjoy. It doesn't map raw colors to notes. Instead it **reads each visualization's own colorbar
backwards**: every pixel's color is turned back into the physical value it encodes (e.g. 27 °C, or "new lights since 2012"),
and that value is played as pitch. A scan line sweeps the map from west to east in stereo. Each tone is a root plus a
perfect fifth, so the sound stays musical. Continents fall silent, warm tropics sing high, and for night lights
growth and loss answer each other as the two notes of one fifth. Everything runs in real time in the browser, is fully keyboard
operable, starts with an **audio legend** (the colorbar played as sound), and can describe any frame or any probed
location aloud.

## Demo (must be ≤ 30 s video or ≤ 7 slides, English, hosted at a public link)
`demo/jukebox_demo_30s.mp4`: a 30-second cut of a screen recording of the app's real Web Audio output, with English captions.
Longer walkthrough: `demo/jukebox_demo_full.mp4`.

## Project details
**What it does.** Pick a visualization: (1) Global Sea Surface Currents & Temperature, SVS 3912, or (2) Change in Night
Lights 2012–2023, EIC version, SVS 5313. The jukebox plays the animation and sonifies it live:
- *Sea surface temperature*: pitch = temperature recovered from the colorbar · pan = longitude · loudness = share of ocean in
  the column, so land is silence · a drone follows the global mean temperature through the year.
- *Night lights*: in the yearly maps, every lit city under the scan line rings a bell, so more cities give denser twinkling.
  In the change map, an upper bright voice (new lights) and a lower dark voice (lights out) sound a perfect fifth apart,
  at loudness proportional to the share of purple vs orange pixels. The app detects the phase of the animation by itself.

**How it works.** Plain HTML + JavaScript + the Web Audio API, with no build step. Sea temperature: north → south scan, one synthesized cello tone (32 harmonics, body resonances, vibrato) on dominant-seventh chord tones over an octave colorbar reference. Video frames are downsampled onto a canvas.
Pixels are matched by **hue** against a lookup table extracted from the SVS colorbar image (Python + Pillow). Hue is
used instead of RGB because it is robust to the shading of the flow lines. Per-column statistics then drive dyad oscillators,
stereo panners, filters and a convolution reverb. ffmpeg transcodes the SVS movies into small, browser-friendly files.

**Accessibility.** Keyboard-only operation; a listening probe moved with the arrow keys that speaks location and value
(ARIA live region and speech synthesis); a spoken "describe this frame" summary (date, global mean, latitude bands,
share of ocean above 28 °C, share of new vs lost lights); an audio legend before playback; and a toggle between musical
(pentatonic) and raw continuous pitch.

**Why these choices.** Pitch is the most precise and widely used sonification dimension. Stereo keeps the "where".
The perfect fifth keeps the sound consonant, which answers the challenge's warning that pixel-to-sound becomes noise. For a
diverging colorbar, the two ends of the colorbar *are* the two notes of the fifth. Inverting the colorbar keeps the
sound faithful to the data rather than to the rainbow.

**Impact.** EIC's visual stories become available to blind and low-vision visitors. Sighted visitors get a second
channel that reveals patterns, such as the warm tropical band or how far new lights outnumber lost ones, as rhythm and harmony.

## NASA data used
- Global Sea Surface Currents and Temperature — NASA SVS 3912 — https://svs.gsfc.nasa.gov/3912/
- Change in Night Lights between 2012 and 2023, EIC Version — NASA SVS 5313 — https://svs.gsfc.nasa.gov/5313/
- EIC content gallery — https://svs.gsfc.nasa.gov/gallery/earth-information-center/
- Conceptual reference: Data Sonification: Caldwell 73 — https://svs.gsfc.nasa.gov/13786/

## Use of SI (Super Intelligence) tools
(Required by the Space Apps FAQ — edit to match your team's actual use. Example:) An SI coding assistant (Claude Code) was used to help write
the web app, the colorbar extraction script and the documentation, under the team's direction. All sonification design
decisions were reviewed and tested by the team. No SI-generated images, audio or video are used: all sound is
synthesized live from NASA visualization pixels.

## Tools
HTML/CSS/JavaScript, Web Audio API, Python (Pillow, NumPy), ffmpeg, Playwright (demo recording).
