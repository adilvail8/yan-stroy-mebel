(function () {
  'use strict';

  var WA = '77089249883';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var wa = function (text) { return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(text); };

  /* ---------- header ---------- */
  var hdr = $('#hdr');
  var nav = $('#nav');
  var burger = $('#burger');

  var hero = $('.hero');

  function stickPoint() {
    return (hero ? hero.offsetHeight : window.innerHeight) - 90;
  }

  function onScroll() {
    hdr.classList.toggle('is-stuck', window.scrollY > stickPoint());
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  var burgerLbl = $('#burgerLbl');

  function setMenu(open) {
    nav.classList.toggle('is-open', open);
    burger.classList.toggle('is-on', open);
    burger.setAttribute('aria-expanded', String(open));
    burgerLbl.textContent = open ? 'Закрыть' : 'Меню';
    hdr.classList.toggle('is-stuck', open || window.scrollY > stickPoint());
  }

  burger.addEventListener('click', function (e) {
    e.stopPropagation();
    setMenu(!nav.classList.contains('is-open'));
  });
  $$('#nav a').forEach(function (a) {
    a.addEventListener('click', function () { setMenu(false); });
  });
  document.addEventListener('click', function (e) {
    if (nav.classList.contains('is-open') && !nav.contains(e.target)) setMenu(false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.classList.contains('is-open')) { setMenu(false); burger.focus(); }
  });

  /* ---------- payment track ---------- */
  var STEPS = [
    {
      t: 'Замер',
      sum: '0 ₸',
      d: 'Замерщик приезжает по Алматы бесплатно, снимает размеры проёмов, ниш, выводов воды и электрики, фотографирует узлы. Уезжает с точными цифрами, вы не платите ничего.',
      m: 'Срок: 1 день'
    },
    {
      t: 'Проект и смета',
      sum: '0 ₸',
      d: 'Рисуем чертёж и визуализацию, подбираем материалы и фурнитуру, считаем в трёх бюджетах. Правки на этом этапе бесплатны и не ограничены по количеству.',
      m: 'Срок: 2 или 3 дня'
    },
    {
      t: 'Договор ТОО',
      sum: '0 ₸',
      d: 'Подписываем договор: состав заказа, материалы, сумма, срок, гарантия и порядок оплаты после установки. Никаких счетов на этом этапе не выставляем.',
      m: 'Срок: 1 день'
    },
    {
      t: 'Производство',
      sum: '0 ₸',
      d: 'Закупаем плиту, фасады, столешницу и фурнитуру за свой счёт. Пилим, кромим, присаживаем, собираем модули. Присылаем фото с производства по ходу работы.',
      m: 'Срок: зависит от типа фасадов'
    },
    {
      t: 'Доставка и монтаж',
      sum: '0 ₸',
      d: 'Привозим, поднимаем и собираем на месте. Подрезаем столешницу под мойку и варочную, настраиваем фасады, убираем за собой мусор.',
      m: 'Срок: от 1 до 3 дней'
    },
    {
      t: 'Приёмка и оплата',
      sum: '100%',
      d: 'Проходим вместе по чек-листу: зазоры, кромка, работа доводчиков, соответствие чертежу. Недочёты устраняем сразу. Оплата только после того, как вы всё приняли.',
      m: 'Гарантийные обязательства начинаются с этого дня'
    }
  ];

  var track = $('#track');
  var paySum = $('#paySum');
  var payTitle = $('#payTitle');
  var payText = $('#payText');
  var payMeta = $('#payMeta');
  var meterFill = $('#meterFill');

  function setStep(i) {
    var s = STEPS[i];
    if (!s) return;
    $$('.step', track).forEach(function (b) {
      var on = Number(b.dataset.step) === i;
      b.classList.toggle('is-on', on);
      b.setAttribute('aria-selected', String(on));
    });
    paySum.textContent = s.sum;
    payTitle.textContent = s.t;
    payText.textContent = s.d;
    payMeta.textContent = s.m;
    meterFill.style.width = ((i + 1) / STEPS.length * 100) + '%';
  }

  track.addEventListener('click', function (e) {
    var b = e.target.closest('.step');
    if (b) setStep(Number(b.dataset.step));
  });
  track.addEventListener('keydown', function (e) {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    var cur = $$('.step', track).findIndex(function (b) { return b.classList.contains('is-on'); });
    var next = (cur + (e.key === 'ArrowRight' ? 1 : STEPS.length - 1)) % STEPS.length;
    setStep(next);
    $$('.step', track)[next].focus();
    e.preventDefault();
  });
  setStep(0);

  /* ---------- portfolio: three tiles on phones ---------- */
  var grid = $('#grid');
  var gridMore = $('#gridMore');
  var narrow = window.matchMedia('(max-width:860px)');

  function syncGrid() {
    if (grid.dataset.expanded === '1') return;
    var clamp = narrow.matches;
    grid.classList.toggle('is-clamped', clamp);
    gridMore.hidden = !clamp;
  }
  gridMore.addEventListener('click', function () {
    grid.dataset.expanded = '1';
    grid.classList.remove('is-clamped');
    gridMore.hidden = true;
  });
  narrow.addEventListener('change', syncGrid);
  syncGrid();

  /* ---------- quiz ---------- */
  var QUESTIONS = [
    'Изделие', 'Конфигурация', 'Размер по фронту', 'Состояние помещения', 'Сроки'
  ];
  var steps = $$('.q');
  var qNum = $('#qNum');
  var qFill = $('#qFill');
  var qPrev = $('#qPrev');
  var qNext = $('#qNext');
  var qSend = $('#qSend');
  var summary = $('#summary');
  var qName = $('#qName');
  var qArea = $('#qArea');
  var cur = 0;

  function answer(i) {
    var el = $('input[name="q' + i + '"]:checked');
    return el ? el.value : '';
  }

  function render() {
    steps.forEach(function (f, i) { f.classList.toggle('is-on', i === cur); });
    qNum.textContent = String(cur + 1);
    qFill.style.width = ((cur + 1) / steps.length * 100) + '%';
    qPrev.disabled = cur === 0;

    var last = cur === steps.length - 1;
    qNext.hidden = last;
    qSend.hidden = !last;

    if (last) {
      buildSummary();
    } else {
      qNext.disabled = !answer(cur);
    }
  }

  function buildSummary() {
    summary.innerHTML = '';
    QUESTIONS.forEach(function (label, i) {
      var v = answer(i);
      if (!v) return;
      var row = document.createElement('div');
      var b = document.createElement('b');
      b.textContent = label;
      var s = document.createElement('span');
      s.textContent = v;
      row.appendChild(b);
      row.appendChild(s);
      summary.appendChild(row);
    });
    updateLink();
  }

  function updateLink() {
    var lines = ['Здравствуйте. Прошёл расчёт на сайте YanStroyMebel.'];
    QUESTIONS.forEach(function (label, i) {
      var v = answer(i);
      if (v) lines.push(label + ': ' + v);
    });
    var n = (qName.value || '').trim();
    var a = (qArea.value || '').trim();
    if (n) lines.push('Имя: ' + n);
    if (a) lines.push('Район или ЖК: ' + a);
    lines.push('Жду расчёт.');
    qSend.href = wa(lines.join('\n'));
  }

  $('#qForm').addEventListener('change', function (e) {
    if (e.target.type === 'radio') {
      qNext.disabled = false;
      if (cur < steps.length - 1) {
        window.setTimeout(function () {
          if (cur < steps.length - 1) { cur++; render(); }
        }, 260);
      }
    }
  });
  [qName, qArea].forEach(function (el) { el.addEventListener('input', updateLink); });

  qNext.addEventListener('click', function () {
    if (cur < steps.length - 1) { cur++; render(); }
  });
  qPrev.addEventListener('click', function () {
    if (cur > 0) { cur--; render(); }
  });
  render();

  /* ---------- accordion, one open at a time ---------- */
  var accItems = $$('#acc details');
  accItems.forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (!d.open) return;
      accItems.forEach(function (o) { if (o !== d) o.open = false; });
    });
  });

  /* ---------- reveal on scroll ---------- */
  var targets = $$('.sec-head, .pay__grid, .grid, .quiz__box, .dp__in, .mat__grid, .acc, .cnt__in');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -12% 0px' });
    targets.forEach(function (t) { t.classList.add('rv'); io.observe(t); });
  }
})();
