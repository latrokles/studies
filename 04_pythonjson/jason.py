import json
from typing import Any, Dict


def to_dict(obj: object) -> Dict[str, Any]:
    match obj:
        case int()|float()|str()|bool()|None:
            return obj
        case list()|tuple()|set():
            return [to_dict(i) for i in obj]
        case dict():
            return {to_dict(k): to_dict(v) for k, v in obj.items()}
        case object():
            return to_dict(obj.__dict__)


def to_json(obj: object) -> str:
    json.dumps(to_dict(obj))
