import sys
from pathlib import Path

from classify_warning import PROJECT_ROOT, classify_warning
from lookup_warning import lookup_warning


def main():
    if len(sys.argv) != 2:
        print("Usage: python src/ground_warning.py <image_path>")
        return

    image_path = Path(sys.argv[1])

    if not image_path.is_absolute():
        image_path = PROJECT_ROOT / image_path

    if not image_path.is_file():
        print(f"Image not found: {image_path}")
        return

    try:
        prediction = classify_warning(image_path)
    except Exception as error:
        print(f"Classification failed: {error}")
        return

    print("\nVLM prediction")
    print("-" * 40)
    print(f"Warning ID: {prediction.warning_id}")
    print(f"Confidence: {prediction.confidence}")

    if prediction.warning_id == "unknown":
        print("\nNo controlled warning could be identified.")
        print("Knowledge-graph retrieval was not performed.")
        return

    if prediction.confidence == "low":
        print("\nPrediction confidence is too low.")
        print("Knowledge-graph retrieval was not performed.")
        return

    if prediction.confidence == "medium":
        print("\nNote: This prediction should be manually reviewed.")

    lookup_warning(prediction.warning_id)


if __name__ == "__main__":
    main()
