# 哔哩哔哩用户相册图片下载

下载 B 站用户的相册图片，并建立本地数据库。

API 来自浏览器调试
https://api.bilibili.com/x/dynamic/feed/draw/doc_list?uid={uid}&page_num={page_num}&page_size=30&biz=all&jsonp=jsonp

## 使用方法

1. 安装依赖 `pip install -r requirements`

2. 编写 xxx.toml 配置，然后 `python -m album xxx.toml`

toml 配置示例：

```toml
uid = 168687092
root = 'D:/Pictures/acgn'
name = 'bili-空美町'
```
