# -*- coding: utf-8 -*-
"""一键发布：读取「写文章.txt」，生成一篇新文章并推送上线。

用法：双击「发布.bat」，或在命令行运行  python publish.py
规则：
  - 写文章.txt 第一行是标题（留空则默认「随思」），之后是正文。
  - 正文里：回车一次 = 接着写，空一行及以上 = 新段落。
  - 每次发布会生成一篇新文章（文件名带时间戳），不会覆盖旧文。
  - 要修改旧文，直接编辑 posts/ 目录下对应的 html 文件。
"""
import datetime
import html
import os
import re
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
DRAFT = os.path.join(BASE, '写文章.txt')
INDEX = os.path.join(BASE, 'index.html')
POSTS = os.path.join(BASE, 'posts')
DEFAULT_TITLE = '随思'

ARTICLE_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script>
    (function () {
      var t = localStorage.getItem('theme');
      if (t === 'dark' || (!t && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.setAttribute('data-theme', 'dark');
      }
    })();
  </script>
  <title>{title} · 大橘的博客</title>
  <meta name="description" content="{title}">
  <link rel="stylesheet" href="../css/style.css">
</head>
<body>
  <header class="site-header">
    <div class="container header-inner">
      <a class="site-title" href="../index.html">大橘的博客</a>
      <div class="header-actions">
        <button class="theme-toggle" aria-label="切换深色/浅色主题">🌙</button>
        <button class="nav-toggle" aria-label="打开菜单" aria-expanded="false"><span></span><span></span><span></span></button>
      </div>
      <nav class="site-nav">
        <a href="../index.html">首页</a>
        <a href="../about.html">关于</a>
        <a href="../friends.html">友情链接</a>
        <a href="../contact.html">联系</a>
      </nav>
    </div>
  </header>

  <main class="container">
    <article class="post">
      <h1>{title}</h1>
      <p class="post-meta"><time datetime="{datetime}">{date}</time></p>
      <div class="post-body">{content}</div>
    </article>
  </main>

  <footer class="site-footer">
    <div class="container">
      <p>© 2026 大橘的博客 · 由 <a href="https://pages.github.com/" target="_blank" rel="noopener">GitHub Pages</a> 驱动</p>
    </div>
  </footer>

  <script src="../js/main.js"></script>
</body>
</html>
'''


def read_draft():
    with open(DRAFT, encoding='utf-8') as f:
        text = f.read()
    lines = text.split('\n')
    title = DEFAULT_TITLE
    start = 0
    for i, line in enumerate(lines):
        if line.strip():
            title = line.strip()
            start = i + 1
            break
    content = '\n'.join(lines[start:]).strip()
    return title, content


def make_filename(title, now):
    safe = re.sub(r'[\\/:*?"<>|]', '', title).strip() or DEFAULT_TITLE
    return safe + '-' + now.strftime('%Y%m%d-%H%M%S') + '.html'


def find_latest_article():
    files = [f for f in os.listdir(POSTS) if f.endswith('.html') and not f.startswith('_')]
    if not files:
        return None
    files.sort(reverse=True)
    return os.path.join(POSTS, files[0])


def extract_content(html_text):
    m = re.search(r'<div class="post-body">(.*?)</div>', html_text, re.S)
    if not m:
        return ''
    return html.unescape(m.group(1)).strip()


def update_index(title, now, filename):
    with open(INDEX, encoding='utf-8') as f:
        index_html = f.read()
    # 更新分类标题
    index_html = re.sub(r'<h2[^>]*>.*?</h2>', '<h2>' + html.escape(title) + '</h2>', index_html, count=1)
    # 在列表最前面插入新条目
    entry = ('        <li>\n'
             '          <a class="post-link" href="posts/' + filename + '">\n'
             '            <time class="post-date">' + now.strftime('%Y-%m-%d %H:%M') + '</time>\n'
             '          </a>\n'
             '        </li>\n')
    marker = '        <!-- POSTS_START -->\n'
    index_html = index_html.replace(marker, marker + entry, 1)
    with open(INDEX, 'w', encoding='utf-8') as f:
        f.write(index_html)


def run(cmd):
    subprocess.run(cmd, cwd=BASE, check=True)


def main():
    title, content = read_draft()
    if not content:
        print('「写文章.txt」里还没有正文内容。')
        sys.exit(1)
    latest = find_latest_article()
    if latest:
        with open(latest, encoding='utf-8') as f:
            latest_content = extract_content(f.read())
        if latest_content == content:
            print('内容与最新一篇相同，没有生成新文章。')
            return
    now = datetime.datetime.now()
    filename = make_filename(title, now)
    article = (ARTICLE_TEMPLATE
               .replace('{title}', html.escape(title))
               .replace('{datetime}', now.strftime('%Y-%m-%dT%H:%M'))
               .replace('{date}', now.strftime('%Y-%m-%d %H:%M'))
               .replace('{content}', html.escape(content)))
    with open(os.path.join(POSTS, filename), 'w', encoding='utf-8') as f:
        f.write(article)
    update_index(title, now, filename)
    run(['git', 'add', '-A'])
    r = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=BASE)
    if r.returncode == 0:
        print('没有新的改动，已跳过提交。')
        return
    run(['git', 'commit', '-m', '发布：' + title])
    run(['git', 'push'])
    print('已发布新文章：' + title + ' @ ' + now.strftime('%Y-%m-%d %H:%M'))


if __name__ == '__main__':
    main()
