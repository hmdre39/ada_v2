"""
JSON Sanitization utilities for converting numpy/special types to JSON-serializable formats
"""
import numpy as np
from typing import Any, Dict, List, Union


def sanitize_for_json(data: Any) -> Any:
    """
    Recursively convert numpy types and other non-JSON-serializable types to Python native types.
    
    Args:
        data: Data structure that may contain numpy types
        
    Returns:
        JSON-serializable version of the data
    """
    if isinstance(data, dict):
        return {k: sanitize_for_json(v) for k, v in data.items()}
    elif isinstance(data, (list, tuple)):
        return [sanitize_for_json(item) for item in data]
    elif isinstance(data, (np.integer, np.int8, np.int16, np.int32, np.int64,
                           np.uint8, np.uint16, np.uint32, np.uint64)):
        return int(data)
    elif isinstance(data, (np.floating, np.float16, np.float32, np.float64)):
        return float(data)
    elif isinstance(data, np.bool_):
        return bool(data)
    elif isinstance(data, np.ndarray):
        return data.tolist()
    elif isinstance(data, (np.complexfloating, np.complex64, np.complex128)):
        return {'real': float(data.real), 'imag': float(data.imag)}
    elif hasattr(data, 'item'):  # Catch any other numpy scalar types
        return data.item()
    return data
