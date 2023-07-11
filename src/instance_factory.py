#!/usr/bin/env python3
# Load annotations and convert them into entities and properties.
#
import argparse
import pathlib
import json

import annotation_reader
import annotation_model
import instance_adapter_json
from instance_model import *


def _parse_arguments():
    parser = argparse.ArgumentParser(description="Extract instances from given files.")
    parser.add_argument(action="store", dest="input", help="Path to extract from.")
    return vars(parser.parse_args())


def main(args):
    model = create_instance_model(args["input"])
    print(instance_adapter_json.instance_model_to_json_string(model))


def create_instance_model(path: str):
    paths = _list_files(path)
    entities = []
    for path in paths:
        source_file = annotation_reader.extract_source_file(str(path))
        entities.extend(_create_entities(source_file))
    return InstanceModel(entities)


def _list_files(path: str) -> list[pathlib.Path]:
    root = pathlib.Path(path)
    if root.is_file():
        return [root]
    else:
        return [path for path in root.rglob("*") if path.is_file()]


def _create_entities(source: annotation_model.SourceFile) -> list[Entity]:
    source_file = SourceFile(None, source.relative_file_path)
    annotations = sorted(
        source.annotations, key=lambda item: item.annotation_line_start
    )
    entities = []
    for entity_annotations in _iterate_entities(annotations):
        entities.append(_create_entity(source_file, entity_annotations))
    return entities


def _iterate_entities(annotations: list[annotation_model.Annotation]):
    iterator = _split_annotations(annotations, annotation_model.EntityAnnotation)
    # Drop annotations before the first entity
    try:
        next(iterator)
    except StopIteration:
        return []
    return iterator


def _split_annotations(annotations: list[annotation_model.Annotation], separator):
    """Consumes sorted list of annotations."""
    collector = []
    for annotation in annotations:
        if isinstance(annotation, separator):
            if collector is not None:
                yield collector
            collector = []
        collector.append(annotation)
    if len(collector) > 0:
        yield collector


def _create_entity(
    source_file: SourceFile, annotations: list[annotation_model.Annotation]
) -> Entity:
    identifier = None
    identifier_annotations = _select_annotation(
        annotations, annotation_model.IdentifierAnnotation
    )
    if identifier_annotations is not None:
        identifier = identifier_annotations.identifier
    return Entity(identifier, [_create_entity_instance(source_file, annotations)])


def _select_annotation(annotations: list[annotation_model.Annotation], type):
    candidates = _select_annotations(annotations, type)
    assert len(candidates) < 2, "Expected at most one annotation"
    return candidates[0] if len(candidates) > 0 else None


def _select_annotations(annotations: list[annotation_model.Annotation], type):
    return [annotation for annotation in annotations if isinstance(annotation, type)]


def _create_entity_instance(
    source_file: SourceFile, annotations: list[annotation_model.Annotation]
) -> EntityInstance:
    iterator = _split_annotations(annotations, annotation_model.PropertyAnnotation)
    entity_annotations = next(iterator)

    source_location = None
    name = None
    label = None
    description = None
    extends = []
    for annotation in entity_annotations:
        if isinstance(annotation, annotation_model.EntityAnnotation):
            source_location = SourceLocation(
                source_file, annotation.annotation_line_start
            )
        elif isinstance(annotation, annotation_model.NameAnnotation):
            name = annotation.name
        elif isinstance(annotation, annotation_model.LabelAnnotation):
            label = annotation.label
        elif isinstance(annotation, annotation_model.DescriptionAnnotation):
            description = annotation.description
        elif isinstance(annotation, annotation_model.EntityExtendsAnnotation):
            extends.extend(annotation.extends)
    properties = [
        _create_property(source_file, property_annotations)
        for property_annotations in iterator
    ]
    return EntityInstance(
        source_location, name, label, description, properties, extends
    )


def _create_property(
    source_file: SourceFile, annotations: list[annotation_model.Annotation]
) -> Property:
    identifier = None
    source_location = None
    name = None
    label = None
    description = None
    types = []
    for annotation in annotations:
        if isinstance(annotation, annotation_model.PropertyAnnotation):
            source_location = SourceLocation(
                source_file, annotation.annotation_line_start
            )
        elif isinstance(annotation, annotation_model.IdentifierAnnotation):
            identifier = annotation.identifier
        elif isinstance(annotation, annotation_model.NameAnnotation):
            name = annotation.name
        elif isinstance(annotation, annotation_model.LabelAnnotation):
            label = annotation.label
        elif isinstance(annotation, annotation_model.DescriptionAnnotation):
            description = annotation.description
        elif isinstance(annotation, annotation_model.TypeAnnotation):
            types.append(annotation.type)
    return Property(identifier, source_location, name, label, description, types)


if __name__ == "__main__":
    main(_parse_arguments())
