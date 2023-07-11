#!/usr/bin/env python3
import collections

from instance_model import *

Connection = collections.namedtuple("Connection", ["source", "target"])


def instance_model_to_plantuml(model: InstanceModel) -> str:
    # Public service: http://www.plantuml.com/plantuml/uml/
    counter = 0
    identifier_to_key = {}
    associations = set()
    extends = set()
    lines = ["@startuml"]
    # Create entities and collect connections.
    for entity in model.entities:
        for instance in entity.instances:
            counter += 1
            key = "entity_" + str(counter).zfill(3)
            name = instance.name
            if entity.identifier is not None:
                identifier_to_key[entity.identifier] = key
            lines.append(f'entity "{name}" as {key} ' + "{")
            for property in instance.properties:
                line = f"  {property.name}"
                if len(property.types) > 0:
                    for type in property.types:
                        associations.add(Connection(key, type))
                    # TODO Replace type identifier with code
                    line += ": " + " ".join(property.types)
                lines.append(line)
            for extend in instance.extends:
                extends.add(Connection(key, extend))
            lines.append("}")
    # Associations
    for source, target_identifier in associations:
        target = identifier_to_key.get(target_identifier, None)
        if target is None:
            # Can be missing or primitive type.
            continue
        lines.append(f"{source} --> {target}")
    # Extends
    for source, target_identifier in extends:
        target = identifier_to_key.get(target_identifier, None)
        if target is None:
            # Can be missing.
            continue
        lines.append(f"{source} --|> {target}")

    return "\n".join(lines) + "\n@enduml"
