from typing import Callable

type Processor = Callable[[str], str]
type ProcessingPipeline = tuple[Processor, ...]
