"""Patch a locally owned Balatro EXE. Python 3.9+, standard library only.

Never distributes game files. Replaces conf.lua and translates only the built-in
debug menu. Creates a full local backup before an atomic replacement.
"""
import argparse
import copy
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
UI_PATH = 'functions/UI_definitions.lua'


def translate_ui(source, translations):
    start = source.index('function create_UIBox_debug_tools()')
    end = source.index('\nfunction create_UIBox_notify_alert', start)
    menu = source[start:end]
    for english, chinese in translations.items():
        old = json.dumps(english, ensure_ascii=False)
        new = json.dumps(chinese, ensure_ascii=False)
        if menu.count(old) == 1 and menu.count(new) == 0:
            menu = menu.replace(old, new)
        elif menu.count(old) == 0 and menu.count(new) == 1:
            continue
        else:
            raise ValueError('Unsupported or ambiguous menu text: ' + english)
    return source[:start] + menu + source[end:]


def patch_game(exe, check_only=False):
    exe = Path(exe).resolve(strict=True)
    translations = json.loads((ROOT / 'translations.json').read_text(encoding='utf-8'))
    conf = (ROOT / 'conf.lua').read_bytes()
    candidate = None
    backup = None
    with exe.open('rb') as f:
        if f.read(2) != b'MZ':
            raise ValueError('Expected a Windows PE executable (MZ header).')
    try:
        with zipfile.ZipFile(exe) as src:
            infos = src.infolist()
            names = src.namelist()
            if not infos or len(names) != len(set(names)):
                raise ValueError('Empty archive or duplicate ZIP entries.')
            original_ui = src.read(UI_PATH).decode('utf-8')
            translated = translate_ui(original_ui, translations).encode('utf-8')
            src.read('conf.lua')
            prefix_size = min(i.header_offset for i in infos)
            if prefix_size < 2:
                raise ValueError('Missing executable prefix.')
            if check_only:
                return {'compatible': True, 'menu_labels': len(translations), 'modified': False}
            changes = {'conf.lua': conf, UI_PATH: translated}
            if all(src.read(name) == data for name, data in changes.items()):
                return {'compatible': True, 'modified': False, 'already_applied': True}
            with exe.open('rb') as f:
                prefix = f.read(prefix_size)
            fd, name = tempfile.mkstemp(prefix='balatro-zh-', suffix='.tmp', dir=exe.parent)
            os.close(fd)
            candidate = Path(name)
            with candidate.open('wb') as f:
                f.write(prefix)
                with zipfile.ZipFile(f, 'w') as dst:
                    dst.comment = src.comment
                    for info in infos:
                        data = changes[info.filename] if info.filename in changes else src.read(info.filename)
                        dst.writestr(copy.copy(info), data)
            with zipfile.ZipFile(candidate) as checked:
                if checked.testzip() is not None or checked.namelist() != names:
                    raise ValueError('ZIP integrity check failed.')
                for info in infos:
                    expected = changes[info.filename] if info.filename in changes else src.read(info.filename)
                    if checked.read(info.filename) != expected:
                        raise ValueError('Content verification failed: ' + info.filename)
            with candidate.open('rb') as f:
                if f.read(prefix_size) != prefix:
                    raise ValueError('Executable prefix changed.')
        # Source handles must be closed before replacing a Windows executable.
        stamp = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
        backup = exe.with_name(exe.name + '.before-debug-zh-' + stamp + '.bak')
        shutil.copy2(exe, backup)
        os.replace(candidate, exe)
        candidate = None
        return {'compatible': True, 'modified': True, 'menu_labels': len(translations), 'backup': str(backup)}
    finally:
        if candidate is not None and candidate.exists():
            candidate.unlink()


def main():
    parser = argparse.ArgumentParser(description='Balatro Chinese debug menu patch / 中文调试菜单补丁')
    parser.add_argument('--exe', required=True, help='Path to your Balatro.exe / 游戏 EXE 路径')
    parser.add_argument('--check', action='store_true', help='Check compatibility without writing / 只检查，不修改')
    args = parser.parse_args()
    try:
        result = patch_game(args.exe, args.check)
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as exc:
        parser.exit(1, 'Failed / 失败: ' + str(exc) + '\nClose the game and check the EXE path/version. / 请退出游戏并检查路径和版本。\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
