# import pytest
# from ruamel.yaml import SequenceNode
# from piqard.utils.yaml_constructor import yaml_constructor
#
# class TestYAMLConstructor:
#     @pytest.fixture
#     def loader(self):
#         # mock a YAML loader
#         class Loader:
#             def construct_object(self, node):
#                 return node.value
#         return Loader()
#
#     @pytest.fixture
#     def sequence_node(self):
#         # mock a SequenceNode
#         class SequenceNode:
#             def __init__(self, value):
#                 self.value = value
#         return SequenceNode
#
#     def test_yaml_constructor(self, loader, sequence_node):
#         # Test a class with all valid data
#         @yaml_constructor
#         class TestClass:
#             def __init__(self, a, b, c=None):
#                 self.a = a
#                 self.b = b
#                 self.c = c
#
#         node = sequence_node([
#             ("a", "value1"),
#             ("b", "value2"),
#             ("c", "value3")
#         ])
#         obj = TestClass.from_yaml(loader, node)
#         assert obj.a == "value1"
#         assert obj.b == "value2"
#         assert obj.c == "value3"
#
#         # Test a class with some missing data
#         node = sequence_node([
#             ("a", "value1"),
#             ("b", "value2"),
#         ])
#         obj = TestClass.from_yaml(loader, node)
#         assert obj.a == "value1"
#         assert obj.b == "value2"
#         assert obj.c is None
#
#     def test_yaml_constructor_with_sequence(self, loader, sequence_node):
#         # Test a class with a sequence field
#         @yaml_constructor
#         class TestClass:
#             def __init__(self, a, b, c=None):
#                 self.a = a
#                 self.b = b
#                 self.c = c
#
#         node = sequence_node([
#             ("a", "value1"),
#             ("b", "value2"),
#             ("c", sequence_node(["item1", "item2"]))
#         ])
#         obj = TestClass.from_yaml(loader, node)
#         assert obj.a == "value1"
#         assert obj.b == "value2"
#         assert obj.c == ["item1", "item2"]
#
#     def test_yaml_constructor_with_null_values(self, loader, sequence_node):
#         # Test a class with a sequence field
#         @yaml_constructor
#         class TestClass:
#             def __init__(self, a, b, c=None):
#                 self.a = a
#                 self.b = b
#                 self.c = c
#
#         node = sequence_node([
#             ("a", "null"),
#             ("b", "value2"),
#             ("c", "null")
#         ])
#         obj = TestClass.from_yaml(loader, node)
#         assert obj.a is None
#         assert obj.b == "value2"
#         assert obj.c is None
