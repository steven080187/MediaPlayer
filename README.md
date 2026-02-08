# Private Player - Android Version

Android video player app with playlist support, built with Kivy.

## Features

- **Multi-video playback**: Watch 1, 2, or 4 videos simultaneously
- **Playlist management**: Add video files from your device
- **Autoplay**: Automatically play next video in playlist
- **Landscape optimized**: Designed for horizontal viewing
- **Offline**: Complete privacy, no internet required

## Building the APK

### Prerequisites

You need to build this on Linux (or use WSL on Windows). macOS is not recommended for Android builds.

**Install dependencies:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Install buildozer
pip3 install --user buildozer cython

# Install Kivy (for testing locally)
pip3 install kivy
```

### Build APK

1. Navigate to the app directory:
```bash
cd ~/PornApp-android
```

2. Build the APK (first build will take 30-60 minutes as it downloads SDKs):
```bash
buildozer android debug
```

3. The APK will be in:
```
bin/privateplayer-1.0-arm64-v8a-debug.apk
```

### Transfer to Android Device

```bash
# Using adb
adb install bin/privateplayer-1.0-arm64-v8a-debug.apk

# Or use any file transfer method and install manually
```

## Alternative: Cloud Build Service

If you can't build locally, you can use a cloud build service like:
- GitHub Actions (free for public repos)
- Google Colab (free, requires setup)
- Buildozer Web Service (if available)

## Testing Locally (Desktop)

You can test the app on your Mac/Linux before building:

```bash
pip3 install kivy
python3 main.py
```

## Usage on Android

1. Install the APK
2. Grant storage permissions when prompted
3. Add videos to playlist using "+ Files" button
4. Tap a video to play it
5. Use layout selector to change view mode
6. Enable/disable autoplay as needed

## Permissions

- **READ_EXTERNAL_STORAGE**: To access your video files
- **WRITE_EXTERNAL_STORAGE**: To save app preferences (Android <10)
- **INTERNET**: Not actually used, but may be required by video codecs

## Supported Video Formats

MP4, MKV, AVI, MOV, WMV, FLV, WebM, M4V

## Notes

- First build takes a long time (downloads Android SDK/NDK)
- Subsequent builds are much faster
- APK size will be ~50-70MB
- Minimum Android version: 5.0 (API 21)
- Target Android version: 13 (API 33)
