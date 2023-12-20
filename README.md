# bili-album  哔哩哔哩用户相册图片下载器

下载 B 站用户的相册图片，并维护本地数据库，以保持更新。

> API 来自浏览器调试：
> `https://api.bilibili.com/x/dynamic/feed/draw/doc_list?uid={uid}&page_num={page_num}&page_size=30&biz=all&jsonp=jsonp`

## 使用方法

1. 克隆或下载本项目，安装本程序：在项目根目录执行 `pip install .`
2. 运行 CLI 程序 `bili-album`

CLI 程序提供两个命令 `up-db` 和 `up-img` ，分别更新数据库和下载图片。

编写 `xxx.toml` 配置文件，然后 `bili-album up-db xxx.toml` 、 `bili-album up-img xxx.toml`

配置示例：

```toml
['bili-空美町'] # 图片保存目录名及数据库名（键名记为 name），注意引号！
uid = 168687092
root = 'D:/Pictures/acgn' # 图片及数据库保存路径，注意引号。图片保存到 {root}/{name}/，数据库保存到 {root}/{name}.db
['Marias马睿思']
uid = 474960080
root = 'D:/Pictures/data'
ignore = true # 可选，设置忽略为 true 则会跳过该项
```

## TODO

本项目使用 aiohttp 异步请求，效率很高，但下载图片时图片过多（例如下载 5000 张图片）会出现 TCP 链接超时问题。
