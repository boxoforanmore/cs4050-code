#!/bin/bash
echo
echo "Running Unit Tests..."
echo "python3 -m unittest MatGraph.py"
echo
python3 -m unittest ALGraph.py
sleep 1 
echo
echo
echo
echo
echo "Running Test Files"
echo "python3 ALGraph.py ./TestFiles/*.txt"
echo
sleep 1
echo
python3 ALGraph.py ./TestFiles/*.txt
