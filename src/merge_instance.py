#!/usr/bin/env python3
import argparse
import collections
import json
import itertools

from instance_model import *
from instance_factory import create_instance_model
import instance_adapter_json


def _parse_arguments():
    parser = argparse.ArgumentParser(
        description="Extract and merge instances from given files."
    )
    parser.add_argument(action="store", dest="input", help="Path to extract from.")
    return vars(parser.parse_args())


def main(args):
    model = create_instance_model(args["input"])
    model = merge_entity_instance(model)
    print(instance_adapter_json.instance_model_to_json_string(model))


def merge_entity_instance(model: InstanceModel) -> InstanceModel:
    """Merge instances without preserving information about sources."""
    groups = _group_entity_by_identifier(model)
    entities = [_merge_entities(entities) for entities in groups.values()]
    return InstanceModel(entities)


def _group_entity_by_identifier(model: InstanceModel) -> dict[str, list[Entity]]:
    result = collections.defaultdict(list)
    for entity in model.entities:
        result[entity.identifier].append(entity)
    return result


def _merge_entities(entities: list[Entity]) -> Entity:
    instances = [instance for entity in entities for instance in entity.instances]
    merged_instance = None
    for instance in instances:
        if merged_instance is None:
            merged_instance = EntityInstance(
                None,
                instance.name,
                instance.label,
                instance.description,
                _merge_properties(instance.properties, []),
                instance.extends,
            )
        else:
            merged_instance = _merge_entity_instance(merged_instance, instance)
    return Entity(entities[0].identifier, [merged_instance])


def _merge_entity_instance(
    left: EntityInstance, right: EntityInstance
) -> EntityInstance:
    return EntityInstance(
        None,
        _first(left.name, right.name),
        _first(left.label, right.label),
        _first(left.description, right.description),
        _merge_properties(left.properties, right.properties),
        [*left.extends, *right.extends],
    )


def _first(*args: list[any]):
    for item in args:
        if item is not None:
            return item
    return None


def _merge_properties(left: list[Property], right: list[Property]) -> list[Property]:
    properties = {}
    for index, property in enumerate(itertools.chain(left, right)):
        # We identify using identifier or name.
        # When both are None the property can not be merged.
        key = _first(property.identifier, property.name, index)
        if key in properties:
            # Existing property.
            # TODO We should be able to merge from name only to property and vice versa.
            visited = properties[key]
            properties[key] = Property(
                _first(visited.identifier, property.identifier),
                None,
                _first(visited.name, property.name),
                _first(visited.label, property.label),
                _first(visited.description, property.description),
                [*visited.types, *property.types],
            )
        else:
            # New property.
            properties[key] = Property(
                property.identifier,
                None,
                property.name,
                property.label,
                property.description,
                property.types,
            )
    return list(properties.values())


if __name__ == "__main__":
    main(_parse_arguments())
