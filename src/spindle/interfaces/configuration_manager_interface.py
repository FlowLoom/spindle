from abc import ABC, abstractmethod
from typing import Any, Optional

__All__ = ["IConfigurationManager"]


class IConfigurationManager(ABC):
    """
    Interface for configuration management operations.
    """

    @abstractmethod
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Retrieve a configuration value.

        Args:
            key (str): The key of the configuration item.
            default (Optional[Any]): The default value to return if the key is not found.

        Returns:
            Any: The value of the configuration item, or the default value if not found.
        """
        pass

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.

        Args:
            key (str): The key of the configuration item.
            value (Any): The value to set for the configuration item.
        """
        pass

    @abstractmethod
    def load(self) -> None:
        """
        Load configuration from a source (e.g., file, environment variables).
        """
        pass

    @abstractmethod
    def save(self) -> None:
        """
        Save the current configuration to a persistent storage.
        """
        pass

    @abstractmethod
    def get_config_dir(self) -> str:
        """
        Get the configuration directory path.

        Returns:
            str: The path to the configuration directory.
        """
        pass

    @abstractmethod
    def get_patterns_dir(self) -> str:
        """
        Get the patterns directory path.

        Returns:
            str: The path to the patterns directory.
        """
        pass

    @abstractmethod
    def get_all(self) -> dict:
        """
        Get all configuration key-value pairs.

        Returns:
            dict: A dictionary containing all configuration items.
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Clear all configuration settings.
        """
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """
        Check if a configuration key exists.

        Args:
            key (str): The key to check.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        pass