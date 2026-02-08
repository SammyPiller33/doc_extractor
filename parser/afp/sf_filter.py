"""
Module for filtering structured fields based on JSON configuration.
"""

import json
from typing import Optional


class SfFilter:
    """Filter for selecting which structured fields to parse."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the SF filter.

        Args:
            config_path: Path to JSON configuration file. If None, all SFs are parsed.
        """
        self.sf_names_to_parse: Optional[set[str]] = None
        
        if config_path:
            self._load_config(config_path)

    def _load_config(self, config_path: str) -> None:
        """Load and validate the JSON configuration."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validate structure
            if not isinstance(config, dict):
                raise ValueError("Configuration must be a JSON object")
            
            if "sf_names" not in config:
                raise ValueError("Configuration must contain a 'sf_names' key")
            
            if not isinstance(config["sf_names"], list):
                raise ValueError("'sf_names' must be a list")
            
            # Convert to set for O(1) lookup
            self.sf_names_to_parse = set(config["sf_names"])
            
            if not self.sf_names_to_parse:
                raise ValueError("'sf_names' list cannot be empty")
                
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON parsing error: {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

    def should_parse(self, sf_name: str) -> bool:
        """
        Check if a structured field should be parsed.

        Args:
            sf_name: Short name of the structured field (e.g., "BDT", "TLE").

        Returns:
            bool: True if the SF should be parsed, False otherwise.
        """
        # If no filter is configured, parse everything
        if self.sf_names_to_parse is None:
            return True
        
        return sf_name in self.sf_names_to_parse

    def get_filter_info(self) -> str:
        """Get information about the current filter."""
        if self.sf_names_to_parse is None:
            return "No filter (all SFs are parsed)"
        
        return f"Active filter: {sorted(self.sf_names_to_parse)}"