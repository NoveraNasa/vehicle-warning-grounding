import base64
import json
import mimetypes
import sys
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel


PROJECT_ROOT = Path(__file__).resolve().parent.parent

WarningID = Literal[
    "oil_pressure",
    "engine_temperature",
    "battery",
    "brake_system",
    "tire_pressure",
    "unknown",
]


class WarningPrediction(BaseModel):
    warning_id: WarningID
    confidence: Literal["high", "medium", "low"]


def encode_image(image_path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(image_path)

    if mime_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise ValueError("Use a JPG, PNG, or WEBP image.")

    encoded = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def classify_warning(image_path: Path) -> WarningPrediction:
    load_dotenv(PROJECT_ROOT / ".env")
    client = OpenAI()

    response = client.responses.parse(
        model="gpt-5.6",
        reasoning={"effort": "low"},
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Classify the dashboard warning symbol. "
                            "Choose oil_pressure, engine_temperature, battery, "
                            "brake_system, tire_pressure, or unknown. "
                            "Use unknown if the symbol is missing, unclear, or "
                            "does not match one of the five permitted classes."
                        ),
                    },
                    {
                        "type": "input_image",
                        "image_url": encode_image(image_path),
                        "detail": "high",
                    },
                ],
            }
        ],
        text_format=WarningPrediction,
    )

    if response.output_parsed is None:
        raise RuntimeError("The model did not return a valid prediction.")

    return response.output_parsed


def main():
    if len(sys.argv) != 2:
        print("Usage: python src/classify_warning.py <image_path>")
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
    print("\nStructured result:")
    print(json.dumps(prediction.model_dump(), indent=2))


if __name__ == "__main__":
    main()
