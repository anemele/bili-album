# 哔哩哔哩用户相册图片下载

下载 B 站用户的相册图片，并维护本地数据库。

API 来自浏览器调试
`https://api.bilibili.com/x/dynamic/feed/draw/doc_list?uid={uid}&page_num={page_num}&page_size=30&biz=all&jsonp=jsonp`

## 使用方法

1. 安装依赖 `pip install -r requirements`

2. 编写 `xxx.toml` 配置，然后 `python -m album xxx.toml`

配置示例：

```toml
uid = 168687092 # up uid
root = 'D:/Pictures/acgn' # 图片及数据库保存路径
name = 'bili-空美町' # 图片保存目录名及数据库名
```
