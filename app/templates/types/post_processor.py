from typing import Callable

type PostProcessor = Callable[[str], str]
type PostProcessingPipeline = tuple[PostProcessor, ...]
