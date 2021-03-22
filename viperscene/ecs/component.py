from typing import Any

class Component:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    def on_added(self) -> None:
        pass
    
    def on_removed(self) -> None:
        pass
