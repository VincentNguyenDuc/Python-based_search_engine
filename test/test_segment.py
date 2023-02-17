import unittest
from pysearch import segmentHandler



class SetUpTests(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()
