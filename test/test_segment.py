import unittest
from pysearch import segmentHandler
import os
import shutil



class SegmentsTests(unittest.TestCase):

    def setUp(self):
        # Set up environment for testing
        super(SegmentsTests, self).setUp()
        self.base = os.path.join(os.getcwd(), "segment_tests")
        shutil.rmtree(self.base, ignore_errors=True)
        self.handler = segmentHandler.SegmentHandler(self.base)

    def tearDown(self):
        # Tear down the environment after testing
        shutil.rmtree(self.base, ignore_errors=True)
        super(SegmentsTests, self).tearDown()


    def test_parse_record(self):
        self.assertEqual(segmentHandler._parse_record('hello\t{"abc": [1, 2, 3]}\n'), ['hello', '{"abc": [1, 2, 3]}'])

    def test_make_record(self):
        self.assertEqual(segmentHandler._make_record('hello', {"abc": [1, 2, 3]}), 'hello\t{"abc": [1, 2, 3]}\n')

    def test_update_term_info(self):
        orig = {
            "abc": [1, 2, 3],
            "ab": [2],
        }
        new = {
            "abc": [2, 1, 5],
            "bcd": [2, 3],
            "ghi": [25],
        }
        self.assertEqual(segmentHandler._update_term_info(orig, new), {
            'ab': [2],
            'abc': [1, 2, 3, 5],
            'bcd': [2, 3],
            'ghi': [25]
        })

    def test_set_name_seg(self):
        path_prefix = os.path.join(os.getcwd(), 'segment_tests', 'index')
        self.assertEqual(self.handler.set_name_seg('hello'), os.path.join(path_prefix,'5d4140.index' ))
        self.assertEqual(self.handler.set_name_seg('world'), os.path.join(path_prefix, '7d7930.index'))
        self.assertEqual(self.handler.set_name_seg('truly'), os.path.join(path_prefix, 'f499b3.index'))
        self.assertEqual(self.handler.set_name_seg('splendid'), os.path.join(path_prefix, '291e4e.index'))
        self.assertEqual(self.handler.set_name_seg('example'), os.path.join(path_prefix, '1a79a4.index'))
        self.assertEqual(self.handler.set_name_seg('some'), os.path.join(path_prefix, '03d59e.index'))
        self.assertEqual(self.handler.set_name_seg('tokens'), os.path.join(path_prefix, '25d718.index'))
        self.assertEqual(self.handler.set_name_seg('top'), os.path.join(path_prefix, 'b28354.index'))
        self.assertEqual(self.handler.set_name_seg('notch'), os.path.join(path_prefix, '9ce862.index'))
        self.assertEqual(self.handler.set_name_seg('really'), os.path.join(path_prefix, 'd2d92e.index'))

    def test_save_segment(self):
        raw_index = self.handler.set_name_seg('hello')
        self.assertFalse(os.path.exists(raw_index))

        self.assertTrue(self.handler.save_segment('hello', {'abc': [1, 5]}))
        self.assertTrue(os.path.exists(raw_index))

        with open(raw_index, 'r') as raw_index_file:
            self.assertEqual(raw_index_file.read(), 'hello\t{"abc": [1, 5]}\n')

        self.assertTrue(self.handler.save_segment(
            'hello', {'abc': [1, 5], 'bcd': [3, 4]}))
        self.assertTrue(os.path.exists(raw_index))

        with open(raw_index, 'r') as raw_index_file:
            self.assertEqual(raw_index_file.read(),
                             'hello\t{"abc": [1, 5], "bcd": [3, 4]}\n')

    def test_load_segment(self):
        raw_index = self.handler.set_name_seg('hello')
        self.assertFalse(os.path.exists(raw_index))

        # Shouldn't fail if it's not there.
        self.assertEqual(self.handler.load_segment('hello'), 'segment not exist')

        with open(raw_index, 'w') as raw_index_file:
            raw_index_file.write('hello\t{"bcd": [3, 4], "abc": [1, 5]}\n')

        self.assertTrue(os.path.exists(raw_index))

        # Should load the correct term data.
        self.assertEqual(self.handler.load_segment('hello'),
                         {'abc': [1, 5], 'bcd': [3, 4]})

        # Won't hash to the same file & since we didn't put the data there,
        # it fails to lookup.
        self.assertEqual(self.handler.load_segment('binary'), 'segment not exist')

if __name__ == '__main__':
    unittest.main()
