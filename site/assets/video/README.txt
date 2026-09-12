Two cuts of your room tour, both encoded from "Shetty hospitality_ rooms video_A2.MOV".

  hero.mp4           1080x608   3.0 Mbps   30 s   10.0 MB   wide screens
  hero-portrait.mp4   720x1280  2.4 Mbps   30 s    8.1 MB   phones (under 820px)

Why two: the source was shot vertically. On a desktop the browser crops a tall video to a
horizontal band anyway, so hero.mp4 is that band cropped at full source resolution — every
bit of the file goes into pixels you actually see, which is what makes it look sharp.
hero-portrait.mp4 keeps the whole tall frame for phones, where the full height is visible.

The script picks one at page load. If you only want to maintain one file, keep hero.mp4;
phones will just crop it more tightly.

Replacing them:
  - H.264 in an .mp4. HEVC will not play in most browsers, which is why the original could
    not be used as-is.
  - Around 3 Mbps is the floor for this footage. Below about 2 Mbps the wood grain and
    fabric go blocky.
  - No audio track; it plays muted, so audio is wasted bytes.
  - Landscape footage of the same rooms would beat both of these on desktop.
