#!/usr/bin/env python3
import json

from instance_model import *

def instance_model_to_json_string(model: InstanceModel) ->str:
    model_as_json = instance_model_to_json(model)
    return json.dumps(model_as_json, indent=2, ensure_ascii=False)

def instance_model_to_json(model: InstanceModel) -> dict[str, any]:
    def convert_location(location: SourceLocation | None):
        if location is None:
            return None
        else:
            return {
                "file": location.file.relative_file_path,
                "line": location.line_number,
            }

    object = {
        "metadata": {"version": 1},
        "entities": [
            {
                "identifier": entity.identifier,
                "source": convert_location(instance.source),
                "name": instance.name,
                "label": instance.label,
                "description": instance.description,
                "extends": instance.extends,
                "properties": [
                    {
                        "identifier": property.identifier,
                        "source": convert_location(property.source),
                        "name": property.name,
                        "label": property.label,
                        "description": property.description,
                        "types": property.types,
                    }
                    for property in instance.properties
                ],
            }
            for entity in model.entities
            for instance in entity.instances
        ],
    }
    return _remove_empty(object)


def _remove_empty(value: any):
    """Remove None and empty lists."""
    if type(value) is list:
        filtered_list = [
            next_item
            for item in value
            if (next_item := _remove_empty(item)) is not None
        ]
        return filtered_list if len(filtered_list) > 0 else None
    elif type(value) is dict:
        return {
            key: next_item
            for key, item in value.items()
            if (next_item := _remove_empty(item)) is not None
        }
    else:
        return value
