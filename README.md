# Balatro Debug Menu ZH

**English** | [简体中文](README.zh-CN.md)

**Enable Balatro's built-in Tab debug menu, hide the black LÖVE console, and optionally translate the menu into Simplified Chinese.**

[Download](https://github.com/RyanLiu1208/balatro-debug-menu-zh/releases/latest) · [Configuration](conf.lua) · [Translation map](translations.json)

This project contains a configuration file and a text patch. It requires no Lovely, Steamodded, or other mod loader. No game executable, full game scripts, images, saves, or game assets are distributed.

## 1. What each file does

| File | Purpose |
| --- | --- |
| [`conf.lua`](conf.lua) | Enables built-in debugging and disables the console. Includes bilingual comments. **Replacing this file alone does not translate the menu.** |
| [`translations.json`](translations.json) | Maps 27 original English menu strings to Chinese. |
| [`patch.py`](patch.py) | Optional local patcher: installs both the configuration and translation into your own EXE, backing it up before replacement. |
| [`tests/`](tests) | Tests using synthetic EXE/ZIP fixtures; no game files needed. |

`conf.lua` only controls startup settings. Menu labels live in `functions/UI_definitions.lua` inside the game. The complete Chinese menu requires changes to both files. The patcher changes the configuration and debug menu text, preserving button callbacks.

## 2. Compatibility and preparation

| Item | Description |
| --- | --- |
| Tested version | Windows Steam build `1.0.1o-FULL`; game startup and Chinese menu rendering were checked in-game. |
| Other versions | Not individually tested. The patcher refuses unsupported menu text rather than making unchecked edits. |
| Game language | Select Simplified Chinese in the game when using the translation so Chinese fonts are available. |
| Before editing | Save and fully exit the game. Back up the original EXE and saves under `%APPDATA%/Balatro`. |
| Updates | Steam updates, file verification, or restoring the original EXE may overwrite the patch. |

These are debug tools: Unlock and Discover change collection progress, and some buttons directly change the run. Learn the controls with a backup or test save.

## 3. Option A: manually replace the Lua file

No Python is needed. This enables the menu and hides the console; labels remain English unless you also apply Option B or the UI translations in Section 5.

| Step | Description |
| --- | --- |
| 1 | Select **Code → Download ZIP** on GitHub and extract this project. |
| 2 | In Steam, right-click Balatro → Manage → Browse local files, then locate `Balatro.exe`. |
| 3 | Copy the original `Balatro.exe` to a separate backup location. |
| 4 | Open the EXE as an archive with a tool that supports embedded ZIPs and find `conf.lua` at the archive root. |
| 5 | Drag this project's `conf.lua` into the archive, replace the existing file, and wait for writing to finish. Do not put it inside an extra folder. |
| 6 | Launch through Steam, hold **Tab** to show the menu, and release it to close. |

**Do not extract everything, create a regular ZIP, and rename it to EXE.** The executable has a launcher prefix that a regular ZIP cannot replace. If your archive tool cannot safely update an embedded archive, use Option B.

## 4. Option B: apply config and Chinese labels together

Requires Python 3.9 or newer and uses only the standard library: **no pip dependencies**. Extract this project and run the following from its directory. Replace the sample path with your actual game location.

First check compatibility without changing the game:

```powershell
python patch.py --exe "C:\Program Files (x86)\Steam\steamapps\common\Balatro\Balatro.exe" --check
```

Fully exit the game, then apply the patch:

```powershell
python patch.py --exe "C:\Program Files (x86)\Steam\steamapps\common\Balatro\Balatro.exe"
```

If your PC uses the `py` launcher, replace `python` with `py -3`.

On success, output includes `"modified": true` and a `backup` path. The backup sits beside the EXE with a name like `Balatro.exe.before-debug-zh-TIMESTAMP.bak`. The patcher checks ZIP integrity, preserves the executable prefix, verifies other entries, then replaces the file. Reapplying the same patch reports `"already_applied": true`.

For permission errors, first ensure the game is fully closed and the target directory is writable. Any retained `.bak` file is a recovery backup, not a game update.

## 5. Menu text

These strings belong only to the debug menu. For manual translation, locate `create_UIBox_debug_tools()` in the EXE's `functions/UI_definitions.lua` and replace only its displayed text, preserving quotes, commas, braces, and callback names. Save as UTF-8 and replace the archive entry. The automatic patcher already performs this step.

See [`translations.json`](translations.json) for all 27 original menu strings and Chinese translations.

## 6. How to use the controls

### Showing the menu

Hold **Tab** to show the menu and release it to close. Keep Tab held while clicking menu buttons. Tab displays the panel; the number shortcuts and Q do not themselves require Tab to be held.

### Unlock, Discover, and Spawn

In a collection/card overlay, hover the intended card, then press the number key. Pressing the key without a hovered card does not award a random card.

| Key | Description |
| --- | --- |
| **1 — Unlock** | Bypasses that card's unlock condition. It does not add a copy to the run or automatically mark it discovered. |
| **2 — Discover** | Unlocks and marks the card discovered so its normal collection entry is revealed. Does not give a copy to the player. |
| **3 — Spawn** | Adds the hovered Joker or consumable to the current run if its area exists and has room. Consumables include Tarot, Planet, and Spectral cards. This shortcut does not spawn ordinary playing cards or automatically grant a permanent unlock. |

Example: to obtain Blueprint, start a run, open an available collection view, hover Blueprint, and press **3**. It will not spawn if Joker slots are full. To fill collection progress without obtaining a copy, use **2**.

### Other shortcuts

| Key | Description |
| --- | --- |
| **Q** | Hover a Joker/playing card to cycle Base → Foil → Holographic → Polychrome → Negative → Base. Applicability depends on the hovered card. |
| **H** | Toggles the main UI to isolate the background; press again to restore. |
| **J** | Toggles the splash display and leaves the active run for the splash screen; this is not a harmless preview. |
| **8** | Shows/hides the mouse cursor. |
| **9** | Toggles the debug tooltip display state. |

Setting `_RELEASE_MODE = false` also enables other debug shortcuts already present in the game. This project does not remove or rewrite them; for example, **B restarts a run and L reloads the saved run**. Avoid experimenting with unrelated shortcuts during a normal run.

### Menu buttons

| Button | Purpose |
| --- | --- |
| $10 | Adds $10 to the current run. |
| +1 Round | Increments the round counter; does not simulate completing a blind. |
| +1 Ante | Increments Ante; does not guarantee rewards for advancing. |
| +1 Hand | Adds one remaining hand. |
| +1 Discard | Adds one remaining discard. |
| Boss Reroll | Calls Boss reroll when the run has an applicable blind-selection screen. |
| +10 chips / +10 mult / X2 chips / X10 mult | Changes the current hand's scoring-panel values, not directly the blind's accumulated score; effects depend on scoring timing. |
| Reset | Sets both current hand scoring-panel values to zero. |
| Win this Run | Triggers the win logic during a run. |
| Lose this Run | Switches the active run to game over. |
| Background | Toggles the debug background display. |
| Jimbo | Cycles the debug Jimbo character's display states. |
| Jimbo talk | Triggers dialogue animation when debug Jimbo is present. |

## 7. Troubleshooting and restore

| Problem | Description |
| --- | --- |
| Black console still appears | Check the EXE actually being launched contains `t.console = false`; ensure you did not patch another copy. Fully exit and relaunch. |
| Tab does nothing | Confirm the config at the archive root has `_RELEASE_MODE = false`, the game has keyboard focus, and the file was not merely placed beside the EXE. |
| Labels remain English | Config alone does not translate labels. Apply Option B or edit the UI script as described in Section 5. |
| Missing Chinese glyphs | Select Simplified Chinese in game and reopen the menu. |
| Spawn does nothing | Hover a Joker or consumable in a collection overlay, ensure its current-run area exists and has room. |
| Unsupported text | The version or another edit changed menu strings. Restore the original EXE and check the version before attempting another patch. |
| Full restore | Exit the game and restore the full original EXE backup as `Balatro.exe`, or use Steam's file verification to restore official files. |

Setting `_RELEASE_MODE` back to `true` disables debug shortcuts but does not undo collection unlocks, discoveries, or changes already saved. Restore a pre-edit save backup to undo those.

## 8. Development and license

```powershell
python -m unittest discover -s tests -v
```

Tests verify executable-prefix, unrelated-entry and backup preservation, read-only checks, repeated application, unsupported inputs, and original-file preservation when replacement fails. No game assets are required.

This project's original configuration, patching utility, and documentation are provided under the [MIT License](LICENSE). Rights to Balatro's original code, name, and assets remain with their respective owners. This project is not affiliated with LocalThunk or Playstack.
