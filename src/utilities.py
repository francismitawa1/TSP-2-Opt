"""
Utility functions for 2-Opt TSP solver
"""

import math


def calculate_distance(x1, y1, x2, y2):
    """
    Calculate Euclidean distance between two points
    
    Args:
        x1, y1: Coordinates of first point
        x2, y2: Coordinates of second point
        
    Returns:
        Euclidean distance
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def format_distance(distance):
    """Format distance for display"""
    return f"{distance:.2f} units"


def format_time(seconds):
    """Format time for display"""
    if seconds < 0.001:
        return f"{seconds*1000:.3f}ms"
    elif seconds < 1:
        return f"{seconds*1000:.1f}ms"
    else:
        return f"{seconds:.3f}s"