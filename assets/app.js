/* Rabat Music Group — interacciones */
(function () {
  var h = document.getElementById('hamb'), m = document.getElementById('menu');
  if (h && m) {
    h.addEventListener('click', function () {
      m.classList.toggle('abierto');
      h.setAttribute('aria-expanded', m.classList.contains('abierto') ? 'true' : 'false');
    });
    m.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { m.classList.remove('abierto'); });
    });
  }
  var aaa = document.getElementById('aaa');
  if (aaa) aaa.textContent = new Date().getFullYear();

  var pr = document.getElementById('progreso');
  if (pr) {
    var raf = false;
    var pintaProgreso = function () {
      var d = document.documentElement;
      var max = d.scrollHeight - d.clientHeight;
      pr.style.width = (max > 0 ? (d.scrollTop / max) * 100 : 0) + '%';
      raf = false;
    };
    window.addEventListener('scroll', function () {
      if (!raf) { raf = true; requestAnimationFrame(pintaProgreso); }
    }, { passive: true });
    pintaProgreso();
  }

  var rev = document.querySelectorAll('.rev');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('visto'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    rev.forEach(function (e) { io.observe(e); });
  } else {
    rev.forEach(function (e) { e.classList.add('visto'); });
  }

  var chips = Array.prototype.slice.call(document.querySelectorAll('.chip'));
  var fichas = Array.prototype.slice.call(document.querySelectorAll('#roster .ficha'));
  var cuenta = document.getElementById('cuenta');
  var busca = document.getElementById('busca');
  var filtro = 'todos';
  function pinta() {
    var n = 0;
    var q = busca && busca.value ? busca.value.toLowerCase().trim() : '';
    fichas.forEach(function (f) {
      var okG = filtro === 'todos' || (f.dataset.gen || '').indexOf(filtro) > -1;
      var okB = !q || (f.dataset.busca || '').indexOf(q) > -1;
      var ver = okG && okB;
      f.style.display = ver ? '' : 'none';
      if (ver) n++;
    });
    if (cuenta) cuenta.textContent = n + (n === 1 ? ' artista' : ' artistas');
  }
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      chips.forEach(function (x) { x.classList.remove('activo'); });
      c.classList.add('activo');
      filtro = c.dataset.f;
      pinta();
    });
  });
  if (busca) busca.addEventListener('input', pinta);

  var fm = document.getElementById('formulario');
  if (fm) {
    fm.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var g = function (i) { var el = document.getElementById(i); return el ? el.value.trim() : ''; };
      var asunto = g('mot') + (g('ciu') ? ' — ' + g('ciu') : '');
      var cuerpo = 'Nombre y empresa: ' + g('nom') + '\nEmail: ' + g('eml') +
        '\nCiudad y fecha: ' + g('ciu') + '\n\n' + g('msg');
      window.location.href = 'mailto:hola@rabatmusicgroup.com?subject=' +
        encodeURIComponent(asunto) + '&body=' + encodeURIComponent(cuerpo);
      var r = document.getElementById('respuesta');
      if (r) r.textContent = 'Abriendo tu programa de correo con el mensaje listo.';
    });
  }
})();
