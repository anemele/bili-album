# bili-album  哔哩哔哩用户相册图片下载器

下载 B 站用户的相册图片，支持增量更新。

> API 来自浏览器调试

## 使用方法

1. 克隆或下载本项目，安装本程序：在项目根目录执行 `pip install .`
2. 运行 CLI 程序 `bili-album`

编写 `xxx.toml` 配置文件，然后 `bili-album xxx.toml`

配置示例：

```toml
root = 'D:/Pictures' # 图片保存路径，注意引号！
[[up]] # 固定写法
name = 'bili-空美町'# 图片保存到 {root}/{name}/，注意引号！
uid = '168687092' # 注意引号！
[[up]]
name = 'Marias马睿思'
uid = '474960080'
```
