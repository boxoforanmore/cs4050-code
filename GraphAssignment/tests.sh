#!/bin/bash
echo
echo "-----------------------------------"
echo "------RUNNING GRAPH UNITTESTS------"
echo "-----------------------------------"
echo
echo "ADJACENCY LIST:"
echo
echo "Running: python3 -m unittest ALGraph.py"
python3 -m unittest ALGraph.py
echo
echo
echo
echo "ADJACENCY MATRIX:"
echo
echo "Running: python3 -m unittest MatGraph.py"
python3 -m unittest MatGraph.py
echo
echo
echo
