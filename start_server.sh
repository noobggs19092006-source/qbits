#!/bin/bash
# QBits Server Startup Script

export LD_LIBRARY_PATH=$HOME/.local/lib:$LD_LIBRARY_PATH
export GROQ_API_KEY='gsk_Jz9UQ5dLrn1quFTrkFutWGdyb3FYUL0CYMzho3ccqSlK3wDpoueJD'

echo "=============================================="
echo "🚀 Starting QBits Platform with REAL AI"
echo "=============================================="
echo ""
echo "Library Path: $LD_LIBRARY_PATH"
echo "AI Status: ✅ ENABLED (Groq LLM)"
echo ""

python3 src/app.py
