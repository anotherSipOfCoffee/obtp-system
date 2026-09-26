"""Visibility must partition real model parts without modifying model outputs."""
import copy
import unittest
from collections import Counter
from obtp.model import build, parameters
from obtp.preview_filter import GROUPS, category, visible

class PreviewFilterTests(unittest.TestCase):
    def test_real_presets(self):
        for program in (0, 1):
            for preset in range(6):
                scene=build(parameters(preset_index=preset,program_type=program))
                before=copy.deepcopy(scene)
                counts=Counter(category(p) for p in scene['parts'])
                self.assertNotIn('other',counts)
                self.assertEqual(sum(counts.values()),len(scene['parts']))
                self.assertTrue(all(visible(p) for p in scene['parts']))
                off={key:False for key,label in GROUPS}
                self.assertFalse(any(visible(p,off) for p in scene['parts']))
                for i,(key,label) in enumerate(GROUPS,1):
                    selected=[p for p in scene['parts'] if visible(p,off,i)]
                    self.assertEqual(len(selected),counts[key])
                    self.assertFalse(any(visible(p,{key:False}) for p in selected))
                self.assertEqual(scene,before)

if __name__=='__main__':unittest.main()
