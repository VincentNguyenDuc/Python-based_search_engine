import os


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


if __name__ == '__main__':
    PathSetUp(os.path.join(os.getcwd(), "SearchData"))
