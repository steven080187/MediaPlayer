#!/bin/bash

echo "Building Android APK using Docker..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed."
    echo "Install it: brew install --cask docker"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "🔨 Building APK (first build takes 30-60 minutes)..."
echo ""

docker run --rm -v "$(pwd)":/home/user/hostcwd \
    --privileged \
    cimg/android:2024.01.1 \
    bash -c "cd /home/user/hostcwd && pip3 install --user buildozer cython && export PATH=\$PATH:~/.local/bin && buildozer android debug"

if [ -f "bin/privateplayer-1.0-arm64-v8a-debug.apk" ]; then
    echo ""
    echo "✅ APK built successfully!"
    echo "📦 Location: bin/privateplayer-1.0-arm64-v8a-debug.apk"
    echo ""
    echo "Transfer to your Android phone and install it."
else
    echo "❌ Build failed."
    exit 1
fi
