import pytest
from piqard.utils.chain_trace import ChainTrace


class TestChainTrace:
    def test_init(self):
        # Test the initialisation of ChainTrace
        chain_trace = ChainTrace("base_prompt", "base_prompt", 0)
        assert chain_trace.data == "base_prompt"
        assert chain_trace.type_of_node == "base_prompt"
        assert chain_trace.depth == 0
        assert chain_trace.next is None
        assert chain_trace.is_leaf is False

    def test_add(self):
        # Test the add method of ChainTrace
        chain_trace = ChainTrace("base_prompt", "base_prompt", 0)
        chain_trace.add("thought1", "thought")
        assert chain_trace.next.data == "thought1"
        assert chain_trace.next.type_of_node == "thought"
        assert chain_trace.next.depth == 1
        assert chain_trace.next.next is None
        assert chain_trace.next.is_leaf is False

    def test_compose(self):
        # Test the compose method of ChainTrace
        chain_trace = ChainTrace("base_prompt", "base_prompt", 0)
        chain_trace.add("thought1", "thought")
        chain_trace.add("action1", "action")
        assert chain_trace.compose() == "base_promptthought1action1"

    def test_to_json(self):
        # Test the to_json method of ChainTrace
        chain_trace = ChainTrace("base_prompt", "base_prompt", 0)
        chain_trace.add("thought1", "thought")
        chain_trace.add("action1", "action")
        assert chain_trace.to_json() == [{'type': 'base_prompt', 'data': 'base_prompt'},
                                         {'type': 'thought', 'data': 'thought1'},
                                         {'type': 'action', 'data': 'action1'}]

    def test_get_max_depth(self):
        # Test the get_max_depth method of ChainTrace
        chain_trace = ChainTrace("base_prompt", "base_prompt", 0)
        chain_trace.add("thought1", "thought")
        chain_trace.add("action1", "action")
        assert chain_trace.get_max_depth() == 2

    def test_get_deepest_node(self):
        # Test the get_deepest_node method of ChainTrace
        chain_trace = ChainTrace("base_prompt", "base_prompt", 0)
        chain_trace.add("thought1", "thought")
        chain_trace.add("action1", "action")
        assert chain_trace.get_deepest_node().data == "action1"

    def test_str(self):
        # Test the __str__ method of ChainTrace
        chain_trace = ChainTrace("base_prompt", "base_prompt", 0)
        assert str(chain_trace) == "\x1b[37m[base_prompt] base_prompt\x1b[0m"
