from typing import Any, Union


class Cache:
    def __init__(self) -> None:
        self.cache: dict[str, Any] = {}

    def add(self, key: str, value: Any) -> bool:
        """Add value to cache if its doesnt exist"""
        if key in self.cache.keys():
            return False
        self.cache[key] = value
        return True

    def remove(self, key: str) -> bool:
        """Add value to cache if its doesnt exist"""
        if key not in self.cache.keys():
            return False
        self.cache.pop(key)
        return True

    def get_item(self, key: str) -> Union[bool, Any]:
        """Return the given cache"""
        if key not in self.cache.keys():
            return False
        return self.cache[key]

    def get_cache(self) -> dict[str, Any]:
        """Return the given cache"""
        return self.cache


watcher_cache = Cache()
