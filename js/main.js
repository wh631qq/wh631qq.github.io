// 移动端导航菜单
(function () {
  var navToggle = document.querySelector('.nav-toggle');
  var siteNav = document.querySelector('.site-nav');
  if (!navToggle || !siteNav) return;

  navToggle.addEventListener('click', function () {
    var open = siteNav.classList.toggle('open');
    navToggle.classList.toggle('open', open);
    navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
})();

// 深色 / 浅色主题切换
(function () {
  var toggle = document.querySelector('.theme-toggle');
  if (!toggle) return;

  function applyIcon() {
    var dark = document.documentElement.getAttribute('data-theme') === 'dark';
    toggle.textContent = dark ? '☀️' : '🌙';
  }

  toggle.addEventListener('click', function () {
    var dark = document.documentElement.getAttribute('data-theme') === 'dark';
    var next = dark ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try {
      localStorage.setItem('theme', next);
    } catch (e) {
      /* 忽略存储失败 */
    }
    applyIcon();
  });

  applyIcon();
})();

// 文章正文换行规则：回车一次 = 接着写，空一行及以上 = 新段落
(function () {
  var bodies = document.querySelectorAll('.post-body');
  bodies.forEach(function (body) {
    var text = body.textContent
      .replace(/\r\n/g, '\n')
      .replace(/[ \t]+\n/g, '\n')
      .replace(/\n[ \t]+/g, '\n')
      .trim();
    var html = text.split(/\n{2,}/).map(function (p) {
      return '<p>' + p.replace(/\n/g, '') + '</p>';
    }).join('');
    body.innerHTML = html;
  });
})();
