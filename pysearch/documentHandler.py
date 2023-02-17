from pathsSetUp import PathSetUp
import tokenization
import os
import json


class DocumentHandler(PathSetUp):
    def __init__(self, base_directory) -> None:
        super().__init__(base_directory)

    def set_name_docs(self, doc_id):
        """
        Constructs a path where the document should be stored from doc_id
        """
        return os.path.join(self.docs_path, tokenization.hash_name(doc_id), f"{doc_id}.json")

    def save_document(self, doc_id, document):
        """
        Save the document
        """
        doc_path = self.set_name_docs(doc_id)
        base_path = os.path.dirname(doc_path)

        if not os.path.exists(base_path):
            os.makedirs(base_path)

        with open(doc_path, 'w') as doc_file:
            doc_file.write(json.dumps(document, ensure_ascii=False))

    def load_document(self, doc_id):
        doc_path = self.set_name_docs(doc_id)

        with open(doc_path, 'r') as doc_file:
            data = json.loads(doc_file.read())

        return data


if __name__ == '__main__':
    dh = DocumentHandler(os.path.join(os.getcwd(), "SearchData"))
    dh.save_document('100', {1:2})
    print(dh.load_document('100'))

