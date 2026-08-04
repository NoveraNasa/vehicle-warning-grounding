import csv
from pathlib import Path

from classify_warning import PROJECT_ROOT, classify_warning


GROUND_TRUTH = {
    "oil_pressure.jpg": "oil_pressure",
    "engine_temperature.jpg": "engine_temperature",
    "battery.jpg": "battery",
    "brake_system.jpg": "brake_system",
    "tire_pressure.jpg": "tire_pressure",
    "unknown.jpg": "unknown",
}


def main():
    images_dir = PROJECT_ROOT / "images"
    results_dir = PROJECT_ROOT / "results"
    results_dir.mkdir(exist_ok=True)

    output_file = results_dir / "vlm_evaluation.csv"
    rows = []
    correct_count = 0

    print("\nVLM evaluation")
    print("-" * 70)

    for filename, expected_id in GROUND_TRUTH.items():
        image_path = images_dir / filename

        if not image_path.is_file():
            print(f"Missing image: {filename}")
            rows.append(
                {
                    "filename": filename,
                    "expected_id": expected_id,
                    "predicted_id": "error",
                    "confidence": "",
                    "correct": False,
                }
            )
            continue

        try:
            prediction = classify_warning(image_path)
            predicted_id = prediction.warning_id
            confidence = prediction.confidence
            is_correct = predicted_id == expected_id

        except Exception as error:
            print(f"{filename}: Classification failed: {error}")
            predicted_id = "error"
            confidence = ""
            is_correct = False

        if is_correct:
            correct_count += 1

        rows.append(
            {
                "filename": filename,
                "expected_id": expected_id,
                "predicted_id": predicted_id,
                "confidence": confidence,
                "correct": is_correct,
            }
        )

        result = "CORRECT" if is_correct else "INCORRECT"

        print(
            f"{filename:<28} "
            f"Expected: {expected_id:<20} "
            f"Predicted: {predicted_id:<20} "
            f"{result}"
        )

    total = len(GROUND_TRUTH)
    accuracy = correct_count / total

    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "filename",
                "expected_id",
                "predicted_id",
                "confidence",
                "correct",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print("-" * 70)
    print(f"Correct predictions: {correct_count}/{total}")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    main()
