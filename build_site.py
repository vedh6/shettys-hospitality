# -*- coding: utf-8 -*-
"""Generates the static pages for shettyshospitality.com.
Edit the CONTENT below and re-run:  python3 build_site.py
"""
import os, io, time

# Bumped on every build so browsers never serve a stale stylesheet or script.
BUILD_ID = int(time.time())

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

PHONE_DISPLAY = "+91 76766 43606"
PHONE_TEL = "+917676643606"
PHONE_WA = "917676643606"
EMAIL = "info@shettyshospitality.com"
INSTAGRAM = "https://www.instagram.com/shettys_hospitality/"

NAV = [
    ("index.html",        "Home"),
    ("stays.html",        "Stays"),
    ("celebrations.html", "Celebrations"),
    ("journeys.html",     "Journeys"),
    ("manpower.html",     "Manpower"),
    ("about.html",        "About"),
]

BELL = ("<svg viewBox=\"0 0 40 40\" fill=\"none\"><circle cx=\"20\" cy=\"20\" r=\"20\" fill=\"currentColor\"/>"
        "<path d=\"M20 10.6c.66 0 1.2.54 1.2 1.2v.9c2.9.56 5.05 3.1 5.05 6.15v3.6l1.5 2.35a.7.7 0 0 1-.59 1.08H12.84"
        "a.7.7 0 0 1-.59-1.08l1.5-2.35v-3.6c0-3.04 2.15-5.59 5.05-6.15v-.9c0-.66.54-1.2 1.2-1.2Z\" fill=\"#F5F2EA\"/>"
        "<path d=\"M17.6 27.6h4.8a2.4 2.4 0 0 1-4.8 0Z\" fill=\"#F5F2EA\"/></svg>")


def head(page, title, desc):
    body_class = "home" if page == "index.html" else "page"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300..700;1,300..700&family=Spectral:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css?v={BUILD_ID}" />
<script>document.documentElement.classList.add('js');</script>
</head>
<body class="{body_class}">
<a class="skip" href="#main">Skip to content</a>
"""


def header(page):
    links, drawer = [], []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == page else ''
        links.append(f'      <a href="{href}"{cur}>{label}</a>')
        drawer.append(f'    <a href="{href}"{cur}>{label}</a>')
    return f"""<header class="nav">
  <div class="nav__in">
    <a class="brand" href="index.html" aria-label="Shetty&rsquo;s Hospitality, home">
      <span class="brand__mark" aria-hidden="true">{BELL}</span>
      <span class="brand__type">
        <span class="brand__name">Shetty&rsquo;s Hospitality</span>
        <span class="brand__tag">Simplifying hospitality</span>
      </span>
    </a>
    <nav class="nav__links" aria-label="Primary">
{chr(10).join(links)}
    </nav>
    <a class="btn btn--sm" href="contact.html">Plan a stay</a>
    <button class="nav__toggle" id="navToggle" aria-expanded="false" aria-controls="navDrawer" aria-label="Open menu">
      <span></span><span></span>
    </button>
  </div>
  <div class="nav__drawer" id="navDrawer" hidden>
{chr(10).join(drawer)}
    <a href="contact.html">Plan a stay</a>
  </div>
</header>
"""


FOOTER = f"""<footer class="foot">
  <div class="foot__in">
    <div class="foot__brand">
      <span class="brand__mark brand__mark--sm" aria-hidden="true">{BELL}</span>
      <p>Shetty&rsquo;s Hospitality<br><span>Simplifying hospitality.</span></p>
    </div>
    <div class="foot__cols">
      <div>
        <h4>Pages</h4>
        <a href="stays.html">Stays</a>
        <a href="celebrations.html">Celebrations</a>
        <a href="journeys.html">Journeys</a>
        <a href="about.html">About</a>
      </div>
      <div>
        <h4>Reach us</h4>
        <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>
        <a href="mailto:{EMAIL}">{EMAIL}</a>
        <a href="https://wa.me/{PHONE_WA}" target="_blank" rel="noopener">WhatsApp</a>
        <a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a>
      </div>
      <div>
        <h4>Where</h4>
        <p>Mangalore<br>Dakshina Kannada<br>Karnataka, India</p>
      </div>
    </div>
    <p class="foot__legal">&copy; <span id="yr">2026</span> Shetty&rsquo;s Hospitality, Mangalore. A vision by Rithesh Shetty.</p>
  </div>
</footer>
<script src="assets/js/main.js?v={BUILD_ID}"></script>
</body>
</html>
"""


def cta(title, body, label="Plan a stay", href="contact.html"):
    return f"""<section class="cta">
  <div class="cta__in reveal">
    <h2>{title}</h2>
    <p>{body}</p>
    <div class="cta__row">
      <a class="btn btn--light" href="{href}">{label}</a>
      <a class="btn btn--outline" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
    </div>
  </div>
</section>
"""


def phero(eyebrow, title, lede, meta=None, image=None, alt="", variant="beside"):
    """Page mastheads. Each inner page opens differently, so the site does not read
    like the same template four times:
      beside  — copy left, image right (About)
      below   — copy, then a full-bleed landscape image (Stays)
      overlay — copy set over a full-bleed darkened image (Celebrations)
      mirror  — image left, copy right, meta running full width beneath (Journeys)
    """
    m = ""
    if meta:
        items = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in meta)
        m = f'<dl class="phero__meta">{items}</dl>'

    fig = ""
    if image:
        fig = (f'<figure class="phero__figure">'
               f'<img src="assets/img/pages/{image}?v={BUILD_ID}" alt="{alt}" />'
               f'</figure>')

    copy = f"""<div class="phero__copy">
      <p class="eyebrow{' eyebrow--light' if variant == 'overlay' else ''}">{eyebrow}</p>
      <h1>{title}</h1>
      <p class="lede">{lede}</p>
      {m if variant != 'mirror' else ''}
    </div>"""

    if variant == "below":
        return f"""<section class="phero phero--below">
  <div class="phero__in">
    {copy}
  </div>
  {fig}
</section>
"""

    if variant == "overlay":
        return f"""<section class="phero phero--overlay">
  {fig}
  <div class="phero__scrim" aria-hidden="true"></div>
  <div class="phero__in">
    {copy}
  </div>
</section>
"""

    if variant == "mirror":
        return f"""<section class="phero phero--mirror">
  <div class="phero__in">
    {fig}
    {copy}
  </div>
  {m}
  <div class="ridge" aria-hidden="true"></div>
</section>
"""

    return f"""<section class="phero">
  <div class="phero__in">
    {copy}
    {fig}
  </div>
  <div class="ridge" aria-hidden="true"></div>
</section>
"""


PAGES = {}

# ------------------------------------------------------------------ HOME
PAGES["index.html"] = dict(
title="Shetty&rsquo;s Hospitality — Homestays &amp; celebrations in Mangalore",
desc="Managed homestays, private celebrations, temple journeys and rides across Mangalore. One contact for the whole stay.",
body=f"""
<section class="vhero">
  <picture class="vhero__pic" aria-hidden="true">
    <source media="(max-width:819px)" srcset="assets/img/hero-portrait.jpg?v={BUILD_ID}" />
    <img class="vhero__media" src="assets/img/hero.jpg?v={BUILD_ID}" alt=""
         fetchpriority="high" decoding="async" />
  </picture>
  <div class="vhero__scrim" aria-hidden="true"></div>

  <div class="vhero__in">
    <p class="eyebrow eyebrow--light">Mangalore &middot; Homestays &amp; celebrations</p>
    <h1>You <em>arrive</em>. The rest is already done.</h1>
    <p class="lede">
      We keep homes across Mangalore &mdash; and we keep them ready. Beds made, kitchen stocked,
      driver briefed, temple slots held. One person arranges all of it, and stays on the phone
      from the first call to the last drop.
    </p>

    <div class="vhero__cta">
      <a class="pill" href="contact.html">
        <span class="pill__label">Plan a stay</span>
        <span class="pill__arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 7h10v10"/><path d="M7 17 17 7"/></svg><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 7h10v10"/><path d="M7 17 17 7"/></svg></span>
      </a>
      <a class="btn btn--outline" href="celebrations.html">Host a celebration</a>
    </div>

    <dl class="vhero__facts">
      <div><dt>Based in</dt><dd>Mangalore, Karnataka</dd></div>
      <div><dt>One contact for</dt><dd>Stay, rides, temples, table</dd></div>
      <div><dt>Reply within</dt><dd>A few hours, every day</dd></div>
    </dl>
  </div>
</section>

<section class="section">
  <header class="section__head reveal">
    <p class="eyebrow">The coast you have landed on</p>
    <h2>What there is to see and do here.</h2>
    <p class="section__lede">
      Most people arrive for a wedding or a temple and leave the next morning having seen the
      airport road and not much else. The coast, the ghats behind it and the kitchens in between
      are worth a good deal longer than that.
    </p>
  </header>

  <div class="mang reveal" data-mang>
    <div class="mang__tabs" role="tablist" aria-label="Around Mangalore">
      <button type="button" role="tab" data-mangtab aria-controls="mang-coast" aria-selected="true">The coast</button>
      <button type="button" role="tab" data-mangtab aria-controls="mang-kambala" aria-selected="false">Kambala</button>
      <button type="button" role="tab" data-mangtab aria-controls="mang-temples" aria-selected="false">Temples</button>
      <button type="button" role="tab" data-mangtab aria-controls="mang-table" aria-selected="false">The table</button>
      <button type="button" role="tab" data-mangtab aria-controls="mang-ghats" aria-selected="false">The ghats</button>
      <button type="button" role="tab" data-mangtab aria-controls="mang-town" aria-selected="false">The older town</button>
    </div>
    <div class="mang__stage">
      <div class="mang__overlay" aria-hidden="false">
        <div class="mang__overlay-inner">
          <div class="mang__dots" role="tablist" aria-label="Choose a picture" data-mangdots></div>
        </div>
      </div>
      <div class="mang__panel is-current" id="mang-coast" role="tabpanel" data-mangpanel>
        <figure class="mang__figure">
          <img src="assets/img/coast-road.jpg?v={BUILD_ID}" alt="The coast highway from the air, the Arabian Sea and its breakwaters on one side and a river on the other" fetchpriority="high" />
          <figcaption>The coast road &mdash; the sea on one side, a river on the other, most of the way up</figcaption>
        </figure>
        <p class="mang__text">Panambur and Tannirbhavi are the ones everybody knows, and Tannirbhavi is best reached the old way, on the ferry across the Gurupura rather than the long road round. Sasihithlu, where two rivers meet the sea, and Someshwara, where the rocks begin, are quieter and better. Surathkal has the lighthouse; Ullal has the longest stretch of empty sand. Between June and September the sea here is not for swimming and nobody local pretends otherwise — but the light on a monsoon evening is the best of the year. The sunset is the same at all of them; the crowd is not.</p>
      </div>
      <div class="mang__panel" id="mang-kambala" role="tabpanel" data-mangpanel>
        <figure class="mang__figure">
          <img src="assets/img/kambala.jpg?v={BUILD_ID}" alt="A pair of buffalo racing down a flooded paddy track at a kambala" loading="lazy" />
          <figcaption>Kambala &mdash; paired buffalo raced down a flooded paddy track, through the season</figcaption>
        </figure>
        <p class="mang__text">From about November to March, pairs of buffalo are raced down flooded paddy tracks with a man running behind them holding the reins, and half a district turns out to watch. The good meets run through the night under lights, and there is nothing polite about them. Yakshagana runs in the same months — painted faces, drums, a story that starts at ten and finishes at dawn — and bhuta kola is still performed at village shrines for the village, not for visitors. None of it is ticketed and none of it is on a schedule you will find online. Ask us what is on while you are here and we will find out.</p>
      </div>
      <div class="mang__panel" id="mang-temples" role="tabpanel" data-mangpanel>
        <figure class="mang__figure">
          <img src="assets/img/temples-wide.jpg?v={BUILD_ID}" alt="The carved pillars of the Thousand Pillar Jain basadi at Moodabidri" loading="lazy" />
          <figcaption>The Thousand Pillar basadi at Moodabidri &mdash; no two pillars alike</figcaption>
        </figure>
        <p class="mang__text">Kadri and Mangaladevi are inside the city and take an hour between them. Kateel sits on an island in the middle of the Nandini. Dharmasthala, Kukke Subrahmanya and the Krishna Matha at Udupi are each a morning&rsquo;s drive. Inland at Moodabidri stands the Thousand Pillar basadi, a Jain temple whose carved pillars are said to be all different, and which most visitors to the coast never hear about. The difference between a good darshan and three hours in a queue is knowing which line to join, which seva to book ahead, and what time the doors actually close — which is most of what we do for you.</p>
      </div>
      <div class="mang__panel" id="mang-table" role="tabpanel" data-mangpanel>
        <figure class="mang__figure">
          <img src="assets/img/food-wide.jpg?v={BUILD_ID}" alt="A coastal Karnataka meal of ghee roast, neer dosa and rava-fried fish" loading="lazy" />
          <figcaption>Kori rotti, ghee roast, neer dosa, and a Gadbad after</figcaption>
        </figure>
        <p class="mang__text">Kori rotti, chicken ghee roast, neer dosa, pundi, fish fried in rava, and a Gadbad at the end of it. Five kitchens sit within a few streets of one another and none of them cook the same way: Bunt, Udupi, Konkani, Beary and Mangalorean Catholic. The last of those is where pork sorpotel and sannas come from, which surprises people who think they know Indian food. Go to the fish market at first light and you will see tomorrow&rsquo;s menu being argued over. We will tell you where to eat, and it is rarely the place with the sign.</p>
      </div>
      <div class="mang__panel" id="mang-ghats" role="tabpanel" data-mangpanel>
        <figure class="mang__figure">
          <img src="assets/img/ghats-wide.jpg?v={BUILD_ID}" alt="A wet ghat road curving through the monsoon forest of the Western Ghats" loading="lazy" />
          <figcaption>The ghat road in the monsoon</figcaption>
        </figure>
        <p class="mang__text">An hour inland the land stands up. Charmadi and Shiradi climb through thirty-odd hairpins into coffee and pepper country, and through the monsoon the waterfalls beside the road run hard enough to hear over the engine. Agumbe, up the ghat, takes some of the heaviest rain in the country and the sunsets from the top are worth the drive on a clear evening. Bring something warm; it is ten degrees cooler up there than it is on the coast, which nobody ever believes until they arrive.</p>
      </div>
      <div class="mang__panel" id="mang-town" role="tabpanel" data-mangpanel>
        <figure class="mang__figure">
          <img src="assets/img/sultan-battery.jpg?v={BUILD_ID}" alt="The stone bastion of Sultan Battery on the Gurupura river at Boloor, Mangalore" loading="lazy" />
          <figcaption>Sultan Battery &mdash; Tipu&rsquo;s watchtower at Boloor, on the Gurupura</figcaption>
        </figure>
        <p class="mang__text">The tile factories here roofed half of south India, which is why every old building from Bombay to Colombo wears the same terracotta. The standing figure at Karkala is an easy half day inland. St Aloysius has a chapel painted floor to ceiling by an Italian Jesuit in the 1890s that almost nobody outside the city has heard of. And the old trade with Arabia and Portugal still shows in the street names, the doorways and the food, if somebody points it out.</p>
      </div>

      <div class="mang__nav">
        <div class="mang__arrows">
          <button type="button" class="mang__arrow" data-mangprev aria-label="Previous"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5"/><path d="m11 18-6-6 6-6"/></svg></button>
          <button type="button" class="mang__arrow" data-mangnext aria-label="Next"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></svg></button>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <header class="section__head reveal">
    <p class="eyebrow">What we look after</p>
    <h2>Six services, arranged by one person.</h2>
    <p class="section__lede">
      Mangalore has no shortage of good drivers, good cooks and good houses. What it lacks is
      someone holding them together. That is the whole job.
    </p>
  </header>

  <ol class="offer">
    <li class="offer__row reveal">
      <figure class="offer__media">
        <img src="assets/img/cards/stays.jpg?v={BUILD_ID}" alt="A made-up bedroom in a managed homestay, shutters open to the garden" loading="lazy" />
      </figure>
      <div class="offer__copy">
        <p class="offer__n">01</p>
        <h3><a href="stays.html">Shetty&rsquo;s Stays</a></h3>
        <p class="offer__lede">Homestays and service apartments we manage ourselves &mdash; same linen, same checklist, same standard every time you arrive.</p>
        <ul class="ticks">
          <li><b>A room or a whole house</b> &mdash; homes across the city, sized to how many of you there are</li>
          <li><b>Ready before you land</b> &mdash; cleaned, stocked and checked against the same list every time</li>
          <li><b>Staffed if you want it</b> &mdash; cook, housekeeping and airport pickup on request</li>
        </ul>
        <p class="offer__meta"><span>Nightly</span><span>Weekly</span><span>Long stay</span></p>
        <a class="link" href="stays.html">Plan a stay <span aria-hidden="true">&rarr;</span></a>
      </div>
    </li>
    <li class="offer__row reveal">
      <figure class="offer__media">
        <img src="assets/img/cards/celebrations.jpg?v={BUILD_ID}" alt="A Mangalore house decorated for a family celebration" loading="lazy" />
      </figure>
      <div class="offer__copy">
        <p class="offer__n">02</p>
        <h3><a href="celebrations.html">Celebrations at home</a></h3>
        <p class="offer__lede">Naming ceremonies, birthdays, house warmings and small weddings, hosted in your own house instead of a hall.</p>
        <ul class="ticks">
          <li><b>Taste it first</b> &mdash; menus cooked for you before you commit to anything</li>
          <li><b>Sized to the room</b> &mdash; decor, seating, lighting and sound built for a house, not a hall</li>
          <li><b>We stay till the end</b> &mdash; staff on the day, and the clearing up after everyone leaves</li>
        </ul>
        <p class="offer__meta"><span>15 to 150 guests</span></p>
        <a class="link" href="celebrations.html">Host a celebration <span aria-hidden="true">&rarr;</span></a>
      </div>
    </li>
    <li class="offer__row reveal">
      <figure class="offer__media">
        <img src="assets/img/cards/rides.jpg?v={BUILD_ID}" alt="The coast road ahead, seen from the second row of a seven-seater" loading="lazy" />
      </figure>
      <div class="offer__copy">
        <p class="offer__n">03</p>
        <h3><a href="journeys.html#rides">Shetty&rsquo;s Rides</a></h3>
        <p class="offer__lede">Drivers we know by name, cars we have sat in, and a fare agreed before you get in.</p>
        <ul class="ticks">
          <li><b>Any hour</b> &mdash; airport runs at three in the morning, the driver&rsquo;s name and number sent the night before</li>
          <li><b>Sedan to tempo traveller</b> &mdash; day cars in the city or well outside it</li>
          <li><b>The fare is agreed</b> &mdash; before you get in, not after you get out</li>
        </ul>
        <p class="offer__meta"><span>Fixed pricing</span></p>
        <a class="link" href="journeys.html#rides">See the cars <span aria-hidden="true">&rarr;</span></a>
      </div>
    </li>
    <li class="offer__row reveal">
      <figure class="offer__media">
        <img src="assets/img/cards/temples.jpg?v={BUILD_ID}" alt="The gold gopuram of Kudroli Gokarnanatha temple, Mangalore, after rain" loading="lazy" />
      </figure>
      <div class="offer__copy">
        <p class="offer__n">04</p>
        <h3><a href="journeys.html#temples">Temple journeys</a></h3>
        <p class="offer__lede">The drive is the easy part. Knowing which queue to join and when the doors close is what we handle.</p>
        <ul class="ticks">
          <li><b>Sevas booked ahead</b> &mdash; darshan timings held, so you are not guessing at the gate</li>
          <li><b>The big five</b> &mdash; Dharmasthala, Kukke, Udupi, Kateel and Kadri, done properly</li>
          <li><b>Paced for elders</b> &mdash; circuits sequenced so nobody is finished by the second day</li>
        </ul>
        <p class="offer__meta"><span>Day trips</span><span>Multi-day</span></p>
        <a class="link" href="journeys.html#temples">Plan a journey <span aria-hidden="true">&rarr;</span></a>
      </div>
    </li>
    <li class="offer__row reveal">
      <figure class="offer__media">
        <img src="assets/img/cards/hidden.jpg?v={BUILD_ID}" alt="First light at the Bunder fish market, the old port in Mangalore, the night&rsquo;s catch being sorted on the quay" loading="lazy" />
      </figure>
      <div class="offer__copy">
        <p class="offer__n">05</p>
        <h3><a href="journeys.html#hidden">Hidden Mangalore</a></h3>
        <p class="offer__lede">The parts of the coast that never make it onto a list, led by someone who actually lives here.</p>
        <ul class="ticks">
          <li><b>Where locals eat</b> &mdash; kori rotti and neer dosa, rarely the place with the sign</li>
          <li><b>First light at the market</b> &mdash; and Someshwara at low tide, when the rocks come out</li>
          <li><b>Walks with a host</b> &mdash; heritage streets, tile factories, Yakshagana in season</li>
        </ul>
        <p class="offer__meta"><span>Half day</span><span>With a host</span></p>
        <a class="link" href="journeys.html#hidden">Walk with us <span aria-hidden="true">&rarr;</span></a>
      </div>
    </li>
    <li class="offer__row reveal">
      <figure class="offer__media">
        <img src="assets/img/manpower.jpg?v={BUILD_ID}" alt="Service staff laying a long table before guests arrive" loading="lazy" />
      </figure>
      <div class="offer__copy">
        <p class="offer__n">06</p>
        <h3><a href="contact.html">Staff, by the day</a></h3>
        <p class="offer__lede">The same cooks, servers and decorators we use on our own events, available to you on yours.</p>
        <ul class="ticks">
          <li><b>Kitchen and service</b> &mdash; cooks, waiters and cleaners, by the day</li>
          <li><b>Decor and setup</b> &mdash; the crews who build it, and the team that clears after</li>
          <li><b>Yours or theirs</b> &mdash; for your own event, or to fill out someone else&rsquo;s</li>
        </ul>
        <p class="offer__meta"><span>Rates to follow</span></p>
        <a class="link" href="contact.html">Tell us what you need <span aria-hidden="true">&rarr;</span></a>
      </div>
    </li>
  </ol>

  <p class="offer__note reveal">
    Not sure yet? Most people call with dates and a rough idea, and we build the rest around
    it. There is no charge for asking.
    <a class="link" href="contact.html">Tell us what you need <span aria-hidden="true">&rarr;</span></a>
  </p>
</section>

<section class="section">
  <header class="section__head reveal">
    <p class="eyebrow">Where to next</p>
    <h2>Read about each one in full.</h2>
  </header>

  <nav class="jump reveal" aria-label="The four service pages">
    <a class="jcard" href="stays.html">
      <img class="jcard__img" src="assets/img/cards/stays-card.jpg?v={BUILD_ID}" alt="" loading="lazy" />
      <span class="jcard__veil" aria-hidden="true"></span>
      <span class="jcard__body">
        <span class="jcard__sub">Homestays and service apartments</span>
        <span class="jcard__title">Stays</span>
      </span>
    </a>
    <a class="jcard" href="celebrations.html">
      <img class="jcard__img" src="assets/img/cards/celebrations-card.jpg?v={BUILD_ID}" alt="" loading="lazy" />
      <span class="jcard__veil" aria-hidden="true"></span>
      <span class="jcard__body">
        <span class="jcard__sub">Functions hosted at home</span>
        <span class="jcard__title">Celebrations</span>
      </span>
    </a>
    <a class="jcard" href="journeys.html">
      <img class="jcard__img" src="assets/img/cards/journeys-card.jpg?v={BUILD_ID}" alt="" loading="lazy" />
      <span class="jcard__veil" aria-hidden="true"></span>
      <span class="jcard__body">
        <span class="jcard__sub">Temples, cars and days out</span>
        <span class="jcard__title">Journeys</span>
      </span>
    </a>
    <a class="jcard" href="manpower.html">
      <img class="jcard__img" src="assets/img/cards/manpower-card.jpg?v={BUILD_ID}" alt="" loading="lazy" />
      <span class="jcard__veil" aria-hidden="true"></span>
      <span class="jcard__body">
        <span class="jcard__sub">Cooks, servers and setup crews</span>
        <span class="jcard__title">Manpower</span>
      </span>
    </a>
  </nav>
</section>

<section class="promise">
  <p class="eyebrow eyebrow--light">Our promise</p>
  <p class="promise__words reveal"><span>Reliable.</span> <span>Coordinated.</span> <span>Complete.</span></p>
  <p class="promise__by">A vision by Rithesh Shetty</p>
</section>

<section class="wordof">
  <div class="tsplit" data-tsplit>
    <div class="tsplit__copy">

      <article class="tsplit__item is-active" data-testimonial>
        <p class="tsplit__tag"><span class="tsplit__hr" aria-hidden="true"></span>In every house</p>

        <blockquote class="tsplit__quote">
          Cleaned and checked against the same written list. Every arrival, not most of them.
        </blockquote>

        <div class="tsplit__by">
          <span class="tsplit__hr" aria-hidden="true"></span>
          <div>
            <p class="tsplit__name">By someone who has been in the house before</p>
            <p class="tsplit__role">Linen changed and kept separate between stays</p>
          </div>
        </div>
      </article>

      <article class="tsplit__item" data-testimonial>
        <p class="tsplit__tag"><span class="tsplit__hr" aria-hidden="true"></span>Your privacy</p>

        <blockquote class="tsplit__quote">
          Cameras in the common areas only. Never inside a room.
        </blockquote>

        <div class="tsplit__by">
          <span class="tsplit__hr" aria-hidden="true"></span>
          <div>
            <p class="tsplit__name">The same rule in every property we run</p>
            <p class="tsplit__role">Fire extinguishers, first aid and emergency lighting on site</p>
          </div>
        </div>
      </article>

      <article class="tsplit__item" data-testimonial>
        <p class="tsplit__tag"><span class="tsplit__hr" aria-hidden="true"></span>On the road</p>

        <blockquote class="tsplit__quote">
          The figure you agree at the start is the figure at the end.
        </blockquote>

        <div class="tsplit__by">
          <span class="tsplit__hr" aria-hidden="true"></span>
          <div>
            <p class="tsplit__name">Tolls, parking and the driver&rsquo;s allowance are inside it</p>
            <p class="tsplit__role">On overnight runs, so is his stay</p>
          </div>
        </div>
      </article>

      <article class="tsplit__item" data-testimonial>
        <p class="tsplit__tag"><span class="tsplit__hr" aria-hidden="true"></span>One number</p>

        <blockquote class="tsplit__quote">
          One person arranges all of it, and stays on the phone from the first call to the last drop.
        </blockquote>

        <div class="tsplit__by">
          <span class="tsplit__hr" aria-hidden="true"></span>
          <div>
            <p class="tsplit__name">Stay, rides, temples, table</p>
            <p class="tsplit__role">A few hours to reply, every day</p>
          </div>
        </div>
      </article>

      <p class="tsplit__note">
        These are what we hold ourselves to, not things we have been told. Guest words will go here
        once we have asked the people who said them, printed whole, with what was actually arranged
        set out beside them.
        <a class="link" href="contact.html">Stayed with us? Send us yours <span aria-hidden="true">&rarr;</span></a>
      </p>

      <div class="tsplit__dots" data-dots hidden></div>
    </div>

    <div class="tsplit__visual">
    <!-- The path is relative to styles.css, not to this page: a url() carried in a custom
     property resolves against the stylesheet that USES it, and the only consumer is
     .vplayer::before. Written page-relative it resolved to /assets/css/assets/img/ and 404d. -->
    <figure class="vplayer" data-vplayer style="--poster:url(../img/review-poster.jpg?v={BUILD_ID})">
    <video class="vplayer__video" playsinline preload="metadata"
    poster="assets/img/review-poster.jpg?v={BUILD_ID}"
    aria-label="A guest talking about their stay">
    <source src="assets/video/review.mp4?v={BUILD_ID}" type="video/mp4" />
    </video>

  
    <div class="vplayer__bar">
    <div class="vplayer__seekrow">
    <span class="vplayer__time" data-current>0:00</span>
    <input class="vplayer__seek" type="range" min="0" max="100" value="0" step="0.01"
    aria-label="Seek through the video" />
    <span class="vplayer__time" data-duration>0:00</span>
    </div>
    <div class="vplayer__btns">
    <div class="vplayer__group">
    <button type="button" data-skip="-10" aria-label="Back 10 seconds"><svg class="" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="19 20 9 12 19 4 19 20"/><line x1="5" x2="5" y1="19" y2="5"/></svg></button>
    <button type="button" data-play aria-label="Play"><svg class="i-play" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="6 3 20 12 6 21 6 3"/></svg><svg class="i-pause" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="14" y="4" width="4" height="16" rx="1"/><rect x="6" y="4" width="4" height="16" rx="1"/></svg></button>
    <button type="button" data-skip="10" aria-label="Forward 10 seconds"><svg class="" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="5 4 15 12 5 20 5 4"/><line x1="19" x2="19" y1="5" y2="19"/></svg></button>
    <div class="vplayer__vol">
    <button type="button" data-mute aria-label="Mute"><svg class="i-vol" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 4.7a.7.7 0 0 0-1.2-.5L6.4 7.6A1.4 1.4 0 0 1 5.4 8H3a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2.4a1.4 1.4 0 0 1 1 .4l3.4 3.4a.7.7 0 0 0 1.2-.5z"/><path d="M16 9a5 5 0 0 1 0 6"/><path d="M19.4 18.4a9 9 0 0 0 0-12.8"/></svg><svg class="i-mute" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 4.7a.7.7 0 0 0-1.2-.5L6.4 7.6A1.4 1.4 0 0 1 5.4 8H3a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2.4a1.4 1.4 0 0 1 1 .4l3.4 3.4a.7.7 0 0 0 1.2-.5z"/><line x1="22" x2="16" y1="9" y2="15"/><line x1="16" x2="22" y1="9" y2="15"/></svg></button>
    <input class="vplayer__volume" type="range" min="0" max="1" step="0.05" value="1"
    aria-label="Volume" />
    </div>
    </div>
    <button type="button" data-fullscreen aria-label="Full screen"><svg class="i-max" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 3H5a2 2 0 0 0-2 2v3"/><path d="M21 8V5a2 2 0 0 0-2-2h-3"/><path d="M3 16v3a2 2 0 0 0 2 2h3"/><path d="M16 21h3a2 2 0 0 0 2-2v-3"/></svg><svg class="i-min" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 3v3a2 2 0 0 1-2 2H3"/><path d="M21 8h-3a2 2 0 0 1-2-2V3"/><path d="M3 16h3a2 2 0 0 1 2 2v3"/><path d="M16 21v-3a2 2 0 0 1 2-2h3"/></svg></button>
    </div>
    </div>
    </figure>
      <p class="reel__cap">
        <span class="reel__kicker">Guest review</span>
        <a href="https://www.instagram.com/shettys_hospitality/" target="_blank" rel="noopener">@shettys_hospitality</a>
      </p>
    </div>
  </div>
</section>

<section class="section split">
  <figure class="split__media reveal">
    <div class="ph">
      <img src="assets/img/detail-wide.jpg" alt="Interior of a managed homestay" />
    </div>
  </figure>
  <div class="split__copy reveal">
    <p class="eyebrow">Why one contact matters</p>
    <h2>One person arranges the whole trip.</h2>
    <p>
      The usual trip means a booking site, a driver who calls at midnight, a cook who cancels,
      and a temple queue nobody warned you about. We put one person between you and all of it,
      and that person stays with you from the first call to the last drop.
    </p>
    <ul class="ticks">
      <li>One plan, one price, one number to call</li>
      <li>Verified drivers, cooks and caretakers we work with regularly</li>
      <li>Someone on the ground in Mangalore, not a call centre</li>
      <li>The same standard whether you stay two nights or two months</li>
    </ul>
    <a class="link" href="about.html">How we work <span aria-hidden="true">&rarr;</span></a>
  </div>
</section>

{cta("Tell us the dates. We&rsquo;ll take it from there.",
     "Send an enquiry and we&rsquo;ll come back with a plan and a price, usually the same day. No deposit to ask a question.",
     "Send an enquiry")}
""")

# ------------------------------------------------------------------ STAYS
PAGES["stays.html"] = dict(
title="Stays — Shetty&rsquo;s Hospitality, Mangalore",
desc="Managed homestays and service apartments in Mangalore. Cleaned before every arrival, stocked kitchen, cook on request, airport pickup arranged.",
body=phero("Shetty&rsquo;s Stays", "Managed homestays<br>across Mangalore.",
  "Every house on our list is one we manage. We know which geyser is slow, which room catches the "
  "afternoon sun, and how long the drive to the airport really takes at 6am.",
  [("Stay length", "One night to several months"), ("Group size", "2 to 20 guests"), ("Ready", "Cleaned before every arrival")],
  image="stays.jpg", alt="A bedroom in one of our managed homes", variant="below") + f"""
<section class="section">
  <header class="section__head section__head--left reveal">
    <p class="eyebrow">The houses</p>
    <h2>Each one managed by us.</h2>
    <p class="section__lede">Each of these is a house we manage ourselves. Details are being
    collected &mdash; names, sizes and neighbourhoods go in below.</p>
  </header>

  <div class="houses">
    <article class="house reveal">
      <figure class="house__media">
        <img src="assets/img/houses/house-1.jpg?v={BUILD_ID}" alt="" loading="lazy" />
      </figure>
      <p class="house__kind">A whole house</p>
      <h3 class="house__name">House one &mdash; name to follow</h3>
      <p class="house__line">A short line about what this house is good for goes here.</p>
      <dl class="house__meta">
        <div><dt>Sleeps</dt><dd>Sleeps 0 &middot; 0 bedrooms</dd></div>
        <div><dt>Where</dt><dd>Area of Mangalore to follow</dd></div>
      </dl>
    </article>

    <article class="house reveal">
      <figure class="house__media">
        <img src="assets/img/houses/house-2.jpg?v={BUILD_ID}" alt="" loading="lazy" />
      </figure>
      <p class="house__kind">An apartment</p>
      <h3 class="house__name">House two &mdash; name to follow</h3>
      <p class="house__line">A short line about what this house is good for goes here.</p>
      <dl class="house__meta">
        <div><dt>Sleeps</dt><dd>Sleeps 0 &middot; 0 bedrooms</dd></div>
        <div><dt>Where</dt><dd>Area of Mangalore to follow</dd></div>
      </dl>
    </article>

    <article class="house reveal">
      <figure class="house__media">
        <img src="assets/img/houses/house-3.jpg?v={BUILD_ID}" alt="" loading="lazy" />
      </figure>
      <p class="house__kind">A sea-facing house</p>
      <h3 class="house__name">House three &mdash; name to follow</h3>
      <p class="house__line">A short line about what this house is good for goes here.</p>
      <dl class="house__meta">
        <div><dt>Sleeps</dt><dd>Sleeps 0 &middot; 0 bedrooms</dd></div>
        <div><dt>Where</dt><dd>Area of Mangalore to follow</dd></div>
      </dl>
    </article>
  </div>
</section>

<section class="section">
  <header class="section__head section__head--left reveal">
    <p class="eyebrow">In every house</p>
    <h2>Checked before every arrival.</h2>
  </header>

  <div class="bento reveal">
    <figure class="bento__cell bento__cell--lead">
      <img class="bento__img" src="assets/img/pages/stays-housekeeping.jpg?v={BUILD_ID}" alt="Housekeeping drawing a fresh sheet taut across a bed, folded towels waiting on a stool beside it" loading="lazy" />
      <span class="bento__veil" aria-hidden="true"></span>
      <figcaption class="bento__lead">
        <h3>Cleaned and inspected before every arrival</h3>
        <p>Room by room, against the same written checklist every time &mdash; by someone who has
        been in the house before.</p>
      </figcaption>
    </figure>

    <div class="bento__cell">
      <h3>Fresh linen and towels</h3>
      <p>Beds made up before you land, not left folded on the mattress.</p>
    </div>

    <div class="bento__cell">
      <h3>Stocked kitchen</h3>
      <p>Filtered water and the basics already in.</p>
    </div>

    <div class="bento__cell">
      <h3>Wi-Fi and hot water</h3>
      <p>Backup power where the house has it.</p>
    </div>

    <div class="bento__cell">
      <h3>Parking, and a caretaker</h3>
      <p>A name and a number that answers.</p>
    </div>

    <div class="bento__cell">
      <h3>Airport pickup</h3>
      <p>Arranged with the booking, at any hour.</p>
    </div>
  </div>

  <p class="bento__after"><a class="link" href="contact.html">Check dates <span aria-hidden="true">&rarr;</span></a></p>
</section>

<section class="section band cone">
  <div class="band__in">
    <div class="cone__grid">
      <div class="cone__copy reveal">
        <p class="eyebrow eyebrow--light">In development</p>
        <h2>Small cabins, coming to the coast.</h2>
        <p class="section__lede">
          Compact A-frame cabins on land we take on with the owner. We design them, build them
          and run them ourselves.
        </p>
        <ul class="ticks ticks--light">
          <li>300 to 400 sq ft, built for two, private, with a deck of its own</li>
          <li>King bed, good linen, air conditioning, hot water and an attached bathroom</li>
          <li>Wi-Fi and a smart TV, for the afternoons the rain does not let up</li>
          <li>Turned over against a written checklist between stays, linen changed and kept separate</li>
          <li>Fire extinguishers, first aid and emergency lighting. Cameras in the common areas only, never inside a cabin</li>
          <li>First sites on the coast and around Chikkamagaluru</li>
        </ul>
        <p class="cone__note">
          Still in development. The picture is a concept, not a finished build.
        </p>
        <div class="cone__contact">
          <p>For more on the cabins, or if you have land that might suit:</p>
          <p class="cone__lines">
            <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>
            <a href="https://wa.me/{PHONE_WA}" target="_blank" rel="noopener">WhatsApp</a>
            <a href="mailto:{EMAIL}">{EMAIL}</a>
          </p>
        </div>
      </div>
      <figure class="cone__media reveal">
        <img src="assets/img/cone-houses.jpg?v={BUILD_ID}"
             alt="A concept view of A-frame cabins in a palm clearing" loading="lazy" />
      </figure>
    </div>
  </div>
</section>

<section class="section">
  <header class="section__head reveal">
    <p class="eyebrow">Kinds of stay</p>
    <h2>Stays for different kinds of trip.</h2>
  </header>
  <ul class="cards cards--3">
    <li class="card reveal">
      <h3>The short visit</h3>
      <p>A few nights for a wedding, a hospital visit or a temple trip. Arrival any hour, car waiting, breakfast sorted.</p>
      <p class="card__meta">1&ndash;4 nights</p>
    </li>
    <li class="card reveal">
      <h3>The homecoming</h3>
      <p>For families and NRIs back for a season. A whole house, a cook who knows your food, and help with the errands nobody enjoys.</p>
      <p class="card__meta">1 week to 3 months</p>
    </li>
    <li class="card reveal">
      <h3>The work stay</h3>
      <p>Service apartments for project teams and corporate guests. Invoiced monthly, serviced weekly, same standard in each unit.</p>
      <p class="card__meta">Corporate billing</p>
    </li>
  </ul>
</section>

<section class="section">
  <header class="section__head reveal">
    <p class="eyebrow">Add on request</p>
    <h2>What you can add to a stay.</h2>
  </header>
  <ul class="chips reveal">
    <li>Cook, Mangalorean or your family&rsquo;s usual</li>
    <li>Daily housekeeping</li>
    <li>Airport pickup at any hour</li>
    <li>Car and driver for the stay</li>
    <li>Crib, high chair, extra mattresses</li>
    <li>Grocery stocking before arrival</li>
    <li>Elder-friendly ground floor rooms</li>
    <li>Laundry and ironing</li>
  </ul>
</section>

{cta("Send us your dates and we&rsquo;ll send back the houses.",
     "Tell us how many of you there are and roughly where you want to be. We&rsquo;ll reply with what&rsquo;s free and what it costs.",
     "Check availability")}
""")

# ------------------------------------------------------------------ CELEBRATIONS
PAGES["celebrations.html"] = dict(
title="Celebrations at home — Shetty&rsquo;s Hospitality, Mangalore",
desc="Naming ceremonies, house warmings, birthdays and intimate weddings hosted at home in Mangalore. Kitchen, decor, staff and clean-up handled.",
body=phero("Celebrations at home", "Celebrations hosted<br>in your own home.",
  "A house party is only relaxing for the people who did not plan it. We take the planning &mdash; the cooks, "
  "the pandal, the chairs, the flowers, the parking, the plates going back to the rental at midnight &mdash; "
  "and hand you back the evening.",
  [("Guests", "15 to 150"), ("Notice", "Two weeks is comfortable"), ("On the day", "A coordinator, start to finish")],
  image="celebrations.jpg", alt="Banana leaves being laid for a family meal at home", variant="overlay") + f"""
<section class="section occ reveal" data-occ>
  <div class="occ__stage">
  <article class="occ__slide split is-current" data-occasion aria-label="Birthdays">
    <div class="split__copy">
      <p class="eyebrow">Birthdays</p>
      <h2>Smaller parties, planned properly.</h2>
        <p>Most of what we are asked for is not a hundred and fifty people. It is twenty or thirty, in a courtyard, on a Sunday evening &mdash; a child&rsquo;s birthday, a first birthday, an anniversary the family never wanted to move to a hall in the first place.</p>
        <p>Those need less building and more judgement. How much food actually gets eaten. Where the children will end up running once the cake is cut. How loud is too loud in a house with neighbours on both sides. We scale the evening down properly rather than shrinking a package meant for a crowd.</p>
      <a class="link" href="contact.html">Tell us about the occasion <span aria-hidden="true">&rarr;</span></a>
    </div>
    <figure class="split__media">
      <div class="ph">
        <img src="assets/img/occasions/birthday.jpg?v={BUILD_ID}"
             srcset="assets/img/occasions/birthday-700.jpg?v={BUILD_ID} 700w,
                     assets/img/occasions/birthday.jpg?v={BUILD_ID} 1200w"
             sizes="(max-width: 860px) 90vw, 42vw"
             alt="A birthday table laid on the verandah of a Mangalore house" loading="lazy" />
      </div>
    </figure>
  </article>
  <article class="occ__slide split" data-occasion aria-label="Family reunions">
    <div class="split__copy">
      <p class="eyebrow">Family reunions</p>
      <h2>A week of family under one roof.</h2>
        <p>When three families land at once and stay for a week, the hard part is not the welcome dinner. It is the seventh morning, when everyone wants breakfast at a different hour and two people have decided to fast.</p>
        <p>So we staff it as a household rather than an event. The kitchen keeps going between meals, diets are written down instead of guessed at, and the cleaning and the airport runs happen without anybody having to ask. Nobody spends their holiday cooking for twenty.</p>
      <a class="link" href="contact.html">Tell us about the occasion <span aria-hidden="true">&rarr;</span></a>
    </div>
    <figure class="split__media">
      <div class="ph">
        <img src="assets/img/occasions/reunion.jpg?v={BUILD_ID}"
             srcset="assets/img/occasions/reunion-700.jpg?v={BUILD_ID} 700w,
                     assets/img/occasions/reunion.jpg?v={BUILD_ID} 1200w"
             sizes="(max-width: 860px) 90vw, 42vw"
             alt="A long family lunch laid out on the verandah of a coastal Karnataka house" loading="lazy" />
      </div>
    </figure>
  </article>
  <article class="occ__slide split" data-occasion aria-label="Corporate offsites">
    <div class="split__copy">
      <p class="eyebrow">Corporate offsites</p>
      <h2>Team dinners and small offsites.</h2>
        <p>Team dinners and small offsites work better in a house than in a banquet room &mdash; right up until somebody needs the timings held to the minute, or a proper invoice at the end.</p>
        <p>So we run those parts like a venue and leave the rest feeling like a house. Fixed serving times, power and space sorted before anyone arrives, a setup that stays out of the way of whatever the session is, and a single invoice for your accounts team.</p>
      <a class="link" href="contact.html">Tell us about the occasion <span aria-hidden="true">&rarr;</span></a>
    </div>
    <figure class="split__media">
      <div class="ph">
        <img src="assets/img/occasions/offsite.jpg?v={BUILD_ID}"
             srcset="assets/img/occasions/offsite-700.jpg?v={BUILD_ID} 700w,
                     assets/img/occasions/offsite.jpg?v={BUILD_ID} 1200w"
             sizes="(max-width: 860px) 90vw, 42vw"
             alt="A long table set for a private dinner on a lit verandah at dusk" loading="lazy" />
      </div>
    </figure>
  </article>
  </div>
  <div class="occ__dots" data-occ-dots hidden></div>
</section>

<section class="section">
  <header class="section__head reveal">
    <p class="eyebrow">Occasions</p>
    <h2>The occasions we take on.</h2>
  </header>
  <ul class="bento2 reveal">
    <li class="bcard bcard--span-4 reveal">
      <figure class="bcard__media">
        <img src="assets/img/occasions/naming.jpg?v={BUILD_ID}" alt="A flower-hung wooden cradle and brass lamp set out on a verandah" loading="lazy" />
      </figure>
      <div class="bcard__body">
        <h3>Naming and cradle ceremonies</h3>
        <p>Morning functions that start early and fill the house with elders and small children. We plan for both: chairs with backs, shade where people wait, and a menu that leans sweet and is ready when the ceremony ends rather than an hour after.</p>
      </div>
    </li>
    <li class="bcard bcard--span-2 reveal">
      <figure class="bcard__media">
        <img src="assets/img/occasions/housewarming.jpg?v={BUILD_ID}" alt="A rangoli, brass kalasha and lit lamps at a threshold before dawn" loading="lazy" />
      </figure>
      <div class="bcard__body">
        <h3>House warming</h3>
        <p>Griha pravesha at whatever hour the priest gives you, which is often before light. We handle what the pooja needs, keep the kitchen running from dawn, and turn the house around for a full lunch once the ritual is done.</p>
      </div>
    </li>
    <li class="bcard bcard--span-2 reveal">
      <figure class="bcard__media">
        <img src="assets/img/occasions/birthday.jpg?v={BUILD_ID}" alt="A birthday table laid on the verandah of a Mangalore house" loading="lazy" />
      </figure>
      <div class="bcard__body">
        <h3>Birthdays and anniversaries</h3>
        <p>Evening parties, usually smaller. A first birthday and a sixtieth need very different rooms, so we scale the seating, the sound and the food to the actual guest list instead of a package.</p>
      </div>
    </li>
    <li class="bcard bcard--span-4 reveal">
      <figure class="bcard__media">
        <img src="assets/img/occasions/roce.jpg?v={BUILD_ID}" alt="Brass bowls of coconut milk and turmeric set out for a roce" loading="lazy" />
      </figure>
      <div class="bcard__body">
        <h3>Intimate weddings and roce</h3>
        <p>Roce, mehendi, haldi and small weddings held at home rather than in a hall. These run across days and involve family doing things themselves, so we work around the household instead of taking it over.</p>
      </div>
    </li>
    <li class="bcard bcard--span-3 reveal">
      <figure class="bcard__media">
        <img src="assets/img/occasions/reunion.jpg?v={BUILD_ID}" alt="A long family lunch laid out on the verandah of a coastal Karnataka house" loading="lazy" />
      </figure>
      <div class="bcard__body">
        <h3>Family reunions and NRI homecomings</h3>
        <p>Several families under one roof for a week, with different diets, different sleep schedules and a lot of catching up. Meals stay flexible, the kitchen keeps going, and nobody is cooking for twenty on their holiday.</p>
      </div>
    </li>
    <li class="bcard bcard--span-3 reveal">
      <figure class="bcard__media">
        <img src="assets/img/occasions/offsite.jpg?v={BUILD_ID}" alt="A long table set for a private dinner on a lit verandah at dusk" loading="lazy" />
      </figure>
      <div class="bcard__body">
        <h3>Corporate offsites and dinners</h3>
        <p>Team dinners and small offsites in a house instead of a banquet room. Fixed timings, a quiet setup that stays out of the way, and a single invoice at the end for your accounts team.</p>
      </div>
    </li>
  </ul>
</section>

<section class="section band">
  <div class="band__in">
    <header class="section__head section__head--left reveal">
      <p class="eyebrow eyebrow--light">What we bring</p>
      <h2>Kitchen, setting and staff.</h2>
    </header>
    <div class="incl reveal">
      <div><h4>Kitchen</h4><p>Mangalorean, Udupi or North Indian menus with cooks we work with regularly. Tasting before you commit, and enough food that nobody counts.</p></div>
      <div><h4>Setting</h4><p>Decor, seating, lighting and sound scaled to the house &mdash; not a banquet hall dropped into a living room.</p></div>
      <div><h4>Hands</h4><p>Service staff, a coordinator on the day, and a team that stays until the house is back to normal.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <header class="section__head reveal">
    <p class="eyebrow">How the day runs</p>
    <h2>One coordinator, start to finish.</h2>
  </header>
  <ol class="steps">
    <li class="reveal"><span class="steps__n">01</span><h3>A walkthrough</h3><p>We see the house, count the seats, find the power points and work out where the food goes.</p></li>
    <li class="reveal"><span class="steps__n">02</span><h3>A written plan</h3><p>Menu, decor, staff, timings and a single price. Changes are fine until the week before.</p></li>
    <li class="reveal"><span class="steps__n">03</span><h3>Setup morning</h3><p>Our team arrives early. By the time guests come, the house looks like it was always meant to look that way.</p></li>
    <li class="reveal"><span class="steps__n">04</span><h3>And after</h3><p>Clearing, rentals returned, rubbish out. You wake up to your own house.</p></li>
  </ol>
</section>

{cta("Tell us about the occasion.",
     "Date, rough guest count, and whose house it is. We&rsquo;ll come back with a menu and a number.",
     "Start planning")}
""")

# ------------------------------------------------------------------ JOURNEYS
PAGES["journeys.html"] = dict(
title="Journeys — temples, rides &amp; Hidden Mangalore | Shetty&rsquo;s Hospitality",
desc="Temple journeys to Dharmasthala, Kukke and Udupi, airport transfers and day cars, plus curated local experiences around Mangalore.",
body=phero("Journeys", "Temples, cars<br>and days out.",
  "Temples, transport and the parts of Mangalore that never make it onto a list. Booked as one plan, "
  "with one person answering the phone.",
  [("Temples", "Dharmasthala &middot; Kukke &middot; Udupi"), ("Cars", "Fixed fares, verified drivers"), ("Local", "Half-day walks with a host")],
  image="journeys.jpg", alt="Stone steps up to a coastal Karnataka temple at first light", variant="mirror") + f"""
<section class="section" id="temples">
  <header class="section__head reveal">
    <p class="eyebrow">Temple &amp; spiritual travel</p>
    <h2>Temple trips, arranged properly.</h2>
    <p class="section__lede">
      The drive is the easy part. Knowing which queue to join, when the doors close, which seva to book
      ahead and where elders can sit down &mdash; that is what we handle.
    </p>
  </header>
  <ul class="cards cards--3 cards--temples">
    <li class="card reveal">
      <img class="card__bg" src="assets/img/temples/dharmasthala.jpg?v={BUILD_ID}" alt="Dharmasthala temple below the misted Western Ghats in the monsoon" loading="lazy" />
      <h3>Dharmasthala</h3>
      <p>A Shiva temple that has been looked after by a Jain family for centuries, which tells you something about how this coast works. Everyone who comes is fed, free, in a hall that seats thousands &mdash; that is the part people remember. Go early: the queue builds through the morning. The Bahubali monolith on the hill above is a short climb and worth the detour.</p>
      <p class="card__meta">2.5 hrs from Mangalore</p>
    </li>
    <li class="card reveal">
      <img class="card__bg" src="assets/img/temples/kukke.jpg?v={BUILD_ID}" alt="The white gopuram of Kukke Subrahmanya temple against a clear sky" loading="lazy" />
      <h3>Kukke Subrahmanya</h3>
      <p>Subrahmanya worshipped here as the serpent king, which is why people come from across the country for Sarpa Samskara and Ashlesha Bali, the rites for naga dosha. Both must be booked well ahead and both start early. Pilgrims bathe in the Kumaradhara before darshan. The temple sits at the foot of Kumara Parvatha and the country around it is the greenest you will see.</p>
      <p class="card__meta">3 hrs from Mangalore</p>
    </li>
    <li class="card reveal">
      <img class="card__bg" src="assets/img/temples/udupi.jpg?v={BUILD_ID}" alt="The decorated temple chariot in the car street at Udupi Krishna Matha" loading="lazy" />
      <h3>Udupi Krishna Matha</h3>
      <p>You see the Krishna through the Kanakana Kindi, a small silver-plated window &mdash; the story goes that the idol turned to face a devotee who had been refused entry. Founded by Madhvacharya in the thirteenth century, and run in turn by eight mathas; the handover, Paryaya, comes round every two years and fills the town. Malpe and the basalt columns of St Mary&rsquo;s Island are twenty minutes on.</p>
      <p class="card__meta">1.5 hrs from Mangalore</p>
    </li>
    <li class="card reveal">
      <img class="card__bg" src="assets/img/temples/kateel.jpg?v={BUILD_ID}" alt="The red and gold gateway of Kateel Durgaparameshwari temple" loading="lazy" />
      <h3>Kateel Durgaparameshwari</h3>
      <p>The temple stands on an islet in the middle of the Nandini, so in the monsoon the river runs on both sides of it. It keeps one of the best-known Yakshagana melas on the coast &mdash; if you are here in season, ask and we will find out where the troupe is playing. Close enough to the airport to fit on the way in or the way out.</p>
      <p class="card__meta">45 min from the city</p>
    </li>
    <li class="card reveal">
      <img class="card__bg" src="assets/img/temples/kadri.jpg?v={BUILD_ID}" alt="The pale blue gopuram of Kadri Manjunatha temple with gilded figures" loading="lazy" />
      <h3>Kadri Manjunatha</h3>
      <p>Inside the city, on a hill above it. The bronze Lokeshvara in the sanctum is dated to the tenth century and is among the finest bronzes in south India. Behind the temple are nine spring-fed tanks, and above those the Jogi Mutt, which ties the place to the Natha yogis. A good first stop the morning after you land.</p>
      <p class="card__meta">In Mangalore</p>
    </li>
    <li class="card card--ask reveal">
      <h3>A circuit</h3>
      <p>Three or four of these over two days, sequenced so the driving works, the darshan
      timings line up and nobody is finished by the second afternoon. Tell us who is travelling
      and how long you have, and we will lay it out.</p>
      <p class="card__meta"><a class="link" href="contact.html">Plan a circuit <span aria-hidden="true">&rarr;</span></a></p>
    </li>
  </ul>
</section>

<section class="section band" id="rides">
  <div class="band__in">
    <header class="section__head section__head--left reveal">
      <p class="eyebrow eyebrow--light">Shetty&rsquo;s Rides</p>
      <h2>Cars and drivers at a fixed fare.</h2>
      <p class="section__lede">
        Drivers we know by name, cars we have sat in, and no surprise at the end of the day.
      </p>
    </header>
    <div class="incl incl--pics reveal">
      <div>
        <h4>Airport transfers</h4>
        <p>Mangalore International, at any hour. The driver&rsquo;s name, number and vehicle
        reach you the night before, so nobody is scanning a crowd at three in the morning.
        We watch the flight rather than the clock &mdash; if you land two hours late, the car
        is still there and the fare is still the one we quoted.</p>
        <img class="incl__pic" src="assets/img/rides/airport.jpg?v={BUILD_ID}" alt="A driver loading a suitcase into a waiting car at an airport kerb at night" loading="lazy" />
      </div>
      <div>
        <h4>Day cars</h4>
        <p>A car and driver for a half day or a full day, in the city or well outside it.
        Sedans for two or three, SUVs for a family with luggage, tempo travellers for a group
        travelling together. The driver stays with you between stops, so there is no rebooking
        after lunch and no waiting at a temple gate for something to turn up.</p>
        <img class="incl__pic" src="assets/img/rides/daycar.jpg?v={BUILD_ID}" alt="A car and driver waiting in the shade on a quiet temple road" loading="lazy" />
      </div>
      <div>
        <h4>Outstation</h4>
        <p>Udupi, Coorg, Chikmagalur, Kasaragod and the routes in between, priced per trip
        rather than per kilometre. Tolls, parking and the driver&rsquo;s allowance are inside the
        number we give you, and on overnight runs so is his stay. The figure you agree at the
        start is the figure at the end.</p>
        <img class="incl__pic" src="assets/img/rides/outstation.jpg?v={BUILD_ID}" alt="A car pulled in at a hill viewpoint above the coast, ridges going blue with distance" loading="lazy" />
      </div>
    </div>
  </div>
</section>

<section class="section" id="hidden">
  <header class="section__head reveal">
    <p class="eyebrow">Hidden Mangalore</p>
    <h2>Half days out with a local host.</h2>
    <p class="section__lede">
      Led by someone who lives here, not a script. Pick one, or let us build a morning around what you like.
    </p>
  </header>
  <ul class="chips reveal">
    <li>Kori rotti and neer dosa, where locals eat</li>
    <li>The fish market at first light</li>
    <li>Someshwara rocks at low tide</li>
    <li>Old Mangalore tile factories</li>
    <li>Basel Mission heritage walk</li>
    <li>Sultan Battery and the boat across</li>
    <li>Cashew and coffee buying, properly</li>
    <li>Yakshagana, in season</li>
  </ul>
</section>

{cta("Plan the whole trip with us.",
     "Tell us who&rsquo;s travelling and what matters most. We&rsquo;ll sequence the temples, the cars and the free afternoons.",
     "Plan a journey")}
""")

# ------------------------------------------------------------------ MANPOWER
# Everything on this page comes from what service 06 on the Home page already
# claims - cooks, waiters, cleaners, decor crews, the team that clears after,
# for your own event or someone else's, rates to follow. No rates, no headcounts
# and no guarantees have been invented here; Rithesh has not given us any.
PAGES["manpower.html"] = dict(
title="Staff by the day &mdash; cooks, servers and setup crews | Shetty&rsquo;s Hospitality",
desc="Cooks, waiters, cleaners, decorators and setup crews in Mangalore, booked by the day. The same people we use on our own events.",
body=phero("Staff, by the day", "The people, without<br>the whole event.",
  "The same cooks, servers and decorators we use on our own functions, available on yours &mdash; "
  "whether you are running the day yourself or just short of hands.",
  [("Roles", "Kitchen &middot; service &middot; decor &middot; clearing"),
   ("Booked by", "The day"),
   ("Rates", "To follow")],
  image="manpower.jpg",
  alt="Service staff waiting along the veranda of a heritage house in the last half hour before a private dinner",
  variant="below") + f"""
<section class="section">
  <header class="section__head reveal">
    <p class="eyebrow">Who you can book</p>
    <h2>Three kinds of hands.</h2>
    <p class="section__lede">
      Take one of them or all three. Most people who call us have the house and the guest list
      already, and are short of the part that actually runs the day.
    </p>
  </header>
  <ul class="cards cards--3">
    <li class="card reveal">
      <h3>Kitchen</h3>
      <p>Cooks, and the hands that work under them. These are the same people we put on our own
      functions, so what comes out of your kitchen is what we would have served ourselves.</p>
      <p class="card__meta">By the day</p>
    </li>
    <li class="card reveal">
      <h3>Service</h3>
      <p>Waiters for the tables and cleaners for during and after. Enough of them that nobody
      queues for food and nobody ends up clearing their own plate.</p>
      <p class="card__meta">By the day</p>
    </li>
    <li class="card reveal">
      <h3>Decor and setup</h3>
      <p>The crews who put up the pandal, the lights and the flowers &mdash; and the team that
      takes all of it down again the next morning.</p>
      <p class="card__meta">By the day</p>
    </li>
  </ul>
</section>

<section class="section">
  <header class="section__head section__head--left reveal">
    <p class="eyebrow">How it works</p>
    <h2>Four steps, one phone number.</h2>
  </header>
  <ol class="steps">
    <li class="reveal"><span class="steps__n">01</span><h3>You tell us the day</h3><p>The date, what the function is, roughly how many people, and whose house or hall it is in.</p></li>
    <li class="reveal"><span class="steps__n">02</span><h3>We tell you what it needs</h3><p>How many in the kitchen, how many on the floor, how many for setup. If you already know, we will just send who you asked for.</p></li>
    <li class="reveal"><span class="steps__n">03</span><h3>They arrive briefed</h3><p>They know the house, the timings and what the day is before they get there, so you are not explaining it at the gate.</p></li>
    <li class="reveal"><span class="steps__n">04</span><h3>And they clear after</h3><p>The part everyone forgets to book. Rentals back, rubbish out, kitchen returned to how you had it.</p></li>
  </ol>
</section>

<section class="section band">
  <div class="band__in reveal">
    <p class="eyebrow eyebrow--light">Before you ask</p>
    <h2>On what it costs.</h2>
    <p class="section__lede">
      A day depends on how many people, for how long, and how far out of town the house is, so
      there is no price list to put up. Tell us the day and we will give you the number for it
      before you commit to anything.
    </p>
    <p class="cone__lines">
      <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>
      <a href="https://wa.me/{PHONE_WA}" target="_blank" rel="noopener">WhatsApp</a>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
    </p>
  </div>
</section>

{cta("Tell us what the day needs.",
     "The date, the rough count and what you are already covering yourselves. We will come back with who we would send and what it costs.",
     "Ask about staff")}
""")

# ------------------------------------------------------------------ ABOUT
PAGES["about.html"] = dict(
title="About — Shetty&rsquo;s Hospitality, Mangalore",
desc="Why Shetty's Hospitality exists, how we work, and what we promise. A single point of contact for stays, celebrations, temples and travel in Mangalore.",
body=phero("About us", "One contact for<br>the whole trip.",
  "Mangalore&rsquo;s hospitality is fragmented. Good people, working separately, with nobody joining them up. "
  "Shetty&rsquo;s Hospitality is the join.",
  [("Founded by", "Rithesh Shetty"), ("Based in", "Mangalore"), ("Model", "Aggregator and operator")],
  image="about.jpg", alt="House keys and a hand bell on a table by the door") + f"""
<section class="section split">
  <div class="split__copy reveal">
    <p class="eyebrow">The problem</p>
    <h2>Booking a trip here means four separate vendors.</h2>
    <p>
      Travellers arriving in Mangalore juggle a booking site, a driver, a cook and a temple queue,
      with no coordination between any of them. Quality changes from one to the next, planning eats
      the days before the trip, and there is no single trusted person to call when something slips.
    </p>
  </div>
  <div class="split__copy reveal">
    <p class="eyebrow">The solution</p>
    <h2>We take on the whole trip instead.</h2>
    <p>
      We handle the entire journey &mdash; the house, the cars, the temples, the table and the celebration
      &mdash; to one standard, under one plan. We onboard and manage local vendors, and we stay in the room
      for quality and for every conversation with you.
    </p>
  </div>
</section>

<section class="section band">
  <div class="band__in">
    <header class="section__head section__head--left reveal">
      <p class="eyebrow eyebrow--light">How we work</p>
      <h2>We manage the people we use.</h2>
    </header>
    <div class="incl reveal">
      <div><h4>Local network</h4><p>We onboard houses, drivers, cooks and staff in Mangalore, and keep working with the ones who hold the standard.</p></div>
      <div><h4>Our own checklists</h4><p>Standard operating procedures for arrivals, cleaning, transport and events, so the experience does not depend on who turned up.</p></div>
      <div><h4>We stay the contact</h4><p>Vendors execute. We coordinate, inspect and answer the phone. You never have to manage a chain of suppliers.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <header class="section__head reveal">
    <p class="eyebrow">How it works for you</p>
    <h2>Four steps from first call to arrival.</h2>
  </header>
  <ol class="steps">
    <li class="reveal"><span class="steps__n">01</span><h3>You call once</h3><p>Phone, WhatsApp or the enquiry form. One person picks it up and stays with you for the whole trip.</p></li>
    <li class="reveal"><span class="steps__n">02</span><h3>We ask the right questions</h3><p>Dates, how many of you, elders in the group, dietary needs, which temples matter. Ten minutes, usually.</p></li>
    <li class="reveal"><span class="steps__n">03</span><h3>You get one plan</h3><p>House, cars, temple timings, meals and experiences in a single written proposal with a single price.</p></li>
    <li class="reveal"><span class="steps__n">04</span><h3>We run it</h3><p>From the airport door to the departure gate. And we check in after, because most of our guests come back.</p></li>
  </ol>
</section>

<section class="section split">
  <div class="split__copy reveal">
    <p class="eyebrow">Who we look after</p>
    <h2>Who books with us.</h2>
    <ul class="ticks">
      <li>Families and NRIs returning to Mangalore</li>
      <li>Pilgrimage travellers</li>
      <li>Visitors exploring the coast and its culture</li>
      <li>Corporate teams needing stays and transport that just work</li>
      <li>Local families hosting something at home</li>
    </ul>
  </div>
  <div class="split__copy reveal">
    <p class="eyebrow">Where we&rsquo;re going</p>
    <h2>Mangalore first, the rest of the coast after.</h2>
    <p>
      The immediate work is depth in Mangalore: more houses, more trusted partners, tighter standards.
      After that, the same system in nearby cities &mdash; a structured vendor network is easier to
      replicate than a reputation, so we intend to earn both in that order.
    </p>
  </div>
</section>

{cta("Start with a phone call.",
     "No deposit to ask a question, and no obligation after the plan arrives.",
     "Get in touch")}
""")

# ------------------------------------------------------------------ CONTACT
PAGES["contact.html"] = dict(
title="Contact — Shetty&rsquo;s Hospitality, Mangalore",
desc="Talk to Shetty's Hospitality about a homestay, a celebration at home, temple travel or transport in Mangalore.",
body=f"""
<section class="section plan">
  <div class="plan__grid">
    <div class="plan__copy">
      <p class="eyebrow">Plan with us</p>
      <h1>Tell us the dates.<br>We&rsquo;ll take it from there.</h1>
      <p>
        Send this and we&rsquo;ll come back with a plan and a price &mdash; usually the same day.
        No deposit to ask a question.
      </p>
      <ul class="contact">
        <li><span>Phone &amp; WhatsApp</span><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
        <li><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><span>Instagram</span><a href="{INSTAGRAM}" target="_blank" rel="noopener">@shettys_hospitality</a></li>
        <li><span>Where</span><p>Mangalore, Dakshina Kannada, Karnataka</p></li>
        <li><span>Hours</span><p>Every day, 8am to 9pm IST</p></li>
      </ul>
    </div>

    <form class="form" id="planForm" novalidate>
      <div class="field">
        <label for="f-name">Your name</label>
        <input id="f-name" name="name" type="text" autocomplete="name" required />
      </div>
      <div class="field field--half">
        <label for="f-phone">Phone</label>
        <input id="f-phone" name="phone" type="tel" autocomplete="tel" required />
      </div>
      <div class="field field--half">
        <label for="f-email">Email</label>
        <input id="f-email" name="email" type="email" autocomplete="email" />
      </div>
      <div class="field field--half">
        <label for="f-what">What do you need</label>
        <select id="f-what" name="what">
          <option>A homestay</option>
          <option>A celebration at home</option>
          <option>A temple journey</option>
          <option>Cars and transfers</option>
          <option>All of it</option>
        </select>
      </div>
      <div class="field field--half">
        <label for="f-dates">Dates</label>
        <input id="f-dates" name="dates" type="text" placeholder="e.g. 12&ndash;16 Nov" />
      </div>
      <div class="field">
        <label for="f-notes">Anything we should know</label>
        <textarea id="f-notes" name="notes" rows="4" placeholder="Group size, elders travelling, temples on the list, food preferences"></textarea>
      </div>
      <button class="btn" type="submit">Send enquiry</button>
      <p class="form__note" id="formNote" role="status"></p>
    </form>
  </div>
</section>

<section class="promise">
  <p class="eyebrow eyebrow--light">Our promise</p>
  <p class="promise__words reveal"><span>Reliable.</span> <span>Coordinated.</span> <span>Complete.</span></p>
  <p class="promise__by">A vision by Rithesh Shetty</p>
</section>
""")


def build():
    for page, d in PAGES.items():
        html = head(page, d["title"], d["desc"]) + header(page) + '<main id="main">\n' + d["body"] + '</main>\n' + FOOTER
        with io.open(os.path.join(OUT, page), "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", page)


if __name__ == "__main__":
    build()
