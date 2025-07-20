#!/bin/bash
echo "Testing automatic screenshot..."
export DISPLAY=:0
gnome-screenshot -f test_auto.png
if [ -f "test_auto.png" ]; then
    echo "✓ Automatic screenshot works!"
    rm test_auto.png
else
    echo "✗ Automatic screenshot failed"
fi
