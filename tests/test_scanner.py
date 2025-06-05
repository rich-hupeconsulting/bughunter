import json
import os
import sys

# Ensure the project root is on the Python path so `modules` can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules import scanner


def test_write_json_creates_file():
    scanner.write_json("testtool", "example.com", ["data"])
    path = os.path.join("data", "outputs", "testtool_example_com.json")
    assert os.path.exists(path)
    with open(path) as f:
        obj = json.load(f)
    # check keys and values
    assert obj["tool"] == "testtool"
    assert obj["target"] == "example.com"
    assert "timestamp" in obj
    assert obj["results"] == ["data"]
    os.remove(path)
