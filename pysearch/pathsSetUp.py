import os
import json

__version__ = (1, 0, 0)

class PathSetUp(object):

    def __init__(self, base_directory) -> None:
        """Initialize the folders

        Args:
            base_directory (_type_): The base directory where you want to put all the data
        """
        self.base_directory = base_directory
        self.index_path = os.path.join(self.base_directory, 'index')
        self.docs_path = os.path.join(self.base_directory, 'documents')
        self.stats_path = os.path.join(self.base_directory, 'stats.json')
        self.setup()

    def setup(self) -> bool:
        """Create various data directories.

        Returns:
            bool: return True if success
        """
        if not os.path.exists(self.base_directory):
            os.makedirs(self.base_directory)

        if not os.path.exists(self.index_path):
            os.makedirs(self.index_path)

        if not os.path.exists(self.docs_path):
            os.makedirs(self.docs_path)

        if os.path.exists(self.base_directory) and os.path.exists(self.index_path) and os.path.exists(self.docs_path):
            return True

        return False

    def read_stats(self):
        """
        Reads the index-wide stats.
        """
        if not os.path.exists(self.stats_path):
            return {
                'version': '.'.join([str(bit) for bit in __version__]),
                'total_docs': 0,
            }

        with open(self.stats_path, 'r') as stats_file:
            return json.load(stats_file)

    def write_stats(self, new_stats):
        """
        Writes the index-wide stats.

        Takes a ``new_stats`` parameter, which should be a dictionary of
        stat data. Example stat data::

            {
                'version': '1.0.0',
                'total_docs': 25,
            }
        """
        with open(self.stats_path, 'w') as stats_file:
            json.dump(new_stats, stats_file)
        return True

    def increment_total_docs(self):
        """
        Increments the total number of documents the index is aware of.

        This is important for scoring reasons & is typically called as part
        of the indexing process.
        """
        current_stats = self.read_stats()
        current_stats.setdefault('total_docs', 0)
        current_stats['total_docs'] += 1
        self.write_stats(current_stats)

    def get_total_docs(self):
        """
        Returns the total number of documents the index is aware of.
        """
        current_stats = self.read_stats()
        return int(current_stats.get('total_docs', 0))


if __name__ == '__main__':
    PathSetUp(os.path.join(os.getcwd(), "SearchData"))
