import base64
import json
from typing import Any, Dict

def handler(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Default pass-through function that returns data unchanged.
    """
    encoded_payload = data.get("payload", "")
    decoded_str = base64.b64decode(encoded_payload).decode("utf-8")
    data["data"] = json.loads(decoded_str)
    return data
