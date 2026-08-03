from pathlib import Path
from rdflib import Graph

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GRAPH_FILE = PROJECT_ROOT / "data" / "vehicle_warnings.ttl"
QUERY_FILE = PROJECT_ROOT / "queries" / "all_warnings.rq"


def main():
    graph = Graph()
    graph.parse(GRAPH_FILE, format="turtle")

    print(f"Loaded {len(graph)} RDF triples.\n")

    query = QUERY_FILE.read_text(encoding="utf-8")
    results = graph.query(query)

    print(f"Found {len(results)} vehicle warnings:\n")

    for row in results:
        print(f"Warning:     {row.warningLabel}")
        print(f"Description: {row.description}")
        print(f"Severity:    {row.severityLabel}")
        print(f"Component:   {row.componentLabel}")
        print(f"Action:      {row.actionLabel}")
        print("-" * 60)


if __name__ == "__main__":
    main()
