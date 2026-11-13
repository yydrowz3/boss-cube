# 源码使用

`build_model.py` 从旁边的 `images.jpg` 提取原图字形，重新生成通用彩色 3MF、两份 STL、轮廓数据、几何验证和预览图。

安装 Python 3.11 或更新版本与 uv 后，在此目录运行：

```sh
uv run build_model.py
```

脚本头部声明了依赖，uv 会建立运行环境。输出在本目录新建的 `BOSS_cube_35mm` 子目录，不会覆盖交付的 Bambu 工程。

尺寸常量为 `SIDE=35.0`、`LOGO_WIDTH=28.0`、`RELIEF=0.8`，单位毫米。字形直接来自参考图，没有替换字体。

生成器输出不绑定机型。实际 P2S 工艺已保存在交付目录的 `BOSS_cube_35mm_P2S_04.3mf`；`verified_process_settings.json` 是本次核对的参数清单，可按主说明书在 Studio 中复现。AMS 槽位需连接后确认。
