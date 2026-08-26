# -*- coding: utf-8 -*-
"""提交「其他改动」：自动清理失效的文章链接，然后提交并推送。

用法：双击「其他改动.bat」。
说明：
  - 如果你在 posts/ 目录里删除了某篇文章文件，本脚本会从首页移除对应的失效链接。
  - 然后统一提交所有改动（改关于页、样式、删文章等）并推送。
"""
import os
import re
import subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(BASE, 'index.html')


def remove_stale_links():
    with open(INDEX, encoding='utf-8') as f:
        index_html = f.read()
    m = re.search(r'<!-- POSTS_START -->(.*?)<!-- POSTS_END -->', index_html, re.S)
    if not m:
        return 0
    region = m.group(1)
    new_region = region
    removed = 0
    for li in re.findall(r'\n[ \t]*<li>.*?</li>', region, re.S):
        href_m = re.search(r'href="([^"]+)"', li)
        if not href_m:
            continue
        href = href_m.group(1)
        path = os.path.normpath(os.path.join(BASE, href))
        if not os.path.exists(path):
            new_region = new_region.replace(li, '')
            removed += 1
    if removed:
        index_html = index_html.replace(region, new_region)
        with open(INDEX, 'w', encoding='utf-8') as f:
            f.write(index_html)
    return removed


def run(cmd):
    subprocess.run(cmd, cwd=BASE, check=True)


def main():
    removed = remove_stale_links()
    if removed:
        print('已移除 %d 个失效链接。' % removed)
    run(['git', 'add', '-A'])
    r = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=BASE)
    if r.returncode == 0:
        print('没有改动，无需提交。')
        return
    run(['git', 'commit', '-m', 'update other changes'])
    run(['git', 'push'])
    print('已提交并推送。')


if __name__ == '__main__':
    main()
