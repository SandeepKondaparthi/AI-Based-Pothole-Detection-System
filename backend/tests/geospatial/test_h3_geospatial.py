import h3
import pytest

def test_h3_resolution_9_accuracy():
    # Test coordinates in Los Angeles
    lat, lng = 34.0522, -118.2437
    cell = h3.latlng_to_cell(lat, lng, 9)
    
    # Check that it's a valid H3 index
    assert h3.is_valid_cell(cell)
    assert h3.get_resolution(cell) == 9
    
    # Check that a point slightly moved (10m) stays in same cell
    # Resolution 9 is ~0.1 km^2, so 10m is well within one cell
    lat2, lng2 = 34.05221, -118.24371
    cell2 = h3.latlng_to_cell(lat2, lng2, 9)
    assert cell == cell2

def test_h3_different_cells():
    # Points 1km apart should be in different cells
    lat1, lng1 = 34.0522, -118.2437
    lat2, lng2 = 34.0622, -118.2437
    
    cell1 = h3.latlng_to_cell(lat1, lng1, 9)
    cell2 = h3.latlng_to_cell(lat2, lng2, 9)
    assert cell1 != cell2

def test_h3_neighbor_check():
    lat, lng = 34.0522, -118.2437
    cell = h3.latlng_to_cell(lat, lng, 9)
    
    # Get neighbors (disk distance 1)
    neighbors = h3.grid_disk(cell, 1)
    assert len(neighbors) == 7 # Self + 6 neighbors
    assert cell in neighbors
