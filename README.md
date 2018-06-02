#### **ReadMe file**

#### this is the repository for my blog of hexo

[博客地址](https://huqianshan.github.io)

#### 流程图
![](http://7xshxx.com2.z0.glb.clouddn.com/hexo_process.png)

### 实施前提
1. 旧终端/电脑已安装hexo环境
2. 旧终端/电脑hexo正常工作
3. 旧终端/电脑能通过hexo g -d正常发布至远程xxx.github.io
### 实施步骤
新建远程repo

在github上新增repo，例如名为myhexo，地址为`github.com/xxx/myhexo`

在旧终端中创建本地repo

进入本地hexo目录

`git init`

查看未提交的文件（默认不包含public、deploy文件）

`git status`

根据查看结果将本地hexo建站原始文件纳入版本控制（我本地是`scaffolds、source、themes`文件夹以及`.gitignore、_config.yml、package.json`文件）

```git
git add …
git commit -m …
```

需要注意的是.gitignore中需要增加一行，忽略~结尾的文件

`*~`

在旧终端中创建远程分支连接
```git
git remote add origin git@github.com:xxx/myhexo.git
git remote -v
```
显示如下：
```
origin git@github.com:XXX/myhexo.git (fetch)
origin git@github.com:XXX/myhexo.git (push)
```
在旧终端中提交本地文件至远程repo

`git push -u origin master`

换了终端以后

在新终端中安装node、git环境，配置github sshkey

在新终端中创建空目录作为hexo工作目录，从远程仓库中clone出之前备份的repo
```
mkdir hexo
cd hexo
git init
git clone git@github.com:xxx/myhexo.git
```

在新终端中git clone成功后，本地出现myhexo文件夹，开始安装hexo环境
```
cd myhexo
npm install hexo
npm install
npm install hexo-deployer-git
```
查看本地同步效果，访问localhost:4000
```
hexo g
hexo server
```
在新终端中继续使用和管理hexo

新建文章并修改

`hexo new xxx`

提交原始md文件至远程repo
```
git status
git add
git commit -m xx
git push
```
发布静态网页

`hexo g -d`

切换至旧终端使用hexo

更新网站原始文件
```
git pull
hexo g
hexo server
```
测试更新成功后，表明终端顺利切换完成