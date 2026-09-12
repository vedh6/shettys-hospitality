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
