class ChainTrace:
    __type_of_nodes = ['base_prompt', 'thought', 'action', 'observation', 'finish']
    __color_mapping = {'base_prompt': 'white', 'thought': 'blue', 'action': 'red', 'observation': 'yellow',
                       'finish': 'green'}

    def __init__(self, data: str, type_of_node: str, depth: int = 0) -> None:
        assert type_of_node in self.__type_of_nodes, f"Type of node must be one of {self.__type_of_nodes}"
        self.type_of_node = type_of_node
        self.depth = depth
        if self.depth == 0:
            assert self.type_of_node == 'base_prompt', f"Type of node must be 'base_prompt' for depth 0"
        self.next = None
        self.data = data
        self.is_leaf = False
        if self.type_of_node == 'finish':
            self.is_leaf = True

    def add(self, data: str, type_of_node: str) -> None:
        if self.is_leaf:
            raise Exception("Cannot add to a leaf node")
        if self.next is None:
            self.next = ChainTrace(data, type_of_node, self.depth + 1)
        else:
            self.next.add(data, type_of_node)

    def compose(self) -> str:
        if self.is_leaf or self.next is None:
            return self.data
        else:
            return self.data + self.next.compose()

    def get_max_depth(self) -> int:
        if self.is_leaf == True or self.next is None:
            return self.depth
        else:
            return self.next.get_max_depth()

    def get_deepest_node(self):
        if self.next is None:
            return self
        else:
            return self.next.get_deepest_node()

    def __str__(self) -> str:
        trace = ''
        trace += self.data
        while self.next is not None:
            self = self.next
            trace += self.data
        return trace

    def __len__(self) -> int:
        return len(self.compose())
