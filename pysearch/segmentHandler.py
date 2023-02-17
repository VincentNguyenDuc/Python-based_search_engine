import tokenization
import os
import json
from pathsSetUp import PathSetUp
import tempfile



def _parse_record(line):
    """
        Given a ``line`` from the segment file, this returns the term & its info.

        The term info is stored as serialized JSON. The default separator
        between the term & info is the ``\t`` character, which would never
        appear in a term due to the way tokenization is done.
    """
    return line.rstrip().split('\t', 1)


def _make_record(term, term_info):
    """
    Given a ``term`` and a dict of ``term_info``, creates a line for
    writing to the segment file.
    """
    return "{0}\t{1}\n".format(term, json.dumps(term_info, ensure_ascii=False))

def _update_term_info(orig_info, new_info):
    """
    Takes existing ``orig_info`` & ``new_info`` dicts & combines them
    intelligently.

    Used for updating term_info within the segments.
    """
    # Updates are (sadly) not as simple as ``dict.update()``.
    # Iterate through the keys (documents) & manually update.
    for doc_id, positions in new_info.items():
        if doc_id not in orig_info:
            # Easy case; it's not there. Shunt it in wholesale.
            orig_info[doc_id] = positions
        else:
            # Harder; it's there. Convert to sets, update then convert back
            # to lists to accommodate ``json``.
            orig_positions = set(orig_info.get(doc_id, []))
            new_positions = set(positions)
            orig_positions.update(new_positions)
            orig_info[doc_id] = list(orig_positions)

    return orig_info


class SegmentHandler(PathSetUp):

    def __init__(self, base_directory) -> None:
        super().__init__(base_directory)

    def _set_name(self, term):
        """
        creates a segment filename based on the hash of the term.

        Returns the full path to the segment.
        """
        return os.path.join(self.index_path, f"{tokenization.hash_name(term)}.index")


    def save_segment(self, term, term_info, update=False):
        """
        Writes out new index data to disk.

        Takes a ``term`` string & ``term_info`` dict. It will
        rewrite the segment in alphabetical order, adding in the data
        where appropriate.

        Optionally takes an ``update`` parameter, which is a boolean &
        determines whether the provided ``term_info`` should overwrite or
        update the data in the segment. Default is ``False`` (overwrite).
        """
        seg_name = self.make_segment_name(term)
        new_seg_file = tempfile.NamedTemporaryFile(delete=False)
        written = False

        if not os.path.exists(seg_name):
            # If it doesn't exist, touch it.
            with open(seg_name, 'w') as seg_file:
                seg_file.write('')

        with open(seg_name, 'r') as seg_file:
            for line in seg_file:
                seg_term, seg_term_info = self.parse_record(line)

                if not written and seg_term > term:
                    # We're at the alphabetical location & need to insert.
                    new_line = self.make_record(term, term_info)
                    new_seg_file.write(new_line.encode('utf-8'))
                    written = True
                elif seg_term == term:
                    if not update:
                        # Overwrite the line for the update.
                        line = self.make_record(term, term_info)
                    else:
                        # Update the existing record.
                        new_info = self.update_term_info(
                            json.loads(seg_term_info), term_info)
                        line = self.make_record(term, new_info)

                    written = True

                # Either we haven't reached it alphabetically or we're well-past.
                # Write the line.
                new_seg_file.write(line.encode('utf-8'))

            if not written:
                line = self.make_record(term, term_info)
                new_seg_file.write(line.encode('utf-8'))

        # Atomically move it into place.
        new_seg_file.close()
        try:
            os.rename(new_seg_file.name, seg_name)
        except OSError:
            os.remove(seg_name)
            os.rename(new_seg_file.name, seg_name)
        return True

    
    def load_segment(self, term:str):
        """
        Return term information associated with the term
        """
        seg_name = self._set_name(term)

        if not os.path.exists(seg_name):
            return {}

        with open(seg_name, 'r') as seg_file:
            for line in seg_file:
                seg_term, term_info = self.parse_record(line)

                if seg_term == term:
                    # Found it.
                    return json.loads(term_info)

        return {}



if __name__ == '__main__':
    pass