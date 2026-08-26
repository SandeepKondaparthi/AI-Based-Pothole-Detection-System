import h3
import pytest

def test_h3_res9_global_boundaries():
    # Test equator
    cell = h3.latlng_to_cell(0, 0, 9)
    assert h3.is_valid_cell(cell)
    
    # Test poles
    assert h3.is_valid_cell(h3.latlng_to_cell(89.9, 0, 9))
    assert h3.is_valid_cell(h3.latlng_to_cell(-89.9, 0, 9))
    
    # Test dateline
    c1 = h3.latlng_to_cell(34, 179.9, 9)
    c2 = h3.latlng_to_cell(34, -179.9, 9)
    assert h3.is_valid_cell(c1)
    assert h3.is_valid_cell(c2)
    # Across the dateline, H3 cells remain valid; grid distance is implementation-dependent.
    assert h3.grid_distance(c1, c2) <= 100

def test_h3_res9_precision():
    # Resolution 9 edge length is ~0.17 km
    # Points < 10m apart MUST be in same or neighboring cell
    lat, lng = 34.0522, -118.2437
    c_base = h3.latlng_to_cell(lat, lng, 9)
    
    # Tiny move (1m north ~ 0.000009 degrees)
    c_move = h3.latlng_to_cell(lat + 0.000009, lng, 9)
    assert h3.grid_distance(c_base, c_move) <= 1

def test_h3_cluster_consistency():
    # Ensure that points in the same hex always map to the same ID
    hex_center = h3.cell_to_latlng("8928308280fffff") # Example Res 9 hex
    lat, lng = hex_center
    assert h3.latlng_to_cell(lat, lng, 9) == "8928308280fffff"
