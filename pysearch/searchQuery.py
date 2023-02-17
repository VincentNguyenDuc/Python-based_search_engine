from segmentHandler import SegmentHandler
from documentHandler import DocumentHandler
import math
import tokenization


class SearchQuery(DocumentHandler, SegmentHandler):

    def __init__(self, base_directory) -> None:
        super().__init__(base_directory)

    def index(self, doc_id, document):
        pass

    def parse_query(self, query):
        tokens = tokenization.make_tokens(query)
        return tokenization.make_ngrams(tokens)

    def collect_results(self, terms):
        pass

    def bm25_relevance(self, terms, matches, current_doc, total_docs, b=0, k=1.2):
        """
        Given multiple inputs, performs a BM25 relevance calculation for a
        given document.

        ``terms`` should be a list of terms.

        ``matches`` should be the first dictionary back from
        ``collect_results``.

        ``current_doc`` should be the second dictionary back from
        ``collect_results``.

        ``total_docs`` should be an integer of the total docs in the index.

        Optionally accepts a ``b`` parameter, which is an integer specifying
        the length of the document. Since it doesn't vastly affect the score,
        the default is ``0``.

        Optionally accepts a ``k`` parameter. It accepts a float & is used to
        modify scores to fall into a given range. With the default of ``1.2``,
        scores typically range from ``0.4`` to ``1.0``.
        """
        # More or less borrowed from http://sphinxsearch.com/blog/2010/08/17/how-sphinx-relevance-ranking-works/.
        score = b

        for term in terms:
            idf = math.log(
                (total_docs - matches[term] + 1.0) / matches[term]) / math.log(1.0 + total_docs)
            score = score + \
                current_doc.get(term, 0) * idf / (current_doc.get(term, 0) + k)

        return 0.5 + score / (2 * len(terms))

    def search(self, query, offset=0, limit=20):
        pass
