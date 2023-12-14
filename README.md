# bili-album  哔哩哔哩用户相册图片下载器

下载 B 站用户的相册图片，并维护本地数据库。

API 来自浏览器调试：
`https://api.bilibili.com/x/dynamic/feed/draw/doc_list?uid={uid}&page_num={page_num}&page_size=30&biz=all&jsonp=jsonp`

## 使用方法

编写 `xxx.toml` 配置，然后 `python -m bili_album xxx.toml`

配置示例：

```toml
['bili-空美町'] # 图片保存目录名及数据库名（键名记为 name），注意引号！
uid = 168687092
root = 'D:/Pictures/acgn' # 图片及数据库保存路径，注意引号！。图片保存到 {root}/{name}，数据库保存到 {root}/db_{name}.db
['Marias马睿思']
uid = 474960080
root = 'D:/Pictures/data'
```

## TODO

本项目使用 requests 同步下载， sqlite3 作为数据库保持更新，效率较低。

计划使用 scrapy 重构。
