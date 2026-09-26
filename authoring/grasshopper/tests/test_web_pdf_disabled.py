import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import export_web


class PDFDisabledTests(unittest.TestCase):
    def test_default_export_skips_pdf_work_and_retains_models_and_plans(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder)
            (target / 'previous-revision.pdf').write_bytes(b'old PDF')
            combinations = [[(0, 0, 0, 2, 580, True, 0),
                             (1, 0, 0, 2, 580, False, 0)], [(0, 0), (1, 0)]]
            def model_file(scenes, path):
                path.write_bytes(b'Rhino export fixture')
            with patch.object(export_web.itertools, 'product', side_effect=combinations), \
                 patch.object(export_web, 'write_pdf_documents', side_effect=AssertionError('PDF generation invoked')), \
                 patch.object(export_web, 'file3dm', side_effect=model_file) as models:
                export_web.compile_catalogue(target, 'test-revision')
            manifest = json.loads((target / 'manifest.json').read_text())
            self.assertFalse(manifest['pdf_enabled'])
            self.assertEqual(len(manifest['entries']), 2)
            self.assertEqual(models.call_count, 2)
            self.assertEqual(list(target.glob('*.pdf')), [])
            for entry in manifest['entries']:
                self.assertFalse(entry['pdf'])
                self.assertTrue((target / entry['file']).is_file())
                self.assertTrue((target / (entry['key'] + '-plan.svg')).is_file())
            with zipfile.ZipFile(target / 'OBTP_Grasshopper_R12.zip') as package:
                self.assertEqual(len([n for n in package.namelist() if n.endswith('.3dm')]), 2)
                self.assertFalse(any(n.endswith('.pdf') for n in package.namelist()))


if __name__ == '__main__':
    unittest.main()
