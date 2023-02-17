from pathsSetUp import PathSetUp
import tokenization
import os
import json

        

def _set_name(doc_id):
    """
    Constructs a path where the document should be stored from doc_id
    """
    return os.path.join(PathSetUp.docs_path, tokenization.hash_name(doc_id), f"{doc_id}.json")

def save_document(doc_id, document):
    """
    Save the document
    """
    doc_path = _set_name(doc_id)
    base_path = os.path.dirname(doc_path)

    if not os.path.exists(base_path):
        os.makedirs(base_path)

    with open(doc_path, 'w') as doc_file:
        doc_file.write(json.dumps(document, ensure_ascii=False))

def load_document(doc_id):
    doc_path = _set_name(doc_id)

    with open(doc_path, 'r') as doc_file:
        data = json.loads(doc_file.read())

    return data

