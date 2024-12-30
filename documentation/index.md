# Linked Code
Linked code allows developers to connect software parts.

## Motivation
A common practice in software development is to see diagrams and code as a plan and a realization/implementation.
In the worst-case scenario, diagrams are images accompanied by text that the developers need to study and implement them.
Such scenarios are not uncommon.
The diagrams and text together form a specification, an artefact created by an analyst.
Yet those artifacts are often not owned by the developers, although they may be tasked to keep them up to date.
Approaches, such as diagrams as code, aim to narrow the gap between the code and the specification.
Generating code from specification also help.

Yet inevitably, the code and the specification start to diverge.
The main reason is that there can be only one source of truth.
The source of truth is the code, the ultimate definition of architecture, data model and behavior.
The main drawback of the code is that it is way too detailed.
As a result, it is hard to reason about software using only the code.
We need abstraction; we need the diagrams.

Many tools focus on a top-down approach where code is the product of specification.
Such tools are excellent for use-case analysis, data modelling or software design.
Yet once we start with the implementation, the code quickly becomes the main defining artefact.
We need to transition some of the information and responsibilities from the specification to the code.

For example, a class model may define a data model for an application, until there is code with a domain model implemented in a programming language of choice.
Once implemented, the code always specifies the domain model, not the class diagram.

The idea behind this repository is to embrace this transition and allow developers to connect (link) their code to the specification.
The specification can be created and modified based on the existing code and vice versa.
A developer should not need to search documentation in order to implement a class that will temporarily hold business data.
On the other hand, an analyst, or an architect, should be able to quickly identify parts of the software that are using given business data.
