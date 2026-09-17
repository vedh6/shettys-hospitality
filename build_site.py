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
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..800;1,9..144,300..700&family=Karla:ital,wght@0,300..700;1,300..600&display=swap" rel="stylesheet">
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
    <h2>Mangalore is not a stopover.</h2>
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
      <div class="mang__panel is-current" id="mang-coast" role="tabpanel" data-mangpanel>
        <figure class="mang__figure">
          <img src="assets/img/tannirbhavi.jpg?v={BUILD_ID}" alt="Surf and casuarinas on the sand at Tannirbhavi beach, Mangalore" fetchpriority="high" />
          <figcaption>Tannirbhavi &mdash; a ferry ride across the river, and the sand runs for miles</figcaption>
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
          <img src="assets/img/temples-wide.jpg?v={BUILD_ID}" alt="The lamp-lit stone colonnade of a coastal Karnataka temple at dawn" loading="lazy" />
          <figcaption>First light, before the queues</figcaption>
        </figure>
        <p class="mang__text">Kadri and Mangaladevi are inside the city and take an hour between them. Kateel sits on an island in the middle of the Nandini, which is worth the trip on its own. Dharmasthala, Kukke Subrahmanya and the Krishna Matha at Udupi are each a morning&rsquo;s drive, and each worth doing properly rather than in a rush. The difference between a good darshan and three hours in a queue is knowing which line to join, which seva to book ahead, and what time the doors actually close — which is most of what we do for you.</p>
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
        <p class="mang__text">The tile factories here roofed half of south India, which is why every old building from Bombay to Colombo wears the same terracotta. The Jain bastis at Moodabidri and the standing figure at Karkala are an easy half day inland. St Aloysius has a chapel painted floor to ceiling by an Italian Jesuit in the 1890s that almost nobody outside the city has heard of. And the old trade with Arabia and Portugal still shows in the street names, the doorways and the food, if somebody points it out.</p>
      </div>

      <div class="mang__nav">
        <button type="button" class="mang__arrow" data-mangprev aria-label="Previous"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5"/><path d="m11 18-6-6 6-6"/></svg></button>
        <button type="button" class="mang__arrow" data-mangnext aria-label="Next"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></svg></button>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <header class="section__head reveal">
    <p class="eyebrow">What we look after</p>
    <h2>Six services, one phone number.</h2>
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
          <li><b>Whole houses</b>, not rooms &mdash; yours for the whole stay, across the city</li>
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
        <p class="offer__lede">Naming ceremonies, birthdays, house-warmings and small weddings, hosted in your own house instead of a hall.</p>
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
        <img src="assets/img/cards/rides.jpg?v={BUILD_ID}" alt="A car and driver waiting on a Mangalore roadside" loading="lazy" />
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
        <img src="assets/img/cards/temples.jpg?v={BUILD_ID}" alt="An early morning road through coastal Karnataka on the way to a temple" loading="lazy" />
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
        <img src="assets/img/cards/hidden.jpg?v={BUILD_ID}" alt="A quiet local corner of coastal Mangalore" loading="lazy" />
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

<section class="promise">
  <p class="eyebrow eyebrow--light">Our promise</p>
  <p class="promise__words reveal"><span>Reliable.</span> <span>Coordinated.</span> <span>Complete.</span></p>
  <p class="promise__by">A vision by Rithesh Shetty</p>
</section>

<section class="wordof">
  <div class="tsplit" data-tsplit>
    <div class="tsplit__copy">

      <article class="tsplit__item is-active" data-testimonial>
        <p class="tsplit__tag"><span class="tsplit__hr" aria-hidden="true"></span>A stay</p>

        <blockquote class="tsplit__quote">
          <span class="tsplit__brk" aria-hidden="true">[</span>A family who stayed here. Their own words, printed whole.<span class="tsplit__brk" aria-hidden="true">]</span>
        </blockquote>

        <div class="tsplit__by">
          <span class="tsplit__hr" aria-hidden="true"></span>
          <div>
            <p class="tsplit__name">Name to follow</p>
            <p class="tsplit__role">Four nights, Kadri &middot; month to follow</p>
          </div>
        </div>
      </article>

      <article class="tsplit__item" data-testimonial>
        <p class="tsplit__tag"><span class="tsplit__hr" aria-hidden="true"></span>A celebration</p>

        <blockquote class="tsplit__quote">
          <span class="tsplit__brk" aria-hidden="true">[</span>Whoever hosted the evening. What they said once it was over.<span class="tsplit__brk" aria-hidden="true">]</span>
        </blockquote>

        <div class="tsplit__by">
          <span class="tsplit__hr" aria-hidden="true"></span>
          <div>
            <p class="tsplit__name">Name to follow</p>
            <p class="tsplit__role">House-warming, 60 guests &middot; month to follow</p>
          </div>
        </div>
      </article>

      <article class="tsplit__item" data-testimonial>
        <p class="tsplit__tag"><span class="tsplit__hr" aria-hidden="true"></span>A temple journey</p>

        <blockquote class="tsplit__quote">
          <span class="tsplit__brk" aria-hidden="true">[</span>The people who travelled. Unedited, as they sent it.<span class="tsplit__brk" aria-hidden="true">]</span>
        </blockquote>

        <div class="tsplit__by">
          <span class="tsplit__hr" aria-hidden="true"></span>
          <div>
            <p class="tsplit__name">Name to follow</p>
            <p class="tsplit__role">Dharmasthala and Kukke &middot; month to follow</p>
          </div>
        </div>
      </article>

      <article class="tsplit__item" data-testimonial>
        <p class="tsplit__tag"><span class="tsplit__hr" aria-hidden="true"></span>A homecoming</p>

        <blockquote class="tsplit__quote">
          <span class="tsplit__brk" aria-hidden="true">[</span>A family back for the season. Their account of the month.<span class="tsplit__brk" aria-hidden="true">]</span>
        </blockquote>

        <div class="tsplit__by">
          <span class="tsplit__hr" aria-hidden="true"></span>
          <div>
            <p class="tsplit__name">Name to follow</p>
            <p class="tsplit__role">Two weeks, whole house &middot; month to follow</p>
          </div>
        </div>
      </article>

      <p class="tsplit__note">
        Guests send these after they get home. We ask before printing one, we print it whole, and
        we set out what was actually arranged beside it.
        <a class="link" href="contact.html">Stayed with us? Send us yours <span aria-hidden="true">&rarr;</span></a>
      </p>

      <div class="tsplit__dots" data-dots hidden></div>
    </div>

    <div class="tsplit__visual">
    <figure class="vplayer" data-vplayer style="--poster:url(assets/img/review-poster.jpg?v={BUILD_ID})">
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
    <h2>Nobody wants four vendors on speaker.</h2>
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
body=phero("Shetty&rsquo;s Stays", "Homes, not room numbers.",
  "Every house on our list is one we manage. We know which geyser is slow, which room catches the "
  "afternoon sun, and how long the drive to the airport really takes at 6am.",
  [("Stay length", "One night to several months"), ("Group size", "2 to 20 guests"), ("Ready", "Cleaned before every arrival")],
  image="stays.jpg", alt="A bedroom in one of our managed homes", variant="below") + f"""
<section class="section">
  <header class="section__head section__head--left reveal">
    <p class="eyebrow">The houses</p>
    <h2>Where you would actually stay.</h2>
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
    <h2>The list we check before you arrive.</h2>
  </header>

  <div class="bento reveal">
    <div class="bento__cell bento__cell--hero">
      <h3>Cleaned and inspected before every arrival</h3>
      <p>Room by room, against the same written checklist every time &mdash; by someone who has
      been in the house before.</p>
    </div>

    <figure class="bento__cell bento__cell--img">
      <img src="assets/img/pages/stays.jpg?v={BUILD_ID}" alt="A bedroom in one of our managed homes" loading="lazy" />
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
        <p class="eyebrow eyebrow--light">New line of work</p>
        <h2>Lately we have started building the rooms, not only filling them.</h2>
        <p class="section__lede">
          Cone houses &mdash; triangular A-frame cabins, framed and finished from scratch on
          site. We build them for other people&rsquo;s land: layouts, resorts and estates that
          want rooms up without putting up a block.
        </p>
        <ul class="ticks ticks--light">
          <li>Designed, framed and finished by our own team</li>
          <li>Built on your site, in your layout or resort</li>
          <li>Sizes, timeline and what a unit costs &mdash; to follow</li>
        </ul>
        <a class="link link--light" href="contact.html">Ask about a build <span aria-hidden="true">&rarr;</span></a>
      </div>
      <figure class="cone__media reveal">
        <img src="assets/img/cone-houses.jpg?v={BUILD_ID}"
             alt="A-frame cone house cabins in a palm clearing" loading="lazy" />
      </figure>
    </div>
  </div>
</section>

<section class="section">
  <header class="section__head reveal">
    <p class="eyebrow">Kinds of stay</p>
    <h2>Pick the one that sounds like your trip.</h2>
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
    <h2>Things people ask for, and get.</h2>
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
desc="Naming ceremonies, house-warmings, birthdays and intimate weddings hosted at home in Mangalore. Kitchen, decor, staff and clean-up handled.",
body=phero("Celebrations at home", "The house fills up.<br>You get to enjoy it.",
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
      <h2>A first birthday is not a small wedding.</h2>
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
      <h2>A week is not a long evening.</h2>
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
      <h2>A house that behaves like a venue.</h2>
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
    <h2>What we usually get called for.</h2>
  </header>
  <ul class="occasions occasions--light reveal">
    <li>
      <span>Naming &amp; cradle ceremonies</span>
      <p>Morning functions that start early and fill the house with elders and small children.
      We plan for both: chairs with backs, shade where people wait, and a menu that leans sweet
      and is ready when the ceremony ends rather than an hour after.</p>
    </li>
    <li>
      <span>House-warming</span>
      <p>Griha pravesha at whatever hour the priest gives you, which is often before light.
      We handle what the pooja needs, keep the kitchen running from dawn, and turn the house
      around for a full lunch once the ritual is done.</p>
    </li>
    <li>
      <span>Birthdays &amp; anniversaries</span>
      <p>Evening parties, usually smaller. A first birthday and a sixtieth need very different
      rooms, so we scale the seating, the sound and the food to the actual guest list instead of
      a package.</p>
    </li>
    <li>
      <span>Intimate weddings &amp; roce</span>
      <p>Roce, mehendi, haldi and small weddings held at home rather than in a hall. These run
      across days and involve family doing things themselves, so we work around the household
      instead of taking it over.</p>
    </li>
    <li>
      <span>Family reunions &amp; NRI homecomings</span>
      <p>Several families under one roof for a week, with different diets, different sleep
      schedules and a lot of catching up. Meals stay flexible, the kitchen keeps going, and
      nobody is cooking for twenty on their holiday.</p>
    </li>
    <li>
      <span>Corporate offsites &amp; dinners</span>
      <p>Team dinners and small offsites in a house instead of a banquet room. Fixed timings,
      a quiet setup that stays out of the way, and a single invoice at the end for your
      accounts team.</p>
    </li>
  </ul>
</section>

<section class="section band">
  <div class="band__in">
    <header class="section__head section__head--left reveal">
      <p class="eyebrow eyebrow--light">What we bring</p>
      <h2>Three parts, all of them ours to worry about.</h2>
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
    <h2>You have one person to look for.</h2>
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
body=phero("Journeys", "Everything that happens<br>outside the house.",
  "Temples, transport and the parts of Mangalore that never make it onto a list. Booked as one plan, "
  "with one person answering the phone.",
  [("Temples", "Dharmasthala &middot; Kukke &middot; Udupi"), ("Cars", "Fixed fares, verified drivers"), ("Local", "Half-day walks with a host")],
  image="journeys.jpg", alt="Stone steps up to a coastal Karnataka temple at first light", variant="mirror") + f"""
<section class="section" id="temples">
  <header class="section__head reveal">
    <p class="eyebrow">Temple &amp; spiritual travel</p>
    <h2>Darshan, without the guesswork.</h2>
    <p class="section__lede">
      The drive is the easy part. Knowing which queue to join, when the doors close, which seva to book
      ahead and where elders can sit down &mdash; that is what we handle.
    </p>
  </header>
  <ul class="cards cards--3">
    <li class="card reveal"><h3>Dharmasthala</h3><p>Day trip or overnight, with darshan timings, annadana and the drive up through Charmadi country.</p><p class="card__meta">2.5 hrs from Mangalore</p></li>
    <li class="card reveal"><h3>Kukke Subrahmanya</h3><p>Sarpa samskara and other sevas booked ahead, with an early start so you are back before dark.</p><p class="card__meta">3 hrs from Mangalore</p></li>
    <li class="card reveal"><h3>Udupi Krishna Matha</h3><p>Paryaya-season crowds handled, plus Malpe and the Ananthapadmanabha temple if the day allows.</p><p class="card__meta">1.5 hrs from Mangalore</p></li>
    <li class="card reveal"><h3>Kateel Durgaparameshwari</h3><p>A short morning run to the river temple, easy to pair with the airport on arrival day.</p><p class="card__meta">45 min from the city</p></li>
    <li class="card reveal"><h3>Kadri Manjunatha</h3><p>In the city itself &mdash; a good first stop the morning after you land.</p><p class="card__meta">In Mangalore</p></li>
    <li class="card card--ask reveal"><h3>A circuit</h3><p>Three or four temples over two days, sequenced so the driving works and the elders are not exhausted.</p><p class="card__meta"><a class="link" href="contact.html">Plan a circuit <span aria-hidden="true">&rarr;</span></a></p></li>
  </ul>
</section>

<section class="section band" id="rides">
  <div class="band__in">
    <header class="section__head section__head--left reveal">
      <p class="eyebrow eyebrow--light">Shetty&rsquo;s Rides</p>
      <h2>The fare is agreed before you get in.</h2>
      <p class="section__lede">
        Drivers we know by name, cars we have sat in, and no surprise at the end of the day.
      </p>
    </header>
    <div class="incl reveal">
      <div>
        <h4>Airport transfers</h4>
        <p>Mangalore International, at any hour. The driver&rsquo;s name, number and vehicle
        reach you the night before, so nobody is scanning a crowd at three in the morning.
        We watch the flight rather than the clock &mdash; if you land two hours late, the car
        is still there and the fare is still the one we quoted.</p>
      </div>
      <div>
        <h4>Day cars</h4>
        <p>A car and driver for a half day or a full day, in the city or well outside it.
        Sedans for two or three, SUVs for a family with luggage, tempo travellers for a group
        travelling together. The driver stays with you between stops, so there is no rebooking
        after lunch and no waiting at a temple gate for something to turn up.</p>
      </div>
      <div>
        <h4>Outstation</h4>
        <p>Udupi, Coorg, Chikmagalur, Kasaragod and the routes in between, priced per trip
        rather than per kilometre. Tolls, parking and the driver&rsquo;s allowance are inside the
        number we give you, and on overnight runs so is his stay. The figure you agree at the
        start is the figure at the end.</p>
      </div>
    </div>
  </div>
</section>

<section class="section" id="hidden">
  <header class="section__head reveal">
    <p class="eyebrow">Hidden Mangalore</p>
    <h2>The half day you didn&rsquo;t know to ask for.</h2>
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

{cta("One trip, one plan.",
     "Tell us who&rsquo;s travelling and what matters most. We&rsquo;ll sequence the temples, the cars and the free afternoons.",
     "Plan a journey")}
""")

# ------------------------------------------------------------------ ABOUT
PAGES["about.html"] = dict(
title="About — Shetty&rsquo;s Hospitality, Mangalore",
desc="Why Shetty's Hospitality exists, how we work, and what we promise. A single point of contact for stays, celebrations, temples and travel in Mangalore.",
body=phero("About us", "One contact.<br>Complete hospitality.",
  "Mangalore&rsquo;s hospitality is fragmented. Good people, working separately, with nobody joining them up. "
  "Shetty&rsquo;s Hospitality is the join.",
  [("Founded by", "Rithesh Shetty"), ("Based in", "Mangalore"), ("Model", "Aggregator and operator")],
  image="about.jpg", alt="House keys and a hand bell on a table by the door") + f"""
<section class="section split">
  <div class="split__copy reveal">
    <p class="eyebrow">The problem</p>
    <h2>Four vendors, four standards, one exhausted guest.</h2>
    <p>
      Travellers arriving in Mangalore juggle a booking site, a driver, a cook and a temple queue,
      with no coordination between any of them. Quality changes from one to the next, planning eats
      the days before the trip, and there is no single trusted person to call when something slips.
    </p>
  </div>
  <div class="split__copy reveal">
    <p class="eyebrow">The solution</p>
    <h2>Someone whose job is the whole trip.</h2>
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
      <h2>Aggregator on the supply side. Operator on yours.</h2>
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
    <h2>Four steps, and then it&rsquo;s handled.</h2>
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
    <h2>Mostly people coming home.</h2>
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
    <h2>Deeper here first, then outward.</h2>
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
