from ruamel.yaml import SequenceNode


def yaml_constructor(clss):
    @classmethod
    def from_yaml(cls, loader, node):
        class_data = {}
        for key, val in node.value:
            if type(val) is SequenceNode:
                val = [
                    loader.construct_object(item.value)
                    if item.value != "null"
                    else None
                    for item in val.value
                ]
            else:
                val = loader.construct_object(val) if val != "null" else None
            class_data[key.value] = val
        if class_data:
            return cls(**class_data)
        else:
            return cls()

    setattr(clss, "from_yaml", from_yaml)
    return clss
