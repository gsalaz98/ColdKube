import re

def to_camel_case(string: str) -> str:
    string = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", string)
    string = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", string)
    string = string.replace("-", "_")
    return string.lower()

def get_nested_resources(resource):
    # Recurse into nested objects and calls out to
    # neo4j to create the object if it doesn't exist
    resources = []
    next_recurse = [resource]
    while len(next_recurse) > 0:
        next_objs = []
        for obj in next_recurse:
            if obj is None:
                # Will happen when a resource that can contain
                # a nested object didn't have it specified
                continue

            referenced_objects = [i for i in obj.referenced_objects if i is not None]

            next_objs.extend(referenced_objects)
            resources.extend(referenced_objects)

        next_recurse = next_objs

    return resources