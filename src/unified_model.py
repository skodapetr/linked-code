#!/usr/bin/env python3
from typing import NamedTuple
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
# @lc-description Location in a source file.
@dataclass
class SourceLocation:
    # @lc-property
    # @lc-name relative_file_path
    relative_file_path: str
    # @lc-property
    # @lc-name line_number
    line_number: int

# @lc-entity
# @lc-identifier :StringWithSource
# @lc-name StringWithSource
# @lc-description Value obtained from particular source.
@dataclass
class StringWithSource:
    # @lc-property
    # @lc-name value
    value: str
    # @lc-property
    # @lc-name sources
    sources: list[SourceLocation]

# @lc-entity
# @lc-identifier :Identifiable
# @lc-name Identifiable
# @lc-description Property.
@dataclass
class Property(Identifiable):
    # @lc-property
    # @lc-name sources
    sources: list[SourceLocation]
    # @lc-property
    # @lc-name name
    name: list[StringWithSource]
    # @lc-property
    # @lc-name label
    label: list[StringWithSource]
    # @lc-property
    # @lc-name description
    description: list[StringWithSource]


# @lc-entity
# @lc-identifier :EntityInstance
# @lc-name EntityInstance
@dataclass
class EntityInstance:
    # @lc-property
    # @lc-name sources
    sources: list[SourceLocation]
    # @lc-property
    # @lc-name name
    name: list[StringWithSource]
    # @lc-property
    # @lc-name label
    label: list[StringWithSource]
    # @lc-property
    # @lc-name description
    description: list[StringWithSource]
    # @lc-property
    # @lc-name properties
    properties: list[Property]
    # @lc-property
    # @lc-name extends
    extends: list[StringWithSource]


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
# @lc-identifier :UnifiedModel
# @lc-name UnifiedModel
# @lc-description Collection of instances.
@dataclass
class UnifiedModel:
    # @lc-property
    # @lc-name entities
    entities: list[Entity]
