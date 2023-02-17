from segmentHandler import SegmentHandler
from documentHandler import DocumentHandler
import math
import tokenization
import os


def bm25_relevance(terms, matches, current_doc, total_docs, b=0, k=1.2):
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


class PySearch(DocumentHandler, SegmentHandler):

    def __init__(self, base_directory) -> None:
        super().__init__(base_directory)

    def index(self, doc_id, document):
        """
        Given a ``doc_id`` string & a ``document`` dict, does everything needed
        to save & index the document for searching.

        The ``document`` dict must have a ``text`` key, which should contain the
        blob to be indexed. All other fields are simply stored.

        Returns ``True`` on success.
        """
        # Ensure that the ``document`` looks like a dictionary.
        if not hasattr(document, 'items'):
            raise AttributeError(
                'You must provide `index` with a document in the form of a dictionary.')

        # For example purposes, we only index the ``text`` field.
        if 'text' not in document:
            raise KeyError(
                'You must provide `index` with a document with a `text` field in it.')

        # Make sure the document ID is a string.

        # store docs
        doc_id = str(doc_id)
        self.save_document(doc_id, document)

        # store segments
        # Start analysis & indexing.
        tokens = tokenization.make_tokens(document.get('text', ''))
        terms = tokenization.make_ngrams(tokens)

        for term, positions in terms.items():
            self.save_segment(term, {doc_id: positions})

        self.increment_total_docs()
        return True

    def __parse_query(self, query: str):
        """
        Convert query to terms for searching
        """
        tokens = tokenization.make_tokens(query)
        return tokenization.make_ngrams(tokens)

    def __collect_results(self, terms):
        """
        For a list of ``terms``, collects all the documents from the index
        containing those terms.

        The returned data is a tuple of two dicts. This is done to make the
        process of scoring easy & require no further information.

        The first dict contains all the terms as keys & a count (integer) of
        the matching docs as values.

        The second dict inverts this, with ``doc_ids`` as the keys. The values
        are a nested dict, which contains the ``terms`` as the keys and a
        count of the number of positions within that doc.

        Since this is complex, an example return value::

            >>> per_term_docs, per_doc_counts = ms.collect_results(['hello', 'world'])
            >>> per_term_docs
            {
                'hello': 2,
                'world': 1
            }
            >>> per_doc_counts
            {
                'doc-1': {
                    'hello': 4
                },
                'doc-2': {
                    'hello': 1,
                    'world': 3
                }
            }

        """
        per_term_docs = {}
        per_doc_counts = {}

        for term in terms:
            term_matches = self.load_segment(term)

            per_term_docs.setdefault(term, 0)
            per_term_docs[term] += len(term_matches.keys())

            for doc_id, positions in term_matches.items():
                per_doc_counts.setdefault(doc_id, {})
                per_doc_counts[doc_id].setdefault(term, 0)
                per_doc_counts[doc_id][term] += len(positions)

        return per_term_docs, per_doc_counts


    def search(self, query, offset=0, limit=20):
        """
        Given a ``query``, performs a search on the index & returns the results.

        Optionally accepts an ``offset`` parameter, which is an integer &
        controls what the starting point in the results is. Default is ``0``
        (the beginning).

        Optionally accepts a ``limit`` parameter, which is an integer &
        controls how many results to return. Default is ``20``.

        Returns a dictionary containing the ``total_hits`` (integer), which is
        a count of all the documents that matched, and ``results``, which is
        a list of results (in descending ``score`` order) & sliced to the
        provided ``offset/limit`` combination.
        """
        results = {
            'total_hits': 0,
            'results': []
        }

        if not len(query):
            return results

        total_docs = self.get_total_docs()

        if total_docs == 0:
            return results

        terms = self.__parse_query(query)
        per_term_docs, per_doc_counts = self.__collect_results(terms)
        scored_results = []

        # Score the results per document.
        for doc_id, current_doc in per_doc_counts.items():
            scored_results.append({
                'id': doc_id,
                'score': bm25_relevance(terms, per_term_docs, current_doc, total_docs),
            })

        # Sort based on score.
        sorted_results = sorted(scored_results, key=lambda res: res['score'], reverse=True)
        results['total_hits'] = len(sorted_results)

        # Slice the results.
        sliced_results = sorted_results[offset:offset + limit]

        # For each result, load up the doc & update the dict.
        for res in sliced_results:
            doc_dict = self.load_document(res['id'])
            doc_dict.update(res)
            results['results'].append(doc_dict)

        return results


if __name__ == '__main__':
    engine = PySearch(os.path.join(os.getcwd(), "SearchData"))

    # Index some data.
    engine.index('email_1', {
             'text': "Peter,\n\nI'm going to need those TPS reports on my desk first thing tomorrow! And clean up your desk!\n\nLumbergh"})
    engine.index('email_2', {
             'text': 'Everyone,\n\nM-m-m-m-my red stapler has gone missing. H-h-has a-an-anyone seen it?\n\nMilton'})
    engine.index('email_3', {
             'text': "Peter,\n\nYeah, I'm going to need you to come in on Saturday. Don't forget those reports.\n\nLumbergh"})
    engine.index(
        'email_4', {'text': 'How do you feel about becoming Management?\n\nThe Bobs'})

    print(engine.search('Peter'))



