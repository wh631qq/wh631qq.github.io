# 大橘的博客

一个纯中文的静态个人博客，零依赖、零成本，托管在 GitHub Pages 上。

## 目录结构

```
site/
├── index.html         首页（文章列表）
├── about.html         关于
├── friends.html       友情链接
├── contact.html       联系（留言表单）
├── thanks.html        留言成功后的页面
├── 发布.bat           双击即可推送上线
├── css/style.css      全部样式
├── js/main.js         菜单 / 主题切换
└── posts/
    ├── _template.html  文章模板（复制它来写新文章）
    └── 随思.html      你的文章
```

## 本地预览

最简单的方式：直接双击 `index.html`，用浏览器打开即可。

如果页面里的主题切换、菜单等交互看起来没反应，多半是浏览器限制了本地 JS，可以起一个本地服务：

```powershell
python -m http.server 8000
```

然后浏览器访问 http://localhost:8000 。

## 如何修改站点名

把下面几处文字里的「大橘的博客」替换成你想要的名字：

- 每个 `.html` 文件的 `<title>` 标签
- 头部左上角的 `<a class="site-title">大橘的博客</a>`
- 每个页面页脚的版权文字

## 如何发布文章（一键）

现在的流程非常简单：**只写内容，双击发布即可**。

1. 用文本编辑器打开根目录的 `写文章.txt`：
   - **第一行**是标题（留空则默认「随思」）
   - 之后是正文
2. 正文直接写字即可，换行规则：
   - **回车一次** = 接着写（不分行）
   - **空一行** = 新段落
3. 双击根目录的 `发布.bat`，它会自动生成文章（标题 + 当前时间）、更新首页、提交并推送到 GitHub。

一两分钟后网站就更新了。

> 想改标题，就改 `写文章.txt` 的第一行；发布时间不用管，发布时自动用当前时间。

## 如何配置联系表单

联系表单用的是 [FormSubmit](https://formsubmit.co/)（免费，无需注册）。你只需要做一件事：

1. 打开 `contact.html`；
2. 把 `action="https://formsubmit.co/yourname@example.com"` 里的 `yourname@example.com` 换成你自己的邮箱；
3. 顺带把页面里 `mailto:` 后面的邮箱也一起换了。

第一次有人提交留言后，FormSubmit 会往这个邮箱发一封确认邮件，点一下激活即可。之后留言就会直接发到你的邮箱。

## 如何添加友情链接

打开 `friends.html`，在 `<ul class="friend-list">` 里新增一条：

```html
<li class="friend-item">
  <a href="https://对方的网址" target="_blank" rel="noopener">
    <span class="friend-name">对方的名字</span>
    <span class="friend-desc">一句话介绍</span>
  </a>
</li>
```

## 如何部署到 GitHub Pages

网站是纯静态文件，部署只需要：装 git → 建仓库 → 推送 → 开启 Pages。

### 1. 安装 git

电脑上已有 conda，可以用它装 git：

```powershell
conda install -c conda-forge git
```

装完后配置身份（只需一次）：

```powershell
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

### 2. 在 GitHub 上建仓库

1. 注册 / 登录 [github.com](https://github.com)；
2. 右上角 `+` → `New repository`；
3. 仓库名填 `你的用户名.github.io`（注意这个格式），选 Public，不要勾选任何初始化选项，点创建。

### 3. 推送代码

在本目录打开 PowerShell，执行：

```powershell
git init
git add .
git commit -m "第一次上线"
git branch -M main
git remote add origin https://github.com/你的用户名/你的用户名.github.io.git
git push -u origin main
```

### 4. 开启 Pages

1. 进入仓库 → `Settings` → `Pages`；
2. `Source` 选择 `Deploy from a branch`，分支选 `main`，目录选 `/ (root)`，保存；
3. 等一两分钟，你的网站就会出现在 `https://你的用户名.github.io`。

之后每次改动，直接**双击 `发布.bat`** 即可（等价于 `git add .` + `git commit` + `git push`）。

## 以后可以再加什么

- 评论区：可以用 Giscus（基于 GitHub Discussions，免费）
- 后台管理：以后想不写代码也能发文章，可以考虑迁到 WordPress / Ghost / Halo
- 自定义域名：在域名注册商处买域名后，到 Pages 设置里绑定即可
- 站点图标（favicon）、更多页面、图片等
