# Installing Termux (Latest Version)

This guide provides instructions for installing the latest version of Termux (v0.118.3) on Android devices to run the Helix Triple Helix Innovation project.

## What is Termux?

Termux is a terminal emulator and Linux environment app for Android that works directly without requiring root access. It allows you to run command-line programs and scripts on your Android device.

## Latest Version

**Current Version:** v0.118.3 (Released: 2025-05-22)

## Installation Methods

### Method 1: F-Droid (Recommended)

The recommended way to install Termux is through F-Droid, as the Google Play Store version is deprecated and no longer maintained.

1. Install F-Droid from [https://f-droid.org/](https://f-droid.org/)
2. Open F-Droid and search for "Termux"
3. Install Termux from F-Droid

### Method 2: Direct APK Download from GitHub

Download the appropriate APK file for your device architecture from the [latest release](https://github.com/termux/termux-app/releases/tag/v0.118.3):

#### Choose Your Architecture:

- **ARM 64-bit (Most modern devices)**: 
  - Download: [termux-app_v0.118.3+github-debug_arm64-v8a.apk](https://github.com/termux/termux-app/releases/download/v0.118.3/termux-app_v0.118.3%2Bgithub-debug_arm64-v8a.apk)
  - Size: ~35 MB
  - Most common for modern Android devices (2016+)

- **ARM 32-bit (Older devices)**:
  - Download: [termux-app_v0.118.3+github-debug_armeabi-v7a.apk](https://github.com/termux/termux-app/releases/download/v0.118.3/termux-app_v0.118.3%2Bgithub-debug_armeabi-v7a.apk)
  - Size: ~32 MB
  - For older Android devices

- **x86 64-bit (Intel/AMD processors)**:
  - Download: [termux-app_v0.118.3+github-debug_x86_64.apk](https://github.com/termux/termux-app/releases/download/v0.118.3/termux-app_v0.118.3%2Bgithub-debug_x86_64.apk)
  - Size: ~35 MB
  - For Android devices with Intel/AMD processors (rare)

- **x86 32-bit**:
  - Download: [termux-app_v0.118.3+github-debug_x86.apk](https://github.com/termux/termux-app/releases/download/v0.118.3/termux-app_v0.118.3%2Bgithub-debug_x86.apk)
  - Size: ~34 MB

- **Universal (Works on all architectures)**:
  - Download: [termux-app_v0.118.3+github-debug_universal.apk](https://github.com/termux/termux-app/releases/download/v0.118.3/termux-app_v0.118.3%2Bgithub-debug_universal.apk)
  - Size: ~118 MB
  - Larger file but works on any device

#### Installation Steps:

1. Download the appropriate APK file to your Android device
2. Enable installation from unknown sources in your Android settings
3. Open the downloaded APK file and follow the installation prompts
4. Grant necessary permissions when prompted

## How to Check Your Device Architecture

If you're unsure which APK to download, you can:

1. Install a CPU identification app from Google Play Store (e.g., "CPU-Z" or "AIDA64")
2. Look for the "Architecture" or "CPU Architecture" field
3. Common values:
   - `arm64-v8a` or `aarch64` → Download ARM 64-bit version
   - `armeabi-v7a` or `armv7` → Download ARM 32-bit version
   - `x86_64` → Download x86 64-bit version
   - `x86` → Download x86 32-bit version

**Tip:** If in doubt, download the universal APK which works on all architectures.

## Setting Up Termux for Helix Project

After installing Termux, follow these steps to set up the environment for running the Helix project:

### 1. Update Termux Packages

```bash
pkg update && pkg upgrade
```

### 2. Install Python

```bash
pkg install python
```

### 3. Install Git

```bash
pkg install git
```

### 4. Install Required Build Tools

```bash
pkg install build-essential
```

### 5. Clone the Helix Repository

```bash
cd ~
git clone https://github.com/yabo1234/helix.git
cd helix
```

### 6. Install Python Dependencies

If the project has a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 7. Run the Project

```bash
python triple-helix-innovation.py
```

## Storage Access in Termux

To access your device's shared storage from Termux:

```bash
termux-setup-storage
```

This will prompt you to grant storage permissions and create a `~/storage` directory with symbolic links to your device's storage.

## Troubleshooting

### Installation Issues

- **"App not installed"**: Make sure you've enabled installation from unknown sources for your browser or file manager
- **Architecture mismatch**: Try the universal APK if you're getting installation errors

### Permission Issues

If Termux requests permissions and you accidentally denied them:
1. Go to Android Settings → Apps → Termux
2. Go to Permissions
3. Enable the required permissions

### Package Installation Fails

If `pkg update` or `pkg install` fails:
```bash
# Try changing the mirror
termux-change-repo
```

## Additional Resources

- **Termux Wiki**: [https://wiki.termux.com/](https://wiki.termux.com/)
- **Termux GitHub**: [https://github.com/termux/termux-app](https://github.com/termux/termux-app)
- **Termux Community**: [https://gitter.im/termux/termux](https://gitter.im/termux/termux)

## Security Note

**Important**: Always download Termux from official sources:
- F-Droid repository
- Official GitHub releases (https://github.com/termux/termux-app/releases)

**Do not install Termux from Google Play Store** as it is outdated and no longer maintained.

## What's New in v0.118.3

- Fixed crash on Android 16 QPR1
- Fixed storage permission issues after updates
- Improved plugin compatibility with Termux:API
- Various bug fixes and stability improvements

For the full changelog, see: [v0.118.3 Release Notes](https://github.com/termux/termux-app/releases/tag/v0.118.3)
