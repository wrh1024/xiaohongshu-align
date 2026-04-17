# 小红书首页帖子对齐

统一小红书首页帖子卡片高度，使其左右对齐。

![效果预览](screenshot.jpg)

## 功能

- 自动统一帖子卡片高度
- 支持响应式布局
- 自动适配无限滚动加载的新内容
- 文字添加阴影效果提升可读性

## 安装

### 方法一：Tampermonkey（推荐）

1. 安装 [Tampermonkey](https://www.tampermonkey.net/) 浏览器扩展
2. 点击 [xiaohongshu-align.user.js](xiaohongshu-align.user.js) 安装脚本
3. 刷新小红书页面

### 方法二：浏览器开发者工具

1. 打开小红书首页
2. 按 F12 打开开发者工具
3. 在 Console 中粘贴 `xiaohongshu-align.user.js` 的代码（去掉头部的油猴注释）

## 使用方法

脚本会自动应用，无需任何操作。

## 测试

在本地打开 `test.html` 即可测试脚本效果。

```bash
python test_align.py
```

## 截图预览

![小红书首页帖子对齐效果](screenshot.jpg)

> 截图位置：`C:\Users\wrh\OneDrive\opencodee\小红书首页帖子对齐\屏幕截图_17-4-2026_2027_www.xiaohongshu.com.jpeg`

## License

MIT
