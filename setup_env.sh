#!/bin/bash
# Setup environment for quantum crypto project

export LD_LIBRARY_PATH=$HOME/.local/lib:$LD_LIBRARY_PATH
export LIBRARY_PATH=$HOME/.local/lib:$LIBRARY_PATH
export C_INCLUDE_PATH=$HOME/.local/include:$C_INCLUDE_PATH

echo "✅ Environment variables set"
echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"
