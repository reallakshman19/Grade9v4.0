from dataclasses import asdict, dataclass

@dataclass(frozen=True)
class Diagnostic:
    code: str
    path: str
    message: str
    remediation: str
    object_id: str = ""
    severity: str = "ERROR"

    def as_dict(self):
        return asdict(self)
