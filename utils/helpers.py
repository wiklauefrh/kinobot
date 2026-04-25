"""Helper utilities."""

from datetime import datetime
from typing import Optional


def format_date(dt: Optional[datetime]) -> str:
    """Format datetime to readable string."""
    if not dt:
        return "N/A"
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_duration(seconds: Optional[int]) -> str:
    """Format duration in seconds to HH:MM:SS."""
    if not seconds:
        return "N/A"
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def truncate(text: str, max_length: int = 100) -> str:
    """Truncate text to max length."""
    if len(text) > max_length:
        return text[:max_length - 3] + "..."
    return text


def format_number(num: int) -> str:
    """Format number with comma separator."""
    return f"{num:,}"
