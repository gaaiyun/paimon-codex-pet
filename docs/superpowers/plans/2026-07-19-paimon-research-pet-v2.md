# Paimon Research Pet v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 生成、验证、安装并发布一套高级卡通科研打工人 Paimon Pet，保留 Codex 官方 8×9 atlas、57 帧与应用控制的正常播放速度。

**Architecture:** `hatch-pet` 在 G 盘建立可复现 run，`imagegen` 用 canonical base 和逐行布局 guide 生成 9 个状态条带，确定性脚本负责抠图、单帧检查、atlas 合成与预览。通过 QA 后先备份本机包，再更新 `G:\codex-home\pets\paimon` 与 `G:\github\paimon-codex-pet`，最后验证、提交并推送。

**Tech Stack:** PowerShell 7、Python 3.13、Pillow、Codex `hatch-pet` / `imagegen` skills、Git、WebP/PNG。

---

## 文件结构

- `G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\`：杯架修订后的生成源、prompt、frames、final 与 QA；不把大文件写入 C 盘。旧 run 保留为审计记录，不覆盖。
- `G:\codex-home\pets\paimon\`：Codex 实际加载包，只保存 `pet.json` 与 `spritesheet.webp`。
- `G:\CodexPetBackups\paimon-$stamp\`：覆盖前的可恢复备份与哈希记录，`$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'`。
- `G:\github\paimon-codex-pet\pet\paimon\`：可分发 Pet 包。
- `G:\github\paimon-codex-pet\assets\frames\`：57 个最终透明单帧。
- `G:\github\paimon-codex-pet\assets\expressions\`、`assets\gallery\`：精选帧与总览。
- `G:\github\paimon-codex-pet\qa\`：contact sheet、GIF/视频预览和 JSON 验证结果。
- `G:\github\paimon-codex-pet\source\`：本轮 `pet_request.json` 与生成 prompt。

### Task 1: 建立可复现生成 run

**Files:**
- Create: `G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\pet_request.json`
- Create: `G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\imagegen-jobs.json`
- Read: `G:\CodexDreamSkin\assets\paimon-research-half-rim-2560x1440.png`

- [ ] **Step 1: 确认参考图、仓库和本机包存在**

Run:

```powershell
@(
  'G:\CodexDreamSkin\assets\paimon-research-half-rim-2560x1440.png',
  'G:\codex-home\pets\paimon\pet.json',
  'G:\codex-home\pets\paimon\spritesheet.webp',
  'G:\github\paimon-codex-pet\.git'
) | ForEach-Object { if (-not (Test-Path -LiteralPath $_)) { throw "Missing: $_" } }
```

Expected: 无输出且退出码为 0。

- [ ] **Step 2: 准备 run、布局 guides 与逐状态 prompts**

Run:

```powershell
python 'G:\codex-home\skills\hatch-pet-installed\scripts\prepare_pet_run.py' `
  --pet-name 'Paimon' `
  --pet-id 'paimon' `
  --display-name 'Paimon' `
  --description 'A cute high-efficiency research and coding companion with glasses, coffee, and a tiny keyboard.' `
  --reference 'G:\CodexDreamSkin\assets\paimon-research-half-rim-2560x1440.png' `
  --output-dir 'G:\CodexPetRuns\paimon-research-v2-cupholder-20260719' `
  --pet-notes 'Consistent chibi Paimon-inspired research worker: white bob hair, star hair clip, clean gold halo with nothing on it, half-rim glasses, pencil in hair, black-gold compact keyboard, short closed black-gold travel cup secured in an integrated spill-proof holder on the keyboard rear-right corner; cute, goofy, efficient, writing papers and code. Never place the cup on the head, halo, hair, or in either hand.' `
  --style-preset sticker `
  --style-notes 'Premium non-pixel cartoon sticker; pearl white, warm ivory, champagne gold, graphite black, tiny icy-cyan accent; no purple, pink, neon blue, text, UI, scenery, shadows, speed lines, loose particles, or soft effects.' `
  --chroma-key auto `
  --force
```

Expected: `pet_request.json`、`imagegen-jobs.json`、10 个 prompt 文件和 9 个布局 guide 均存在。

- [ ] **Step 3: 检查 job 依赖和帧数**

Run:

```powershell
$jobs = Get-Content -Raw 'G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\imagegen-jobs.json' | ConvertFrom-Json
if ($jobs.jobs.Count -ne 10) { throw 'Expected 10 image jobs' }
$request = Get-Content -Raw 'G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\pet_request.json' | ConvertFrom-Json
if (($request.rows.frames | Measure-Object -Sum).Sum -ne 57) { throw 'Expected 57 used frames' }
```

Expected: 无异常。

### Task 2: 锁定 canonical base

**Files:**
- Create: `G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\decoded\base.png`
- Create: `G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\references\canonical-base.png`
- Modify: `G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\imagegen-jobs.json`

- [ ] **Step 1: 生成 base**

使用 `imagegen` 内置模式读取 `prompts\base-pet.md`，并把壁纸作为角色/材质参考图。输出必须是单个完整角色、平坦 chroma 背景、无场景和影子。

Expected: 半框眼镜、铅笔、键盘与右后角一体杯架在缩小到 192×208 预览时仍清晰；光环纯净，杯子不在头顶、光环、头发或手中；无紫、粉、霓虹蓝。

- [ ] **Step 2: 固化 canonical identity**

将选中输出复制为 `decoded\base.png` 与 `references\canonical-base.png`，在 `imagegen-jobs.json` 中把 `base` 标记为 `complete` 并记录源路径和 UTC 时间。

Expected: 两个文件 SHA-256 相同，`base.status` 为 `complete`。

### Task 3: 生成身份与步态检查行

**Files:**
- Create: `G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\decoded\idle.png`
- Create: `G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\decoded\running-right.png`

- [ ] **Step 1: 分别生成 `idle` 与 `running-right`**

每个 worker 只处理一行，读取对应 prompt，并同时附加 `references\canonical-base.png` 与该状态同名的 layout guide（此处分别为 `idle.png` 和 `running-right.png`）。最多同时运行两个生成 worker。

Expected: `idle` 恰好 6 个姿态，`running-right` 恰好 8 个向右步态；角色、眼镜、铅笔、键盘和右后角杯架一致，杯子不离开杯架，无布局线、裁切或游离特效。

- [ ] **Step 2: 记录两行完成状态**

复制选中条带到 `decoded`，逐个更新 manifest；不得把只存在于默认生成目录的图片作为项目输入。

Expected: 两行 `status=complete` 且目标文件存在。

- [ ] **Step 3: 决定左跑生成策略**

由于铅笔、眼镜细节和键盘右后角杯架具有方向性，`running-left` 独立生成，不镜像 `running-right`。

Expected: `running-left.derivation_policy` 保持生成路径，不调用镜像脚本。

### Task 4: 生成剩余 7 个状态行

**Files:**
- Create: `G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\decoded\running-left.png`
- Create: `G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\decoded\waving.png`
- Create: `G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\decoded\jumping.png`
- Create: `G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\decoded\failed.png`
- Create: `G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\decoded\waiting.png`
- Create: `G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\decoded\running.png`
- Create: `G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\decoded\review.png`

- [ ] **Step 1: 按最多两个并发 worker 生成所有行**

每行读取自身 prompt、canonical base 与自身 layout guide；若遇到 transport `Bad Request`，仅用该行 retry prompt 重试一次。

Expected: 每行精确满足 8/4/5/8/6/6/6 帧，所有姿势分离、完整、未裁切。

- [ ] **Step 2: 逐行做快速语义 QA 并记录 manifest**

拒绝身份漂移、紫色、阴影、速度线、尘土、游离标点与 UI；`running` 必须是高速打字而非原地奔跑，`review` 必须是扶眼镜核对，`waiting` 必须像在等用户决定。

Expected: 10 个 jobs 全部 `complete`，且每个生成行都存在 canonical base 与 guide 输入记录。

### Task 5: 确定性合成与视觉 QA

**Files:**
- Create: `G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\frames\`
- Create: `G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\final\spritesheet.webp`
- Create: `G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\final\validation.json`
- Create: `G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\qa\contact-sheet.png`
- Create: `G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\qa\previews\*.gif`
- Create: `G:\CodexPetRuns\paimon-research-v2-cupholder-20260719\qa\review.json`

- [ ] **Step 1: 提取并检查 57 个单帧**

Run:

```powershell
$skill='G:\codex-home\skills\hatch-pet-installed\scripts'
$run='G:\CodexPetRuns\paimon-research-v2-cupholder-20260719'
python "$skill\extract_strip_frames.py" --decoded-dir "$run\decoded" --output-dir "$run\frames" --states all --method auto
python "$skill\inspect_frames.py" --frames-root "$run\frames" --json-out "$run\qa\review.json" --require-components
```

Expected: `qa\review.json` 无 errors，57 个已用帧均非空。

- [ ] **Step 2: 合成并验证 atlas**

Run:

```powershell
python "$skill\compose_atlas.py" --frames-root "$run\frames" --output "$run\final\spritesheet.png" --webp-output "$run\final\spritesheet.webp"
python "$skill\validate_atlas.py" "$run\final\spritesheet.webp" --json-out "$run\final\validation.json"
```

Expected: 1536×1872、透明、≤20 MiB、已用单格非空、未用单格全透明、透明像素 RGB 归零。

- [ ] **Step 3: 生成可视化 QA**

Run:

```powershell
python "$skill\make_contact_sheet.py" "$run\final\spritesheet.webp" --output "$run\qa\contact-sheet.png"
python "$skill\render_animation_previews.py" --frames-root "$run\frames" --output-dir "$run\qa\previews"
```

Expected: contact sheet 与 9 个 GIF 均存在。

- [ ] **Step 4: 最终视觉检查与最小修复**

视觉 QA 同时检查 contact sheet 与 9 个 GIF。若仅因提取导致尺寸或基线跳动，改用 `--method stable-slots` 重跑确定性流水线；只有源条带本身失败时才重新生成对应状态行。

Expected: `visual_qa=pass`，无身份漂移、方向错误、静止假动画、异常缩放跳变或速度线等禁用效果。

### Task 6: 备份并安装本机 Pet

**Files:**
- Create: `G:\CodexPetBackups\paimon-$stamp\`，其中 `$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'`
- Modify: `G:\codex-home\pets\paimon\pet.json`
- Modify: `G:\codex-home\pets\paimon\spritesheet.webp`

- [ ] **Step 1: 复制旧包并生成哈希**

用时间戳建立唯一备份目录，复制旧 `pet.json` 与 `spritesheet.webp`，对源文件和备份分别运行 `Get-FileHash -Algorithm SHA256`。

Expected: 两边文件数量相同且对应 SHA-256 相同；不删除旧包。

- [ ] **Step 2: 安装新包**

把已验证的 `final\spritesheet.webp` 复制到本机包，写入 `id=paimon`、`displayName=Paimon`、新描述与 `spritesheetPath=spritesheet.webp` 的 UTF-8 无 BOM `pet.json`。

Expected: 新本机 spritesheet 与 run 最终 WebP 的 SHA-256 相同。

- [ ] **Step 3: 本机静态加载检查**

Run:

```powershell
python 'G:\codex-home\skills\hatch-pet-installed\scripts\validate_atlas.py' 'G:\codex-home\pets\paimon\spritesheet.webp'
Get-Content -Raw 'G:\codex-home\pets\paimon\pet.json' | ConvertFrom-Json | Out-Null
```

Expected: atlas 验证成功且 JSON 可解析。不要自动重启 Codex。

### Task 7: 同步仓库素材与文档

**Files:**
- Modify: `G:\github\paimon-codex-pet\pet\paimon\pet.json`
- Modify: `G:\github\paimon-codex-pet\pet\paimon\spritesheet.webp`
- Delete: `G:\github\paimon-codex-pet\pet\paimon\spritesheet.png`
- Modify: `G:\github\paimon-codex-pet\assets\frames\**\*.png`
- Modify: `G:\github\paimon-codex-pet\assets\expressions\*.png`
- Modify: `G:\github\paimon-codex-pet\assets\gallery\*.png`
- Modify: `G:\github\paimon-codex-pet\assets\manifest.json`
- Modify: `G:\github\paimon-codex-pet\qa\*`
- Modify: `G:\github\paimon-codex-pet\source\*`
- Modify: `G:\github\paimon-codex-pet\README.md`
- Modify: `G:\github\paimon-codex-pet\docs\QA.md`

- [ ] **Step 1: 替换正式包和 57 个帧**

复制 run 的 `pet.json` / `spritesheet.webp` 和 `frames`；删除仓库旧的 active PNG 仅在 WebP 验证与复制完成后执行。

Expected: 仓库正式包只含 JSON 与 WebP，frame manifest 总数为 57。

- [ ] **Step 2: 重建 gallery、expressions 与 QA**

从最终帧选择 8 个代表表情，更新状态总览与 contact sheet，复制 9 个 GIF 和验证 JSON；所有绝对路径改为仓库可读的相对说明或 provenance。

Expected: manifest 中每个路径存在，gallery 与 QA 可直接打开。

- [ ] **Step 3: 更新说明和生成来源**

README 与 QA 文档改为当前官方 WebP 合约、9 状态语义、应用控制速度、Reduced Motion 行为、G 盘安装示例和不自动重启说明；同步本轮 prompts 与 `pet_request.json`。

Expected: 不再声称 PNG 是 active 包，不再使用旧像素风描述。

### Task 8: 最终验证、提交和推送

**Files:**
- Test: `G:\github\paimon-codex-pet\tools\validate_atlas.py`

- [ ] **Step 1: 运行仓库验证和 Git 检查**

Run:

```powershell
python 'G:\github\paimon-codex-pet\tools\validate_atlas.py'
git -C 'G:\github\paimon-codex-pet' diff --check
git -C 'G:\github\paimon-codex-pet' status --short
```

Expected: `Result: ok`，`diff --check` 无输出，状态只包含本轮升级文件。

- [ ] **Step 2: 提交升级**

Run:

```powershell
git -C 'G:\github\paimon-codex-pet' add --all
git -C 'G:\github\paimon-codex-pet' commit -m 'feat(pet): 升级派蒙科研打工人动画'
```

Expected: hooks 正常通过，commit message 不含 AI 或共同署名。

- [ ] **Step 3: 推送并核对远端**

Run:

```powershell
git -C 'G:\github\paimon-codex-pet' push origin main
git -C 'G:\github\paimon-codex-pet' status --short --branch
```

Expected: `main...origin/main` 无 ahead/behind，工作树干净。
