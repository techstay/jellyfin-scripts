# jellyfin-scripts

我的 jellyfin 脚本库，包含了一些整理 jellyfin 媒体库时所使用的脚本。脚本利用了 AI，所以需要配置自己的 API_KEY。各脚本作用请自行查看对应文件，都是比较简单的功能，脚本初衷也是随用随改。

## 开发环境

### 初始化

```py
pdm update
```

### 运行脚本

具体重命名文件的格式查看脚本内代码和 AI 提示词。

```shell
# 批量修改电视剧/动漫名称
python rename_shows.py <show_dir>
# 专门修改物语系列动画
python rename_monogatari.py <show_dir>
# 批量修改字幕匹配视频文件
python rename_subtitles.py <show_dir>
```

### 测试

```bash
# 测试并显示输出
pytest -s
# 测试并显示输出，只测试某关键字
pytest -s -k deepseek
```
