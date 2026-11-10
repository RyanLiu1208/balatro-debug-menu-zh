# Balatro Debug Menu ZH · 小丑牌内置调试菜单汉化

**开启游戏自带的 Tab 调试菜单，隐藏黑色 LÖVE 控制台，并提供中文菜单补丁。**

**Enable Balatro's built-in Tab debug menu, hide the black LÖVE console, and optionally translate the menu into Simplified Chinese.**

本项目是配置文件和文字补丁，不是之前的实时辅助器。不需要 Lovely、Steamodded 或其他模组加载器。仓库不包含 Balatro.exe、完整游戏脚本、图片、存档或游戏资源。

This project contains a configuration file and a text patch, separate from the earlier real-time companion. It requires no Lovely, Steamodded, or other mod loader. No game executable, full game scripts, images, saves, or game assets are distributed.

## 1. 文件用途 / What each file does

| 文件 / File | 中文说明 | English |
|---|---|---|
| [`conf.lua`](conf.lua) | 开启内置调试功能，关闭黑色控制台；文件内有中英注释。**单独替换它不会汉化菜单。** | Enables built-in debugging and disables the console. Includes bilingual comments. **Replacing this file alone does not translate the menu.** |
| [`translations.json`](translations.json) | 调试菜单 27 条英文原文与中文译文的对照。 | Maps 27 original English menu strings to Chinese. |
| [`patch.py`](patch.py) | 可选的本地补丁工具：将配置和汉化同时写进你自己的游戏 EXE，先备份再替换。 | Optional local patcher: installs both the configuration and translation into your own EXE, backing it up before replacement. |
| [`tests/`](tests) | 使用模拟 EXE/ZIP 测试补丁，不需要游戏文件。 | Tests using synthetic EXE/ZIP fixtures; no game files needed. |

**为什么不能只汉化 conf.lua？** 它只是启动配置。菜单按钮和说明位于游戏内部的 `functions/UI_definitions.lua`。完整中文菜单需要同时修改这两个文件。补丁工具只改配置和调试菜单文案，不改按钮回调。

**Why isn't a translated conf.lua enough?** It only controls startup settings. Menu labels live in `functions/UI_definitions.lua` inside the game. The complete Chinese menu requires changes to both files. The patcher changes the configuration and debug menu text, preserving button callbacks.

## 2. 兼容性与准备 / Compatibility and preparation

| 项目 / Item | 中文说明 | English |
|---|---|---|
| 已实测版本 / Tested version | Windows Steam 版 `1.0.1o-FULL`；已实际确认游戏启动和中文菜单显示。 | Windows Steam build `1.0.1o-FULL`; game startup and Chinese menu rendering were checked in-game. |
| 其他版本 / Other versions | 未逐一测试。英文文案变化时，自动补丁会拒绝继续，而不是盲目修改。 | Not individually tested. The patcher refuses unsupported menu text rather than making unchecked edits. |
| 游戏语言 / Game language | 完整汉化后建议在游戏中选择简体中文，以使用中文字体。 | Select Simplified Chinese in the game when using the translation so Chinese fonts are available. |
| 操作前 / Before editing | 保存并彻底退出游戏。备份整个原 EXE，以及 `%APPDATA%/Balatro` 中的存档。 | Save and fully exit the game. Back up the original EXE and saves under `%APPDATA%/Balatro`. |
| 更新覆盖 / Updates | Steam 更新、验证游戏文件或换回原 EXE，可能覆盖补丁。 | Steam updates, file verification, or restoring the original EXE may overwrite the patch. |

这是调试功能：解锁与发现会改变收藏进度，部分按钮会直接改变牌局。先在备份或测试存档中熟悉操作。

These are debug tools: Unlock and Discover change collection progress, and some buttons directly change the run. Learn the controls with a backup or test save.

## 3. 安装方式 A：手动替换 Lua / Option A: manually replace the Lua file

不需要 Python。此方式开启菜单并隐藏控制台，菜单默认仍是英文；需要中文时继续使用方式 B，或按第 5 节手动替换界面文案。

No Python is needed. This enables the menu and hides the console; labels remain English unless you also apply Option B or the UI translations in Section 5.

| 步骤 / Step | 中文 | English |
|---|---|---|
| 1 | 在 GitHub 点击 **Code → Download ZIP**，解压本项目。 | Select **Code → Download ZIP** on GitHub and extract this project. |
| 2 | Steam 游戏库 → 右键 Balatro → 管理 → 浏览本地文件，找到 `Balatro.exe`。 | In Steam, right-click Balatro → Manage → Browse local files, then locate `Balatro.exe`. |
| 3 | 把原 `Balatro.exe` 复制为备份，放在另一位置。 | Copy the original `Balatro.exe` to a separate backup location. |
| 4 | 用支持内嵌 ZIP 的压缩工具打开 `Balatro.exe` 的压缩包内容，找到根目录的 `conf.lua`。 | Open the EXE as an archive with a tool that supports embedded ZIPs and find `conf.lua` at the archive root. |
| 5 | 将仓库中的 `conf.lua` 拖入压缩包，确认替换同名文件，并等待写入完成。不要放进额外的文件夹。 | Drag this project's `conf.lua` into the archive, replace the existing file, and wait for writing to finish. Do not put it inside an extra folder. |
| 6 | 从 Steam 启动游戏，按住 **Tab** 查看菜单，松开关闭。 | Launch through Steam, hold **Tab** to show the menu, and release it to close. |

**不要把游戏全部解压后打成普通 ZIP，再改名为 EXE。** 游戏 EXE 前部还有启动程序，普通 ZIP 不能替代它。压缩工具如果无法正确写回内嵌压缩包，请改用方式 B。

**Do not extract everything, create a regular ZIP, and rename it to EXE.** The executable has a launcher prefix that a regular ZIP cannot replace. If your archive tool cannot safely update an embedded archive, use Option B.

## 4. 安装方式 B：同时应用配置和中文菜单 / Option B: apply config and Chinese labels together

需要本机 Python 3.9 或更新版本，仅使用标准库，**无需 pip 安装任何依赖**。先解压本项目，再在项目目录运行下列命令。请将示例路径替换为你自己的游戏位置。

Requires Python 3.9 or newer and uses only the standard library: **no pip dependencies**. Extract this project and run the following from its directory. Replace the sample path with your actual game location.

先检查兼容性，不修改游戏 / First check compatibility without changing the game:

```powershell
python patch.py --exe "C:\Program Files (x86)\Steam\steamapps\common\Balatro\Balatro.exe" --check
```

确认游戏已经退出，再应用补丁 / Fully exit the game, then apply the patch:

```powershell
python patch.py --exe "C:\Program Files (x86)\Steam\steamapps\common\Balatro\Balatro.exe"
```

如果电脑使用 `py` 启动 Python，可以将命令开头的 `python` 换成 `py -3`。

If your PC uses the `py` launcher, replace `python` with `py -3`.

成功时输出 `"modified": true`，并显示 `backup` 备份路径。备份位于游戏 EXE 旁边，名称形如 `Balatro.exe.before-debug-zh-时间戳.bak`。补丁会检查 ZIP 完整性、保留 EXE 启动部分，核对其他条目内容，然后替换。重复应用同一补丁会输出 `"already_applied": true`。

On success, output includes `"modified": true` and a `backup` path. The backup sits beside the EXE with a name like `Balatro.exe.before-debug-zh-TIMESTAMP.bak`. The patcher checks ZIP integrity, preserves the executable prefix, verifies other entries, then replaces the file. Reapplying the same patch reports `"already_applied": true`.

若出现权限错误，先确认游戏已完全退出且目标目录可写。失败时保留的 `.bak` 是恢复用的备份，不要当作游戏更新文件。

For permission errors, first ensure the game is fully closed and the target directory is writable. Any retained `.bak` file is a recovery backup, not a game update.

## 5. 完整中英对照 / Complete English–Chinese reference

这些字符串只属于调试菜单。手动汉化时，在 EXE 内的 `functions/UI_definitions.lua` 中找到 `create_UIBox_debug_tools()` 函数，只替换这个函数里的显示文案，保留引号、逗号、括号和回调名称。按 UTF-8 保存并替换回压缩包。自动方式已包含这一步。

These strings belong only to the debug menu. For manual translation, locate `create_UIBox_debug_tools()` in the EXE's `functions/UI_definitions.lua` and replace only its displayed text, preserving quotes, commas, braces, and callback names. Save as UTF-8 and replace the archive entry. The automatic patcher already performs this step.

| English / 英文原文 | 中文译文 |
|---|---|
| While in collection, hover over a card | 在收藏界面，将鼠标悬停在卡牌上 |
| and press the following keys: | 再按以下按键： |
| [1] Unlock | [1] 解锁 |
| [2] Discover | [2] 发现 |
| [3] Spawn | [3] 生成 |
| Hover over any Joker/Playing card | 将鼠标悬停在小丑牌或扑克牌上 |
| and press [Q] to cycle Edition | 按 [Q] 切换版本效果 |
| Press [H] to isolate background | 按 [H] 只显示背景 |
| Press [J] to play splash animation | 按 [J] 播放开场动画 |
| Press [8] to toggle cursor | 按 [8] 显示或隐藏鼠标 |
| Press [9] to toggle all tooltips | 按 [9] 显示或隐藏全部提示 |
| $10 | 金钱 +$10 |
| +1 Round | 轮次 +1 |
| +1 Ante | 底注 +1 |
| +1 Hand | 出牌 +1 |
| +1 Discard | 弃牌 +1 |
| Boss Reroll | 重掷 Boss |
| Background | 切换背景 |
| +10 chips | 筹码 +10 |
| +10 mult | 倍率 +10 |
| X2 chips | 筹码 ×2 |
| X10 mult | 倍率 ×10 |
| Win this Run | 赢下本局 |
| Lose this Run | 输掉本局 |
| Reset | 重置筹码倍率 |
| Jimbo | 金宝显示 |
| Jimbo talk | 金宝说话 |

## 6. 实际操作 / How to use the controls

### 显示菜单 / Showing the menu

按住 **Tab** 显示菜单，松开关闭；需要点击菜单按钮时，保持 Tab 按住，再用鼠标点击。Tab 是显示帮助面板，数字键和 Q 的功能并不要求同时按住 Tab。

Hold **Tab** to show the menu and release it to close. Keep Tab held while clicking menu buttons. Tab displays the panel; the number shortcuts and Q do not themselves require Tab to be held.

### 解锁、发现、生成 / Unlock, Discover, and Spawn

在收藏/卡牌展示菜单中，把鼠标停在目标卡牌上，再按数字键。不是只按键就随机送一张牌。

In a collection/card overlay, hover the intended card, then press the number key. Pressing the key without a hovered card does not award a random card.

| 按键 / Key | 中文解释 | English explanation |
|---|---|---|
| **1 — Unlock / 解锁** | 跳过这张牌的解锁条件，使其处于已解锁状态；不会直接加入当前牌局，也不自动标记为发现。 | Bypasses that card's unlock condition. It does not add a copy to the run or automatically mark it discovered. |
| **2 — Discover / 发现** | 先解锁，再标记为已发现，使收藏显示正常牌面与介绍；不会直接送到手中。 | Unlocks and marks the card discovered so its normal collection entry is revealed. Does not give a copy to the player. |
| **3 — Spawn / 生成** | 将鼠标指向的小丑牌或消耗牌加入当前牌局；必须已有对应区域且有空位。消耗牌包括塔罗、星球、幻灵。此快捷键不生成普通扑克牌，也不自动做永久解锁。 | Adds the hovered Joker or consumable to the current run if its area exists and has room. Consumables include Tarot, Planet, and Spectral cards. This shortcut does not spawn ordinary playing cards or automatically grant a permanent unlock. |

例：想使用蓝图，先进入牌局，再在能够打开的收藏界面找到蓝图，鼠标悬停并按 **3**；小丑槽满了不会生成。想只补收藏进度，按 **2**，无需生成。

Example: to obtain Blueprint, start a run, open an available collection view, hover Blueprint, and press **3**. It will not spawn if Joker slots are full. To fill collection progress without obtaining a copy, use **2**.

### 其他快捷键 / Other shortcuts

| 按键 / Key | 中文 | English |
|---|---|---|
| **Q** | 悬停小丑牌/扑克牌后，依次切换普通 → 闪箔 → 镭射 → 多彩 → 负片 → 普通。实际支持范围取决于被指向的卡牌。 | Hover a Joker/playing card to cycle Base → Foil → Holographic → Polychrome → Negative → Base. Applicability depends on the hovered card. |
| **H** | 隐藏/显示主要界面，观察背景；再次按可恢复。 | Toggles the main UI to isolate the background; press again to restore. |
| **J** | 切换开场动画显示，并离开当前牌局回到开场界面；不是无影响的预览按钮。 | Toggles the splash display and leaves the active run for the splash screen; this is not a harmless preview. |
| **8** | 显示/隐藏鼠标指针。 | Shows/hides the mouse cursor. |
| **9** | 切换额外提示显示状态。 | Toggles the debug tooltip display state. |

开启 `_RELEASE_MODE = false` 也会启用游戏原本存在的其他调试快捷键。本项目不删除或改写它们；例如 **B 会重新开始牌局，L 会重载已保存牌局**，不要在正常游玩时随意试按。

Setting `_RELEASE_MODE = false` also enables other debug shortcuts already present in the game. This project does not remove or rewrite them; for example, **B restarts a run and L reloads the saved run**. Avoid experimenting with unrelated shortcuts during a normal run.

### 菜单按钮 / Menu buttons

| 按钮 / Button | 中文用途 | English behavior |
|---|---|---|
| 金钱 +$10 / $10 | 当前牌局增加 $10。 | Adds $10 to the current run. |
| 轮次 +1 / +1 Round | 轮次计数加一；不是自动完整打完一个盲注。 | Increments the round counter; does not simulate completing a blind. |
| 底注 +1 / +1 Ante | 底注计数加一；不是保证获得下一底注奖励。 | Increments Ante; does not guarantee rewards for advancing. |
| 出牌 +1 / +1 Hand | 增加一次剩余出牌次数。 | Adds one remaining hand. |
| 弃牌 +1 / +1 Discard | 增加一次剩余弃牌次数。 | Adds one remaining discard. |
| 重掷 Boss / Boss Reroll | 在有盲注选择界面的适用状态调用 Boss 重掷。 | Calls Boss reroll when the run has an applicable blind-selection screen. |
| 筹码 +10、倍率 +10、筹码 ×2、倍率 ×10 | 修改当前出牌计分面板数值，不等于直接修改本盲注累计分数；效果取决于结算时机。 | Changes the current hand's scoring-panel values, not directly the blind's accumulated score; effects depend on scoring timing. |
| 重置筹码倍率 / Reset | 将当前出牌面板的筹码与倍率都设为零。 | Sets both current hand scoring-panel values to zero. |
| 赢下本局 / Win this Run | 在牌局中触发获胜逻辑。 | Triggers the win logic during a run. |
| 输掉本局 / Lose this Run | 将当前牌局切换到失败状态。 | Switches the active run to game over. |
| 切换背景 / Background | 切换调试背景显示。 | Toggles the debug background display. |
| 金宝显示 / Jimbo | 切换调试金宝角色的显示状态。 | Cycles the debug Jimbo character's display states. |
| 金宝说话 / Jimbo talk | 已显示调试金宝时，触发其对话动画。 | Triggers dialogue animation when debug Jimbo is present. |

## 7. 常见问题与恢复 / Troubleshooting and restore

| 问题 / Problem | 中文处理方法 | English solution |
|---|---|---|
| 仍出现黑色控制台 / Black console still appears | 确认实际启动的 EXE 内 `conf.lua` 为 `t.console = false`，不是另一份游戏副本；完全退出后再启动。 | Check the EXE actually being launched contains `t.console = false`; ensure you did not patch another copy. Fully exit and relaunch. |
| Tab 没反应 / Tab does nothing | 确认 EXE 根目录的配置包含 `_RELEASE_MODE = false`，游戏窗口已获得键盘焦点，且不是只把文件放在 EXE 旁边。 | Confirm the config at the archive root has `_RELEASE_MODE = false`, the game has keyboard focus, and the file was not merely placed beside the EXE. |
| 菜单仍是英文 / Labels remain English | 单独替换配置不会汉化。应用方式 B，或按第 5 节修改界面脚本。 | Config alone does not translate labels. Apply Option B or edit the UI script as described in Section 5. |
| 中文方块或不显示 / Missing Chinese glyphs | 切换游戏语言为简体中文，再重新打开菜单。 | Select Simplified Chinese in game and reopen the menu. |
| 按 3 不生成 / Spawn does nothing | 需要在有当前牌局区域的状态、菜单里悬停小丑牌或消耗牌，并确保对应槽位未满。 | Hover a Joker or consumable in a collection overlay, ensure its current-run area exists and has room. |
| 补丁提示不兼容 / Unsupported text | 当前版本或其他修改改变了菜单文案。先恢复原版 EXE，再核对游戏版本；不要强行替换未知代码。 | The version or another edit changed menu strings. Restore the original EXE and check the version before attempting another patch. |
| 想完全还原 / Full restore | 退出游戏，把备份的完整原 EXE 复制回 `Balatro.exe`；也可使用 Steam 的验证游戏文件功能恢复官方文件。 | Exit the game and restore the full original EXE backup as `Balatro.exe`, or use Steam's file verification to restore official files. |

只把 `_RELEASE_MODE` 改为 `true` 会关闭调试快捷键，但不会撤销收藏解锁、发现或已经写入存档的变化；这些需恢复操作前的存档备份。

Setting `_RELEASE_MODE` back to `true` disables debug shortcuts but does not undo collection unlocks, discoveries, or changes already saved. Restore a pre-edit save backup to undo those.

## 8. 开发与授权 / Development and license

```powershell
python -m unittest discover -s tests -v
```

测试检查 EXE 前缀、其他压缩条目与备份内容保留，检查只读检查模式、重复应用、不兼容输入，以及替换失败时的原文件保留。测试不需要游戏资源。

Tests verify executable-prefix, unrelated-entry and backup preservation, read-only checks, repeated application, unsupported inputs, and original-file preservation when replacement fails. No game assets are required.

本项目原创配置、补丁工具与说明按 [MIT License](LICENSE) 提供。Balatro 的原始代码、名称及资源权利归对应权利人。本项目与 LocalThunk、Playstack 无隶属关系。

This project's original configuration, patching utility, and documentation are provided under the [MIT License](LICENSE). Rights to Balatro's original code, name, and assets remain with their respective owners. This project is not affiliated with LocalThunk or Playstack.
