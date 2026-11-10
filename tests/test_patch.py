"""Synthetic fixtures only. No game code or assets required."""
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from unittest.mock import patch
import patch as app


class PatchTests(unittest.TestCase):
    def make_game(self, root, compatible=True):
        exe = Path(root) / 'Balatro.exe'
        prefix = b'MZ' + b'original-executable-prefix' * 10
        labels = json.loads((app.ROOT/'translations.json').read_text(encoding='utf-8'))
        literals = '\n'.join('text = ' + json.dumps(s) for s in labels)
        if not compatible:
            literals = literals.replace('Boss Reroll', 'Changed Boss Label')
        ui = 'unrelated-prefix\nfunction create_UIBox_debug_tools()\n' + literals + '\nend\nfunction create_UIBox_notify_alert()\nunchanged-tail'
        with exe.open('wb') as f:
            f.write(prefix)
            with zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED) as z:
                z.writestr('conf.lua', 'original-conf')
                z.writestr(app.UI_PATH, ui)
                z.writestr('asset.bin', bytes(range(256)))
        return exe, prefix, ui

    def test_preserves_prefix_assets_backup_and_ui_outside_menu(self):
        with tempfile.TemporaryDirectory() as d:
            exe,prefix,ui = self.make_game(d)
            before = exe.read_bytes()
            result = app.patch_game(exe)
            self.assertTrue(result['modified'])
            self.assertEqual(Path(result['backup']).read_bytes(), before)
            self.assertTrue(exe.read_bytes().startswith(prefix))
            with zipfile.ZipFile(exe) as z:
                self.assertIsNone(z.testzip())
                self.assertEqual(z.read('asset.bin'), bytes(range(256)))
                text=z.read(app.UI_PATH).decode('utf-8')
                self.assertTrue(text.startswith('unrelated-prefix\n'))
                self.assertTrue(text.endswith('unchanged-tail'))
                self.assertIn('重掷 Boss', text)
                self.assertEqual(z.read('conf.lua'), (app.ROOT/'conf.lua').read_bytes())

    def test_check_does_not_write(self):
        with tempfile.TemporaryDirectory() as d:
            exe,_,_ = self.make_game(d)
            before=exe.read_bytes()
            self.assertFalse(app.patch_game(exe,True)['modified'])
            self.assertEqual(before, exe.read_bytes())
            self.assertEqual(len(list(Path(d).iterdir())),1)

    def test_repeat_is_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            exe,_,_ = self.make_game(d)
            app.patch_game(exe)
            before=exe.read_bytes()
            self.assertTrue(app.patch_game(exe)['already_applied'])
            self.assertEqual(before,exe.read_bytes())
            self.assertEqual(len(list(Path(d).glob('*.bak'))),1)

    def test_unknown_version_fails_before_modifying(self):
        with tempfile.TemporaryDirectory() as d:
            exe,_,_ = self.make_game(d,False)
            before=exe.read_bytes()
            with self.assertRaises(ValueError):app.patch_game(exe)
            self.assertEqual(before,exe.read_bytes())
            self.assertEqual(len(list(Path(d).iterdir())),1)

    def test_failed_replacement_keeps_original_and_removes_temp(self):
        with tempfile.TemporaryDirectory() as d:
            exe,_,_ = self.make_game(d)
            before=exe.read_bytes()
            with patch.object(app.os,'replace',side_effect=PermissionError('locked')):
                with self.assertRaises(PermissionError):app.patch_game(exe)
            self.assertEqual(before,exe.read_bytes())
            self.assertEqual(list(Path(d).glob('*.tmp')),[])


if __name__=='__main__':unittest.main()
