---
title: 薅资本主义的羊毛，利用GitHub搭建一个hexo博客
date: 2018-02-03 22：25
tags: [hexo,GitHub]
---

------



> * 安装 node.js Git
> * 创建GitHub仓库，关联ssh key
> * 安装hexo 搭建本地博客
> * 克隆主题样式，修改整站配置文件
> * 撰写博文 1. 创建文件 2. 使用MarkDown语法编辑
> * 部署博客至GitHub 



------


![cmd-markdown-logo](https://cloud.githubusercontent.com/assets/2175271/19885143/62e9269c-a01d-11e6-8e26-e36a36201d88.png)



***安装hexo***                
`$ npm install hexo -g`

***初始化***
`$ hexo init`

***安装依赖包***
`$ npm install`

***确保git部署***
`$ npm install hexo-deployer-git --save`

*** 本地查看\ ***
```
$ hexo generate #(or) hexo g
$ hexo server   #(or) hexo s
```
*hexo g 每次进行相应改动都要hexo g 生成一下*

*hexo s 启动服务预览*

主要配置文件是 _config.yml ，可以用记事本打开，推荐使用 sublime 或者nodepad++打开。


```
# Hexo Configuration
## Docs: http://zespia.tw/hexo/docs/configure.html
## Source: https://github.com/tommy351/hexo/

# Site 这里的配置，哪项配置反映在哪里，可以参考我的博客
title: My Blog #博客名
subtitle: to be continued... #副标题
description: My blog #给搜索引擎看的，对网站的描述，可以自定义
author: Yourname #作者，在博客底部可以看到
email: yourname@yourmail.com #你的联系邮箱
language: zh-CN #中文。如果不填则默认英文

# URL #这项暂不配置，绑定域名后，欲创建sitemap.xml需要配置该项
## If your site is put in a subdirectory, set url as 'http://yoursite.com/child' and root as '/child/'
url: http://yoursite.com
root: /
permalink: :year/:month/:day/:title/
tag_dir: tags
archive_dir: archives
category_dir: categories

# Writing 文章布局、写作格式的定义，不修改
new_post_name: :title.md # File name of new posts
default_layout: post
auto_spacing: false # Add spaces between asian characters and western characters
titlecase: false # Transform title into titlecase
max_open_file: 100
filename_case: 0
highlight:
  enable: true
  backtick_code_block: true
  line_number: true
  tab_replace:

# Category & Tag
default_category: uncategorized
category_map:
tag_map:

# Archives 默认值为2，这里都修改为1，相应页面就只会列出标题，而非全文
## 2: Enable pagination
## 1: Disable pagination
## 0: Fully Disable
archive: 1
category: 1
tag: 1

# Server 不修改
## Hexo uses Connect as a server
## You can customize the logger format as defined in
## http://www.senchalabs.org/connect/logger.html
port: 4000
logger: false
logger_format:

# Date / Time format 日期格式，可以修改成自己喜欢的格式
## Hexo uses Moment.js to parse and display date
## You can customize the date format as defined in
## http://momentjs.com/docs/#/displaying/format/
date_format: YYYY-M-D
time_format: H:mm:ss

# Pagination 每页显示文章数，可以自定义，贴主设置的是10
## Set per_page to 0 to disable pagination
per_page: 10
pagination_dir: page

# Disqus Disqus插件，我们会替换成“多说”，不修改
disqus_shortname:

# Extensions 这里配置站点所用主题和插件，暂时默认
## Plugins: https://github.com/tommy351/hexo/wiki/Plugins
## Themes: https://github.com/tommy351/hexo/wiki/Themes
theme: landscape
exclude_generator:
plugins:
- hexo-generator-feed
- hexo-generator-sitemap

# Deployment 站点部署到github要配置
## Docs: http://zespia.tw/hexo/docs/deploy.html
deploy:
  type: git
  repository: 
  branch: master
```
更新主题
git bash 里执行
`$ cd themes/主题名`
`$ git pull`

 复制SSH码
进入 Github 个人主页中的Repository，复制新建的独立博客项目

 编辑整站配置文件打开 H:\username.github.io_config.yml,把刚刚复制的 SSH 码粘贴到“repository：”后面，*别忘了冒号后要空一格。*
```
deploy:
  type: git
  repository: git@github.com:username/username.github.io.git
  branch: master
```
首先还是在 `.\username.github.io` 目录下右键 Git Bash，执行 `hexo n` 命令，会生成指定名称的 markdown 文件至 username.github.io\source_posts\postName.md：

    hexo new [layout] "filename"
    
    
修改文档
修改file.md开头

```
title: postName #文章页面上的显示名称，可以任意修改，不会出现在URL中
date: 2013-12-02 15:30:16 #文章生成时间，一般不改，当然也可以任意修改
categories: #文章分类目录，可以为空，注意:后面有个空格
tags: #文章标签，可空，多标签请用格式[tag1,tag2,tag3]，别忘了冒号后面有个空格
---
```





提交新文档
```
$ hexo s
$ hexo d
```


---
参考文献：

1. [hexo主题cactus-dark](https://github.com/probberechts/cactus-dark)
2. [用Github搭建个人独立博客——小白篇/](http://www.wuyalan.com/2016/02/23/%E7%94%A8Github%E6%90%AD%E5%BB%BA%E4%B8%AA%E4%BA%BA%E7%8B%AC%E7%AB%8B%E5%8D%9A%E5%AE%A2%E2%80%94%E2%80%94%E5%B0%8F%E7%99%BD%E7%AF%87/)
3. [npm文档](http://www.runoob.com/nodejs/nodejs-npm.html)
4. [hexo官方文档](https://hexo.io/docs/index.html)
5. [ hexo博客出现command not found解决方案](http://blog.csdn.net/whjkm/article/details/42675579)
6. [在线Markdown编辑器](https://zybuluo.com/mdeditor)







