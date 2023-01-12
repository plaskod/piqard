import importlib


class DatabaseLoaderFactory:
    """
    DatabaseLoaderFactory is a factory class that returns the appropriate database loader
    """

    def __init__(self, database: str):
        """
        Constructor of the DatabaseLoaderFactory class

        For proper work you need to write a file with the name convention {database}_loader.py in the data_loaders folder.
        Actually there are only two databases loaders: openbookqa and hotpotqa.

        :param database: name of the database
        """

        module = importlib.import_module(
            f".{database}_loader", package=f"piqard.data_loaders"
        )

        self.load_documents = getattr(module, f"load_documents")
        self.load_questions = getattr(module, f"load_questions")
