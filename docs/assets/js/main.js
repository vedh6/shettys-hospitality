(function () {
  'use strict';

  // Year in footer
  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();

  // Mobile menu
  var toggle = document.getElementById('navToggle');
  var drawer = document.getElementById('navDrawer');
  if (toggle && drawer) {
    var nav = toggle.closest('.nav');
    // The home nav is transparent over the hero video, so an open drawer
    // there would be white links on moving footage. is-open gives it a
    // solid ground for as long as it is open, whatever the page or scroll.
    var setOpen = function (open) {
      if (open) { drawer.removeAttribute('hidden'); } else { drawer.setAttribute('hidden', ''); }
      if (nav) { nav.classList.toggle('is-open', open); }
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    };

    toggle.addEventListener('click', function () {
      setOpen(drawer.hasAttribute('hidden'));
    });
    drawer.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { setOpen(false); }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !drawer.hasAttribute('hidden')) {
        setOpen(false);
        toggle.focus();
      }
    });
  }


  // Home nav: transparent over the video, solid once you're past it.
  var navEl = document.querySelector('.nav');
  if (navEl && document.body.classList.contains('home')) {
    var hero = document.querySelector('.vhero');
    var mark = function () {
      var limit = hero ? hero.offsetHeight * 0.7 : 200;
      navEl.classList.toggle('is-solid', window.scrollY > limit);
    };
    mark();
    window.addEventListener('scroll', mark, { passive: true });
    window.addEventListener('resize', mark);
  }

  // Hero still. The placeholder behind it (.vhero::before) paints first, so
  // fade the real image in over it rather than letting it pop.
  var vid = document.querySelector('.vhero__media');
  if (vid) {
    var ready = function () { vid.classList.add('is-ready'); };
    if (vid.complete && vid.naturalWidth) { ready(); }
    vid.addEventListener('load', ready);
    vid.addEventListener('error', ready);
  }

  // Scroll reveal — nothing below the fold is on screen until you reach it.
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var items = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window) || reduced) {
    items.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry, i) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        setTimeout(function () { el.classList.add('is-in'); }, i * 90);
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -18% 0px', threshold: 0.05 });
    items.forEach(function (el) { io.observe(el); });
  }

  // Hand-off from the hero: its copy lifts and fades out as you scroll past it.
  var heroEl = document.querySelector('.vhero');
  var heroCopy = document.querySelector('.vhero__in');
  if (heroEl && heroCopy && !reduced) {
    var ticking = false;
    var drift = function () {
      var p = Math.min(1, window.scrollY / (heroEl.offsetHeight * 0.72));
      heroCopy.style.opacity = String(1 - p);
      heroCopy.style.transform = 'translate3d(0,' + (p * -70).toFixed(1) + 'px,0)';
      ticking = false;
    };
    drift();
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(drift);
    }, { passive: true });
  }



  // Shared auto-advance timer for the rotating panels. Held while the pointer
  // is over the panel, while anything inside has keyboard focus, while a video
  // inside is playing, and while the panel is off screen or the tab is in the
  // background. Returns restart(), to call after any manual advance.
  function autoRotate(root, advance, everyMs, video) {
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var timer = null, hovering = false, focused = false, onScreen = false;

    function canRun() {
      return !reduced && onScreen && !hovering && !focused &&
             !document.hidden && !(video && !video.paused);
    }
    function restart() {
      if (timer) clearInterval(timer);
      if (reduced) { timer = null; return; }
      var ms = typeof everyMs === 'function' ? everyMs() : everyMs;
      timer = setInterval(function () {
        if (canRun()) advance();
      }, ms);
    }

    root.addEventListener('mouseenter', function () { hovering = true; });
    root.addEventListener('mouseleave', function () { hovering = false; });
    root.addEventListener('focusin', function () { focused = true; });
    root.addEventListener('focusout', function () { focused = false; });
    document.addEventListener('visibilitychange', restart);
    if (video) {
      video.addEventListener('play', restart);
      video.addEventListener('pause', restart);
    }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        var was = onScreen;
        onScreen = entries[0].isIntersecting;
        // Restart on entry so the first slide a reader sees gets a full
        // interval, rather than inheriting whatever is left of a tick that
        // was skipped while the panel was off screen.
        if (onScreen && !was) restart();
      }, { threshold: 0.25 }).observe(root);
    } else {
      onScreen = true;
    }

    restart();
    return restart;
  }

  // Split testimonials. With one account this does nothing; adding a second
  // <article data-testimonial> to the markup turns on the dots, the Next
  // control, click-to-advance and the crossfade, with no further work.
  document.querySelectorAll('[data-tsplit]').forEach(function (root) {
    var items = Array.prototype.slice.call(root.querySelectorAll('[data-testimonial]'));
    var dots = root.querySelector('[data-dots]');
    if (items.length < 2 || !dots) return;

    var index = 0;
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var advance = function () { show((index + 1) % items.length); };

    items.forEach(function (el, i) { if (i !== 0) el.hidden = true; });

    var show = function (next) {
      if (next === index) return;
      var from = items[index], to = items[next];
      index = next;
      paintDots();

      if (reduced) { from.hidden = true; to.hidden = false; return; }

      from.classList.add('is-leaving');
      setTimeout(function () {
        from.hidden = true;
        from.classList.remove('is-leaving');
        to.hidden = false;
        to.classList.add('is-entering');
        requestAnimationFrame(function () {
          requestAnimationFrame(function () { to.classList.remove('is-entering'); });
        });
      }, 260);
    };

    var buttons = items.map(function (_, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('aria-label', 'Show account ' + (i + 1) + ' of ' + items.length);
      b.addEventListener('click', function (e) { e.stopPropagation(); show(i); restart(); });
      dots.appendChild(b);
      return b;
    });

    var next = document.createElement('button');
    next.type = 'button';
    next.className = 'tsplit__next';
    next.innerHTML = 'Next <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
      'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<path d="M7 7h10v10"/><path d="M7 17 17 7"/></svg>';
    next.addEventListener('click', function (e) {
      e.stopPropagation();
      advance();
      restart();
    });
    dots.appendChild(next);

    function paintDots() {
      buttons.forEach(function (b, i) {
        b.setAttribute('aria-current', i === index ? 'true' : 'false');
      });
    }
    paintDots();
    dots.hidden = false;

    // Clicking the panel advances, except on the player and on real links.
    root.addEventListener('click', function (e) {
      if (e.target.closest('.tsplit__visual, a, button')) return;
      advance();
    });

    // Auto-advance every 4s, paused by the shared rules in autoRotate.
    var restart = autoRotate(root, advance, 4000,
                             root.querySelector('.tsplit__visual video'));
  });

  // Rotating occasions on Celebrations. Each slide carries its own copy and
  // its own photograph, so the two always cross-fade together. Slides stay in
  // flow (see .occ__slide) so the section height never jumps.
  document.querySelectorAll('[data-occ]').forEach(function (root) {
    var slides = Array.prototype.slice.call(root.querySelectorAll('[data-occasion]'));
    var dots = root.querySelector('[data-occ-dots]');
    if (slides.length < 2 || !dots) return;

    var index = 0;
    function show(next) {
      if (next === index) return;
      slides[index].classList.remove('is-current');
      index = next;
      slides[index].classList.add('is-current');
      paint();
    }
    var advance = function () { show((index + 1) % slides.length); };

    var buttons = slides.map(function (el, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('aria-label', el.getAttribute('aria-label') || ('Slide ' + (i + 1)));
      b.addEventListener('click', function () { show(i); restart(); });
      dots.appendChild(b);
      return b;
    });

    function paint() {
      buttons.forEach(function (b, i) {
        b.setAttribute('aria-current', i === index ? 'true' : 'false');
      });
      slides.forEach(function (el, i) {
        el.setAttribute('aria-hidden', i === index ? 'false' : 'true');
      });
    }
    paint();
    dots.hidden = false;

    // 4s on a phone, 5s on a laptop — the site owner's call. Re-armed on
    // breakpoint change so a rotate or a resize picks up the other timing.
    var phone = window.matchMedia('(max-width: 860px)');
    var restart = autoRotate(root, advance, function () {
      return phone.matches ? 4000 : 5000;
    }, null);
    if (phone.addEventListener) phone.addEventListener('change', restart);
  });

  // Mangalore tabs. The photograph and the paragraph belong to the same panel,
  // so one click swaps both. No auto-rotation here: the reader is choosing.
  document.querySelectorAll('[data-mang]').forEach(function (root) {
    var tabs = Array.prototype.slice.call(root.querySelectorAll('[data-mangtab]'));
    var panels = Array.prototype.slice.call(root.querySelectorAll('[data-mangpanel]'));
    if (tabs.length !== panels.length || !tabs.length) return;

    var index = 0;
    // A dot per panel, mirroring the tabs. Same job, but sitting next to the
    // picture where the eye already is.
    var dotWrap = root.querySelector('[data-mangdots]');
    var dots = [];
    if (dotWrap) {
      dots = panels.map(function (p, i) {
        var b = document.createElement('button');
        b.type = 'button';
        b.setAttribute('role', 'tab');
        b.setAttribute('aria-label', tabs[i].textContent.trim());
        b.addEventListener('click', function () { slowDown(); firstDone = true; show(i); restart(); });
        dotWrap.appendChild(b);
        return b;
      });
    }

    function show(next) {
      index = next;
      tabs.forEach(function (t, i) {
        t.setAttribute('aria-selected', i === next ? 'true' : 'false');
        t.tabIndex = i === next ? 0 : -1;
      });
      dots.forEach(function (d, i) {
        d.setAttribute('aria-selected', i === next ? 'true' : 'false');
      });
      panels.forEach(function (p, i) {
        p.classList.toggle('is-current', i === next);
        p.setAttribute('aria-hidden', i === next ? 'false' : 'true');
      });
    }
    show(0);

    var advance = function () { show((index + 1) % tabs.length); };

    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { show(i); restart(); });
      // Left/right arrows move between tabs, which is what a tablist should do.
      t.addEventListener('keydown', function (e) {
        var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        var n = (i + d + tabs.length) % tabs.length;
        show(n);
        tabs[n].focus();
        restart();
      });
    });

    // Cycles every 4s. autoRotate holds it while the pointer is over the
    // section or anything inside has focus, which matters more here than on
    // the other panels: these paragraphs take far longer than 4s to read, so
    // hovering is what lets you actually finish one.
    // Three paces. The first change after the section comes into view is 3.5s -
    // long enough to take the opening picture in, short enough to show there is
    // more than one. Everything after that is 4s, including the wrap back round
    // to the first tab. Reaching for an arrow or a dot is a sign of actually
    // reading, so that drops it to 5.5s for the rest of the visit.
    var FIRST = 3500, BASE = 4000, SLOW = 5500;
    var everyMs = FIRST;
    var firstDone = false, slowed = false;

    function slowDown() { slowed = true; everyMs = SLOW; }

    // Wraps advance() so the one-off 3.5s is spent and the timer re-armed at 4s.
    function pacedAdvance() {
      advance();
      if (!firstDone) {
        firstDone = true;
        if (!slowed) { everyMs = BASE; restart(); }
      }
    }

    var prev = root.querySelector('[data-mangprev]');
    var next = root.querySelector('[data-mangnext]');
    if (prev) prev.addEventListener('click', function () {
      slowDown();
      firstDone = true;
      show((index - 1 + tabs.length) % tabs.length);
      restart();
    });
    if (next) next.addEventListener('click', function () {
      slowDown();
      firstDone = true;
      advance();
      restart();
    });

    // autoRotate re-reads this on every restart, so the slower pace takes hold
    // from the press onward. It also holds while the pointer is over the
    // section or anything inside has focus.
    var restart = autoRotate(root, pacedAdvance, function () { return everyMs; }, null);
  });

  // Video player. Custom controls so the review sits in the site's own language
  // rather than the browser's: centre play button, seek, skip, volume,
  // fullscreen, auto-hiding bar, and keyboard shortcuts while focused.
  document.querySelectorAll('[data-vplayer]').forEach(function (root) {
    var video = root.querySelector('video');
    if (!video) return;

    var seek = root.querySelector('.vplayer__seek');
    var vol = root.querySelector('.vplayer__volume');
    var curEl = root.querySelector('[data-current]');
    var durEl = root.querySelector('[data-duration]');
    var idleTimer = null;

    root.tabIndex = 0;

    var fmt = function (t) {
      if (!isFinite(t)) return '0:00';
      var m = Math.floor(t / 60), sec = Math.floor(t % 60);
      return m + ':' + String(sec).padStart(2, '0');
    };

    var paintRange = function (el, pct) {
      el.style.background =
        'linear-gradient(to right, var(--paper) 0%, var(--paper) ' + pct + '%,' +
        ' rgba(245,242,234,.3) ' + pct + '%, rgba(245,242,234,.3) 100%)';
    };

    var wake = function () {
      root.classList.remove('is-idle');
      if (idleTimer) clearTimeout(idleTimer);
      if (!video.paused) {
        idleTimer = setTimeout(function () { root.classList.add('is-idle'); }, 2600);
      }
    };

    var toggle = function () { video.paused ? video.play() : video.pause(); };
    var skipBy = function (n) {
      video.currentTime = Math.max(0, Math.min(video.duration || 0, video.currentTime + n));
    };

    root.querySelectorAll('[data-play]').forEach(function (b) {
      b.addEventListener('click', function (e) { e.stopPropagation(); toggle(); });
    });
    root.querySelectorAll('[data-skip]').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation();
        skipBy(parseFloat(b.getAttribute('data-skip')));
      });
    });
    root.querySelector('[data-mute]').addEventListener('click', function (e) {
      e.stopPropagation();
      video.muted = !video.muted;
    });
    root.querySelector('[data-fullscreen]').addEventListener('click', function (e) {
      e.stopPropagation();
      if (document.fullscreenElement) {
        document.exitFullscreen();
      } else if (root.requestFullscreen) {
        root.requestFullscreen();
      } else if (video.webkitEnterFullscreen) {
        video.webkitEnterFullscreen();   // iPhone Safari only allows the video itself
      }
    });

    video.addEventListener('click', toggle);
    video.addEventListener('loadedmetadata', function () {
      seek.max = String(video.duration || 0);
      durEl.textContent = fmt(video.duration);
    });
    video.addEventListener('timeupdate', function () {
      if (seek.matches(':active')) return;
      seek.value = String(video.currentTime);
      curEl.textContent = fmt(video.currentTime);
      paintRange(seek, video.duration ? (video.currentTime / video.duration) * 100 : 0);
    });
    video.addEventListener('play', function () { root.classList.add('is-playing'); wake(); });
    video.addEventListener('pause', function () {
      root.classList.remove('is-playing', 'is-idle');
      if (idleTimer) clearTimeout(idleTimer);
    });
    video.addEventListener('ended', function () { root.classList.remove('is-playing', 'is-idle'); });
    video.addEventListener('volumechange', function () {
      root.classList.toggle('is-muted', video.muted || video.volume === 0);
      vol.value = String(video.muted ? 0 : video.volume);
      paintRange(vol, (video.muted ? 0 : video.volume) * 100);
    });

    seek.addEventListener('input', function () {
      video.currentTime = parseFloat(seek.value);
      curEl.textContent = fmt(video.currentTime);
      paintRange(seek, video.duration ? (video.currentTime / video.duration) * 100 : 0);
    });
    vol.addEventListener('input', function () {
      video.volume = parseFloat(vol.value);
      video.muted = video.volume === 0;
    });

    root.addEventListener('mousemove', wake);
    root.addEventListener('mouseleave', function () {
      if (!video.paused) root.classList.add('is-idle');
    });

    document.addEventListener('fullscreenchange', function () {
      root.classList.toggle('is-full', document.fullscreenElement === root);
    });

    root.addEventListener('keydown', function (e) {
      var k = e.key;
      if (k === ' ' || k === 'k') { e.preventDefault(); toggle(); }
      else if (k === 'm') { e.preventDefault(); video.muted = !video.muted; }
      else if (k === 'f') { e.preventDefault(); root.querySelector('[data-fullscreen]').click(); }
      else if (k === 'ArrowLeft') { e.preventDefault(); skipBy(-10); }
      else if (k === 'ArrowRight') { e.preventDefault(); skipBy(10); }
      else if (k === 'ArrowUp') { e.preventDefault(); video.muted = false; video.volume = Math.min(1, video.volume + 0.1); }
      else if (k === 'ArrowDown') { e.preventDefault(); video.volume = Math.max(0, video.volume - 0.1); }
      else return;
      wake();
    });

    paintRange(seek, 0);
    paintRange(vol, 100);
  });

  // Enquiry form — no backend yet, so hand the message to WhatsApp/email.
  var form = document.getElementById('planForm');
  var note = document.getElementById('formNote');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = new FormData(form);
      var name = (d.get('name') || '').toString().trim();
      var phone = (d.get('phone') || '').toString().trim();
      if (!name || !phone) {
        note.textContent = 'Add your name and a phone number so we can reply.';
        return;
      }
      var lines = [
        'Enquiry from the website',
        'Name: ' + name,
        'Phone: ' + phone,
        'Email: ' + (d.get('email') || '—'),
        'Needs: ' + (d.get('what') || '—'),
        'Dates: ' + (d.get('dates') || '—'),
        'Notes: ' + (d.get('notes') || '—')
      ];
      var url = 'https://wa.me/917676643606?text=' + encodeURIComponent(lines.join('\n'));
      window.open(url, '_blank', 'noopener');
      note.textContent = 'Opening WhatsApp with your details. If nothing happens, email info@shettyshospitality.com.';
    });
  }
})();
