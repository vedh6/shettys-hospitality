(function () {
  'use strict';

  // Year in footer
  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();

  // Mobile menu
  var toggle = document.getElementById('navToggle');
  var drawer = document.getElementById('navDrawer');
  if (toggle && drawer) {
    toggle.addEventListener('click', function () {
      var open = drawer.hasAttribute('hidden');
      if (open) { drawer.removeAttribute('hidden'); } else { drawer.setAttribute('hidden', ''); }
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    drawer.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        drawer.setAttribute('hidden', '');
        toggle.setAttribute('aria-expanded', 'false');
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

  // The hero ships two cuts of the same footage: a wide band for desktop, where the
  // browser would crop the tall video anyway, and the full tall frame for phones.
  var vid = document.querySelector('.vhero__media');
  if (vid) {
    var portrait = vid.getAttribute('data-portrait');
    if (portrait && window.matchMedia('(max-width: 819px)').matches) {
      vid.src = portrait;
      vid.load();
    }
    // Swapping the source cancels the autoplay attribute, so ask again.
    var play = function () {
      var p = vid.play();
      if (p && p.catch) { p.catch(function () {}); }
    };
    play();
    vid.addEventListener('loadeddata', play);
    vid.addEventListener('canplay', play);
    // Hold it still for anyone who asked for less motion.
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      vid.removeAttribute('autoplay');
      vid.pause();
    }
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



  // Split testimonials. With one account this does nothing; adding a second
  // <article data-testimonial> to the markup turns on the dots, the Next
  // control, click-to-advance and the crossfade, with no further work.
  document.querySelectorAll('[data-tsplit]').forEach(function (root) {
    var items = Array.prototype.slice.call(root.querySelectorAll('[data-testimonial]'));
    var dots = root.querySelector('[data-dots]');
    if (items.length < 2 || !dots) return;

    var index = 0;
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

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
      b.addEventListener('click', function (e) { e.stopPropagation(); show(i); });
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
      show((index + 1) % items.length);
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
      show((index + 1) % items.length);
    });
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
