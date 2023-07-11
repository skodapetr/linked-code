#!/usr/bin/env python3
from dataclasses import dataclass


# @lc-entity
# @lc-identifier :Identifiable
# @lc-name Identifiable
# @lc-description Interface for resources with an identifier.
@dataclass
class Identifiable:
    # @lc-property
    # @lc-name identifier
    identifier: str | None


# @lc-entity
# @lc-identifier :Identifiable
# @lc-name Identifiable
# @lc-description Source file with definition.
@dataclass
class SourceFile(Identifiable):
    # @lc-property
    # @lc-name relative_file_path
    relative_file_path: str


# @lc-entity
# @lc-identifier :Identifiable
# @lc-name Identifiable
# @lc-description Location in a source file.
@dataclass
class SourceLocation:
    # @lc-property
    # @lc-name file
    file: SourceFile
    # @lc-property
    # @lc-name line_number
    line_number: int


# @lc-entity
# @lc-identifier :Identifiable
# @lc-name Identifiable
# @lc-description Property.
@dataclass
class Property(Identifiable):
    # @lc-property
    # @lc-name source
    source: SourceLocation | None
    # @lc-property
    # @lc-name name
    name: str | None
    # @lc-property
    # @lc-name label
    label: str | None
    # @lc-property
    # @lc-name description
    description: str | None
    # @lc-property
    # @lc-name types
    types: list[str]


# @lc-entity
# @lc-identifier :EntityInstance
# @lc-name EntityInstance
# @lc-description Instance of an entity in a source file.
@dataclass
class EntityInstance:
    # @lc-property
    # @lc-name source
    source: SourceLocation | None
    # @lc-property
    # @lc-name name
    name: str | None
    # @lc-property
    # @lc-name label
    label: str | None
    # @lc-property
    # @lc-name description
    description: str | None
    # @lc-property
    # @lc-name properties
    properties: list[Property]
    # @lc-property
    # @lc-name extends
    extends: list[str]


# @lc-entity
# @lc-identifier :Entity
# @lc-name Entity
# @lc-description Identifiable entity, can have multiple instances.
@dataclass
class Entity(Identifiable):
    # @lc-property
    # @lc-name instances
    instances: list[EntityInstance]


# @lc-entity
# @lc-identifier :InstanceModel
# @lc-name InstanceModel
# @lc-description Collection of instances.
@dataclass
class InstanceModel:
    # @lc-property
    # @lc-name entities
    entities: list[Entity]
