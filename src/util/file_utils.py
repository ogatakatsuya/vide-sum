"""
File loading utility
"""

import json
from pathlib import Path


def load_video_extensions(json_path="data/extensions.json"):
    """Load extensions.json and get video ID to extension mapping"""
    json_file = Path(json_path)

    if not json_file.exists():
        return {}

    with open(json_file, "r") as f:
        return json.load(f)
