# Shetty's Hospitality — website

Static site. No build tools, no dependencies. Open `site/index.html` in a browser, or run the
local server below.

## Run it locally

```bash
python3 ".claude/serve.py"
```

Then visit http://localhost:4321

## Pages

| File | What's on it |
| --- | --- |
| `site/index.html` | Home — hero, the five service verticals, why one contact matters |
| `site/stays.html` | Homestays and service apartments |
| `site/celebrations.html` | Events hosted at home |
| `site/journeys.html` | Temple journeys, rides, Hidden Mangalore |
| `site/about.html` | The problem, how you work, the four-step journey, vision |
| `site/contact.html` | Enquiry form and contact details |

## Where to add your details

**Copy and page structure** — either edit the HTML in `site/` directly, or edit `build_site.py`
at the project root and re-run `python3 build_site.py` to regenerate all six pages with the
shared header and footer intact. Pick one and stick to it: running the script overwrites the
HTML files.

**The hero video** — the home page headline sits over a full-screen looping video of your room
tour. Two encodes live in `site/assets/video/`: `hero.mp4` (a wide band, for desktop) and
`hero-portrait.mp4` (the full tall frame, for phones); the script picks one at load.
`site/assets/img/hero-poster.jpg` shows until playback starts. The folder's README explains the
encoding settings and why there are two files.

The source was shot vertically and carries your logo watermark in the top right. Landscape
footage without the watermark would suit this hero better — worth a reshoot when you are next
at the property.

**Page header photographs** — each inner page has an image beside its headline, in
`site/assets/img/pages/`: `stays.jpg`, `celebrations.jpg`, `journeys.jpg`, `about.jpg`.
Landscape 4:3, 1200px wide. The card images on the home page are 3:4 portrait instead.

`stays.jpg` is a real still pulled from your room-tour video. The other three are AI-generated
stand-ins for the photography being shot now. When those photos land, overwrite these four files
with the same names and nothing else needs to change. What each slot wants:

| File | Photograph |
| --- | --- |
| `stays.jpg` | One room with the light doing something — the afternoon sun the copy mentions |
| `celebrations.jpg` | A detail, not a wide shot: hands laying leaves, a garland going up, plates going down |
| `journeys.jpg` | The arrival at a temple, not the road — steps, lamps, someone walking up |
| `about.jpg` | Rithesh, or a caretaker with keys. It is the page that claims a real person is behind this |

**Card photographs** — the six tiles under "Five things, one phone number" each take a photo
band from `site/assets/img/cards/`: `stays.jpg`, `celebrations.jpg`, `rides.jpg`, `temples.jpg`,
`hidden.jpg`, `plan.jpg`. These are AI-generated placeholders. Replace them with real photographs
of your houses, an event you catered and a car you actually use — same filenames, roughly 3:2 or
taller, and the card crops to a 16:10 band from the middle.

**Photographs** — drop yours into `site/assets/img/` and swap the `src` in the HTML. Two
placeholders are in place now, both cropped from the brochure:

- `hero-lobby.jpg` — home page hero (portrait, roughly 5:6)
- `detail-wide.jpg` — used on the home and stays pages (landscape, roughly 4:3)

Grey caption lines like *"Photograph: living room, morning"* mark each slot. They come from the
`data-ph` attribute on the wrapping `<div class="ph">` — delete the attribute once the real
photo is in.

**Contact details** live in `build_site.py` as `PHONE_DISPLAY`, `PHONE_TEL`, `PHONE_WA` and
`EMAIL`. Change them there and rebuild, or find-and-replace across `site/*.html`.

**Colours and type** are CSS variables at the top of `site/assets/css/styles.css`. The sage
`#5C745C` is sampled from your logo; the terracotta `#B4553A` is a Mangalore roof-tile red used
sparingly as the accent.

## The enquiry form

`site/assets/js/main.js` currently opens WhatsApp with the enquiry pre-filled, because there is
no server behind the site yet. When you have hosting, point the form at a real endpoint
(Formspree, Netlify Forms, or your own handler) — the submit handler is the only thing to change.

## Still to do

- Real photography of the houses, the food and an event
- Guest names and quotes for a testimonials section
- Actual house listings with prices, if you want them public
- A domain, hosting and a Google Business profile
