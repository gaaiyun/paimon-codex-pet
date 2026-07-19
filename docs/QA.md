# QA Notes

当前正式包使用 `pet/paimon/spritesheet.webp`。PNG 与 `qa/videos/` 只保留为 v1 历史记录，不参与本版加载或验收。

## 本版验证结果

- Format: WebP / RGBA
- Dimensions: 1536×1872
- Grid: 8×9
- Cell: 192×208
- Used frames: 57
- Transparent RGB residue: 0
- Frame inspection: 0 errors, 0 warnings
- Atlas validation: 0 errors, 0 warnings

对应文件：

- `qa/review.json`
- `qa/validation.json`
- `qa/contact-sheet.png`
- `qa/previews/*.gif`

## 复验

```powershell
python .\tools\validate_atlas.py
```

预期最后一行：

```text
Result: ok
```

视觉检查重点是九个状态中的脸型、半框眼镜、发间铅笔、纯净光环、黑金键盘和键盘右后角杯架保持一致。播放速度由 Codex 桌面应用控制，不在 Pet 文件里修改。
