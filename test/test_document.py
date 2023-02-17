import unittest
import os
import shutil

from pysearch import documentHandler

class DocumentTests(unittest.TestCase):

    def setUp(self):
        # Set up environment for testing
        super(DocumentTests, self).setUp()
        self.base = os.path.join(os.getcwd(), "document_tests")
        shutil.rmtree(self.base, ignore_errors=True)
        self.handler = documentHandler.DocumentHandler(self.base)

    def tearDown(self):
        # Tear down the environment after testing
        shutil.rmtree(self.base, ignore_errors=True)
        super(DocumentTests, self).tearDown()

    def test_set_name_docs(self):
        path_prefix = os.path.join(self.base, 'documents')
        self.assertEqual(self.handler.set_name_docs(
            'hello'), os.path.join(path_prefix, '5d4140', 'hello.json'))
        self.assertEqual(self.handler.set_name_docs(
            'world'), os.path.join(path_prefix, '7d7930', 'world.json'))
        self.assertEqual(self.handler.set_name_docs(
            'truly'), os.path.join(path_prefix, 'f499b3', 'truly.json'))
        self.assertEqual(self.handler.set_name_docs(
            'splendid'), os.path.join(path_prefix, '291e4e', 'splendid.json'))
        self.assertEqual(self.handler.set_name_docs(
            'example'), os.path.join(path_prefix, '1a79a4', 'example.json'))
        self.assertEqual(self.handler.set_name_docs(
            'some'), os.path.join(path_prefix, '03d59e', 'some.json'))

    def test_save_document(self):
        raw_doc = self.handler.set_name_docs('hello')
        self.assertFalse(os.path.exists(raw_doc))

        self.assertTrue(self.handler.save_document('hello', {'abc': [1, 5]})==None)
        self.assertTrue(os.path.exists(raw_doc))

        with open(raw_doc, 'r') as raw_doc_file:
            self.assertEqual(raw_doc_file.read(), '{"abc": [1, 5]}')

    def test_load_document(self):
        raw_doc = self.handler.set_name_docs('hello')
        self.assertFalse(os.path.exists(raw_doc))
        os.makedirs(os.path.dirname(raw_doc))

        with open(raw_doc, 'w') as raw_doc_file:
            raw_doc_file.write('{"bcd": [3, 4], "abc": [1, 5]}\n')

        self.assertTrue(os.path.exists(raw_doc))

        # Should load the correct document data.
        self.assertEqual(self.handler.load_document(
            'hello'), {'abc': [1, 5], 'bcd': [3, 4]})
