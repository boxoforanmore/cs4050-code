#!/bin/bash
echo
echo "Running Unit Tests..."
echo "python3 -m unittest MatGraph.py"
echo
python3 -m unittest MatGraph.py
sleep 1 
echo
echo
echo
echo
echo "Running Test Files"
echo "python3 MatGraph.py ./TestFiles/*.txt"
echo
python3 MatGraph.py ./TestFiles/*.txt
