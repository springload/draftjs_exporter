from typing import Any, List, Mapping

# The whole content state. blocks and entity_map.
ContentState = Mapping[str, Any]

def get_content_sample() -> List[ContentState]: ...
