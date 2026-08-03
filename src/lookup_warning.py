import sys
from pathlib import Path

from rdflib import Graph, Namespace

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GRAPH_FILE = PROJECT_ROOT / "data" / "vehicle_warnings.ttl"
QUERY_FILE = PROJECT_ROOT / "queries" / "warning_by_id.rq"

VW = Namespace("https://example.org/vehicle-warning/")

WARNING_VOCABULARY = {
    "oil_pressure": VW.OilPressureWarning,
    "engine_temperature": VW.EngineTemperatureWarning,
    "battery": VW.BatteryWarning,
    "brake_system": VW.BrakeSystemWarning,
    "tire_pressure": VW.TirePressureWarning,
}


def lookup_warning(predicted_id):
    warning_uri = WARNING_VOCABULARY.get(predicted_id)

    if warning_uri is None:
        allowed = ", ".join(WARNING_VOCABULARY)
        print(f"Unknown warning ID: {predicted_id}")
        print(f"Allowed IDs: {allowed}")
        return

    graph = Graph()
    graph.parse(GRAPH_FILE, format="turtle")

    query = QUERY_FILE.read_text(encoding="utf-8")
    rows = list(
        graph.query(
            query,
            initBindings={"warning": warning_uri},
        )
    )

    if not rows:
        print("No knowledge-graph information was found.")
        return

    row = rows[0]

    print("\nGrounded warning information")
    print("-" * 40)
    print(f"Warning:     {row.warningLabel}")
    print(f"Description: {row.description}")
    print(f"Severity:    {row.severityLabel}")
    print(f"Component:   {row.componentLabel}")
    print(f"Action:      {row.actionLabel}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python src/lookup_warning.py <warning_id>")
        print("Example: python src/lookup_warning.py oil_pressure")
        return

    lookup_warning(sys.argv[1].strip().lower())


if __name__ == "__main__":
    main()
