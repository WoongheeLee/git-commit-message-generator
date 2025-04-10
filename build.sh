#!/bin/bash

EXE_NAME=git-commit-gen

echo "🚧 Building executable..."
pyinstaller --onefile \
  --name "$EXE_NAME" \
  --add-data "prompt_template.yml:." \
  main.py # --model gpt-4-turbo-2024-04-09 # Note: gpt-4-turbo is optimized for English — language settings may have limited effect

echo "📦 Moving executable to current directory..."
mv "dist/$EXE_NAME" ./

echo "🧹 Cleaning up..."
rm -rf build dist "$EXE_NAME".spec

echo "✅ Done! Executable: $EXE_NAME"

