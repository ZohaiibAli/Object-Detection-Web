"""Download a few small public sample images into sample_data/. Run: python scripts/download_samples.py"""
import urllib.request
from pathlib import Path

SAMPLE_DIR = Path(__file__).resolve().parent.parent / "sample_data"

SAMPLES = {
    "bus.jpg": "https://ultralytics.com/images/bus.jpg",              # street scene
    "zidane.jpg": "https://ultralytics.com/images/zidane.jpg",        # people
    "dog.jpg": "https://raw.githubusercontent.com/pytorch/hub/master/images/dog.jpg",  # animal
}


def main() -> None:
    SAMPLE_DIR.mkdir(exist_ok=True)
    for name, url in SAMPLES.items():
        target = SAMPLE_DIR / name
        if target.exists():
            print(f"{name}: already there")
            continue
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(request, timeout=30) as response:
                target.write_bytes(response.read())
            print(f"{name}: downloaded")
        except Exception as error:
            print(f"{name}: failed ({error}) - the app still works without it")


if __name__ == "__main__":
    main()
