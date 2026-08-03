# Semantic Grounding for a Vehicle Warning Assistant

A prototype demonstrating how vehicle-warning explanations can be grounded
in an RDF knowledge graph and a controlled vocabulary.

The project is motivated by the need for deterministic, traceable, and
factually consistent AI responses in vehicle-related applications.

## Current functionality

- OWL-based semantic data model
- SKOS-controlled vocabulary for severity levels
- RDF knowledge graph containing vehicle warnings
- SPARQL retrieval of warning information
- Validation of predicted warning identifiers
- Rejection of identifiers outside the controlled vocabulary

## Architecture

1. A warning identifier is received.
2. The identifier is validated against the controlled vocabulary.
3. It is mapped to an RDF resource.
4. SPARQL retrieves the corresponding description, severity, component,
   and recommended action.
5. The retrieved facts are returned as grounded information.

## Semantic model

Classes:

- `WarningSymbol`
- `VehicleComponent`
- `RecommendedAction`

Relationships:

- `hasSeverity`
- `affectsComponent`
- `requiresAction`
- `hasDescription`

Severity values are represented as SKOS concepts:

- `Critical`
- `Warning`
- `Informational`

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install rdflib
