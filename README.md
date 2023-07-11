# Linked Code
Connecting resources in your code. 

## Data Models

### Annotations
Instances are extracted from source documents.
They capture low level information like start of an entity definition, name, etc..

### Instance
Annotations can be aggregated into instances.
Instances represent entities and their properties in individual files.
If the same entity is declared in multiple class it is represented as multiple instances of same entity.

As this model is quite simple it should be used as the main model to share information.

### Aggregation
Build on instances this model provides aggregated view.
Information from multiple instances are merged together to provide unified view of the data.
Provenance information to level of instances is preserved.
As a result this model should be used only for analytical purpose.
