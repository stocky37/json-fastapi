from dataclasses import dataclass, asdict


def as_dict(obj: dataclass):
    return {k: v for k, v in asdict(obj).items() if v is not None} if obj else {}
