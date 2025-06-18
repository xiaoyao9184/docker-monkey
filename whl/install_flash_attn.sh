#!/bin/bash
set -e

if conda run --no-capture-output -n monkey python -c "import flash_attn" &> /dev/null; then
    echo "[✓] flash_attn installed"
else
    echo "[NOTE] FlashAttention only supports Ampere GPUs or newer."
    echo "[⟳] flash_attn installing..."
    mkdir -p ./whl
    conda run --no-capture-output -n monkey wget --show-progress \
        "https://gh-proxy.com/https://github.com/Dao-AILab/flash-attention/releases/download/v2.7.4.post1/flash_attn-2.7.4.post1%2Bcu12torch2.5cxx11abiFALSE-cp311-cp311-linux_x86_64.whl" \
        -O ./whl/flash_attn-2.7.4.post1+cu12torch2.5cxx11abiFALSE-cp311-cp311-linux_x86_64.whl
    conda run --no-capture-output -n monkey pip install ./whl/flash_attn-2.7.4.post1+cu12torch2.5cxx11abiFALSE-cp311-cp311-linux_x86_64.whl
fi