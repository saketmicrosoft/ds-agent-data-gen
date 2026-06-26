from pathlib import Path

import orjson

from autodata_agent.config import Settings
from autodata_agent.schemas import AttemptTrace


class ArtifactRepository:
    def __init__(self, settings: Settings) -> None:
        self.trace_dir = Path(settings.trace_store_dir)
        self.dataset_dir = Path(settings.dataset_store_dir)
        self.trace_dir.mkdir(parents=True, exist_ok=True)
        self.dataset_dir.mkdir(parents=True, exist_ok=True)

    def write_trace(self, trace: AttemptTrace) -> None:
        path = self.trace_dir / f"round_{trace.round_id:04d}.json"
        path.write_bytes(orjson.dumps(trace.model_dump(), option=orjson.OPT_INDENT_2))

    def write_dataset_example(self, trace: AttemptTrace) -> None:
        path = self.dataset_dir / "accepted.jsonl"
        payload = orjson.dumps(trace.model_dump()) + b"\n"
        with path.open("ab") as handle:
            handle.write(payload)
