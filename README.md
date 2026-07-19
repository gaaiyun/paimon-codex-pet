# 派蒙科研打工人 Codex Pet

一套适配 Codex / ChatGPT 桌面端 Pets 的自定义动画素材。角色采用非像素的高级卡通贴纸风：半框眼镜、发间铅笔、黑金键盘，以及固定在键盘右后角防洒杯架里的带盖保温杯。光环保持纯净，不再把咖啡杯放在头顶。

> 这是 fan-made / inspired 自定义素材，不是官方资源，也不与 HoYoverse、miHoYo、Genshin Impact 或 OpenAI 存在授权、赞助或背书关系。

![九个状态总览](qa/contact-sheet.png)

## 安装

本仓库当前正式加载包只有两个文件：

```text
pet/paimon/
  pet.json
  spritesheet.webp
```

复制到本机 Codex Pets 目录：

```powershell
$target = 'G:\codex-home\pets\paimon'
New-Item -ItemType Directory -Force -Path $target | Out-Null
Copy-Item -LiteralPath '.\pet\paimon\pet.json' -Destination $target -Force
Copy-Item -LiteralPath '.\pet\paimon\spritesheet.webp' -Destination $target -Force
```

然后在桌面端 Settings > Pets 中刷新并选择 Paimon。是否重启由用户自行决定。

## 官方格式

本包遵循当前 [Pets 官方文档](https://learn.chatgpt.com/docs/pets?surface=app)：

- 透明 WebP。
- 精确尺寸 1536×1872。
- 8 列×9 行 atlas，单格 192×208。
- 文件小于 20 MiB。
- Reduced Motion 开启时使用静态帧。
- 动画速度由桌面应用控制，本项目不写入帧率或加速逻辑。

## 动画状态

| 行 | 状态 | 帧数 | 用途 |
| --- | --- | ---: | --- |
| 0 | `idle` | 6 | 呼吸、眨眼与轻微表情变化 |
| 1 | `running-right` | 8 | 向右移动 |
| 2 | `running-left` | 8 | 向左移动，独立生成以保持杯架方向 |
| 3 | `waving` | 4 | 抬手问候 |
| 4 | `jumping` | 5 | 蓄力、腾空与落回 |
| 5 | `failed` | 8 | 眼镜滑低、垂头与趴键盘 |
| 6 | `waiting` | 6 | 等待用户批准、回答或决定 |
| 7 | `running` | 6 | 打字、思考与继续处理任务 |
| 8 | `review` | 6 | 扶眼镜、核对与确认 |

合计 57 个有效帧。未使用单格保持全透明。

## 仓库内容

- `pet/paimon/`：可直接安装的 Pet 包。
- `assets/frames/`：57 个透明单帧。
- `assets/expressions/`：8 个代表性表情。
- `assets/gallery/`：状态与表情总览。
- `source/`：canonical base、生成请求、prompt 和 job provenance。
- `qa/contact-sheet.png`：九个状态总览。
- `qa/previews/*.gif`：本版九个状态的动画预览。
- `qa/review.json`、`qa/validation.json`：帧级与 atlas 验证结果。
- `qa/videos/`、`qa/validation-png.json`：v1 历史记录，不是当前加载入口。

## 验证

```powershell
python .\tools\validate_atlas.py
```

当前构建结果：1536×1872 RGBA WebP、57 个有效帧、透明 RGB 残留 0、帧检查 0 errors / 0 warnings。

## 版权与使用

本项目不授予任何第三方角色、商标或游戏 IP 的授权。建议作为个人自定义 Pet 使用；公开分发或商用前请确认相应权利。
