#!/usr/bin/env python3
from dataclasses import dataclass


# @lc-entity
# @lc-identifier :Annotation
# @lc-name Annotation
# @lc-description Base class for all annotations.
@dataclass
class Annotation:
    # @lc-property
    # @lc-name comment_line_start
    comment_line_start: int

    # @lc-property
    # @lc-name annotation_line_start
    annotation_line_start: int


# @lc-entity
# @lc-identifier :SourceFile
# @lc-name SourceFile
# @lc-description Represent a single source file.
@dataclass
class SourceFile:
    # @lc-property
    # @lc-name relative_file_path
    # @lc-description Relative path to the file.
    relative_file_path: str

    # @lc-property
    # @lc-name annotations
    # @lc-description Annotations found in given file.
    annotations: list[Annotation]


# @lc-entity
# @lc-identifier :PrefixAnnotation
# @lc-name PrefixAnnotation
# @lc-extends :Annotation
# @lc-description Prefix definition.
@dataclass
class PrefixAnnotation(Annotation):
    # @lc-property
    # @lc-name prefix_name
    prefix_name: str

    # @lc-property
    # @lc-name prefix_value
    prefix_value: str


# @lc-entity
# @lc-identifier :EntityAnnotation
# @lc-name EntityAnnotation
# @lc-extends :Annotation
# @lc-description Set context to new entity.
@dataclass
class EntityAnnotation(Annotation):
    ...


# @lc-entity
# @lc-identifier :PropertyAnnotation
# @lc-name PropertyAnnotation
# @lc-extends :Annotation
# @lc-description Set context to new property.
@dataclass
class PropertyAnnotation(Annotation):
    ...


# @lc-entity
# @lc-identifier :ResourceAnnotation
# @lc-name ResourceAnnotation
# @lc-extends :Annotation
# @lc-description Add identifier for current context.
@dataclass
class IdentifierAnnotation(Annotation):
    # @lc-property
    # @lc-name identifier
    identifier: str


# @lc-entity
# @lc-identifier :NameAnnotation
# @lc-name NameAnnotation
# @lc-extends :Annotation
# @lc-description Add a name for current context.
@dataclass
class NameAnnotation(Annotation):
    # @lc-property
    # @lc-name name
    name: str


# @lc-entity
# @lc-identifier :LabelAnnotation
# @lc-name LabelAnnotation
# @lc-extends :Annotation
# @lc-description Add human readable label for current context.
@dataclass
class LabelAnnotation(Annotation):
    # @lc-property
    # @lc-name label
    label: str


# @lc-entity
# @lc-identifier :DescriptionAnnotation
# @lc-name DescriptionAnnotation
# @lc-extends :Annotation
# @lc-description Add human readable description for current context.
@dataclass
class DescriptionAnnotation(Annotation):
    # @lc-property
    # @lc-name description
    description: str


# @lc-entity
# @lc-identifier :EntityExtendsAnnotation
# @lc-name EntityExtendsAnnotation
# @lc-extends :Annotation
# @lc-description Current context is an extension of another one.
@dataclass
class EntityExtendsAnnotation(Annotation):
    # @lc-property
    # @lc-name extends
    extends: list[str]

# @lc-entity
# @lc-identifier :TypeAnnotation
# @lc-name TypeAnnotation
# @lc-extends :Annotation
# @lc-description Define property type.
@dataclass
class TypeAnnotation(Annotation):
    # @lc-property
    # @lc-name extends
    type: str
