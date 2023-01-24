from __future__ import annotations


class ChainTrace:
    """
    ChainTrace is a data structure that is used to store the trace of a interaction with a language model.
    """

    __type_of_nodes = ["base_prompt", "thought", "action", "observation", "finish"]
    __color_mapping = {
        "base_prompt": "white",
        "thought": "blue",
        "action": "red",
        "observation": "yellow",
        "finish": "green",
    }

    def __init__(self, data: str, type_of_node: str, depth: int = 0) -> None:
        """
        Constructor of the ChainTrace class

        :param data: data of the node
        :param type_of_node: type of the node
        :param depth: depth of the node
        """
        assert (
            type_of_node in self.__type_of_nodes
        ), f"Type of node must be one of {self.__type_of_nodes}"
        self.type_of_node = type_of_node
        self.depth = depth
        self.next = None
        self.data = data
        self.is_leaf = False
        if self.type_of_node == "finish":
            self.is_leaf = True

    def add(self, data: str, type_of_node: str) -> None:
        """
        Add a new node to the chain trace.

        :param data: data of the node
        :param type_of_node: type of the node
        :return: None
        """
        if self.is_leaf:
            raise Exception("Cannot add to a leaf node")
        if self.next is None:
            self.next = ChainTrace(data, type_of_node, self.depth + 1)
        else:
            self.next.add(data, type_of_node)

    def compose(self) -> str:
        """
        Compose the chain trace into a string.
        :return: Composed chaine trace data.
        """
        if self.is_leaf or self.next is None:
            return self.data
        else:
            return self.data + self.next.compose()

    def to_json(self) -> list:
        """
        Prepare chain trace to json format.

        :return: List of node dictionaries.
        """
        if self.is_leaf or self.next is None:
            return [{"type": self.type_of_node, "data": self.data}]
        else:
            return [
                {"type": self.type_of_node, "data": self.data}
            ] + self.next.to_json()

    def get_max_depth(self) -> int:
        """
        Get the maximum depth of the chain trace.

        :return: Maximum depth of the chain trace.
        """
        if self.is_leaf == True or self.next is None:
            return self.depth
        else:
            return self.next.get_max_depth()

    def get_deepest_node(self) -> ChainTrace:
        """
        Get the deepest node of the chain trace.

        :return: Deepest node of the chain trace.
        """
        if self.next is None:
            return self
        else:
            return self.next.get_deepest_node()

    def __str__(self) -> str:
        """
        Compose chain trace into a string with colored sections.
        :return: Composed chain trace data.
        """
        trace = ""
        trace += colored(
            f"[{self.type_of_node}] " + self.data,
            self.__color_mapping[self.type_of_node],
        )
        while self.next is not None:
            self = self.next
            trace += colored(
                f"[{self.type_of_node}] " + self.data,
                self.__color_mapping[self.type_of_node],
            )
        return trace

    def __len__(self) -> int:
        return len(self.compose())


def colored(st: str, color: str) -> str:
    """
    Color a string with a specified color.

    :param st: String to color.
    :param color: Color to use.
    :return: Colored string.
    """
    return f"\u001b[{30 + ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'].index(color)}m{st}\u001b[0m"
