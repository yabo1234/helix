# Helix Android sample client

This is a minimal Android Studio project that calls the Helix backend (`POST /v1/chat`).

## Quick start

1. Open the `android/` folder in Android Studio.
2. Set your backend URL (and optional API key) in your **local** Gradle properties (recommended):

Add to `~/.gradle/gradle.properties` (not committed):

```
HELIX_BASE_URL=https://your-service-host/
HELIX_API_KEY=            # optional; set only if HELIX_ACCESS_MODE=private
FIREBASE_API_KEY=         # required for HELIX_AUTH_MODE=firebase
FIREBASE_APP_ID=          # required for HELIX_AUTH_MODE=firebase (Firebase Android App ID)
FIREBASE_PROJECT_ID=      # required for HELIX_AUTH_MODE=firebase
```

Notes:
- Base URL must end with `/`

3. Run the app. Type a question and press “Send”.

## Backend modes

- If backend uses `HELIX_DRY_RUN=true`, the API returns a stub response (useful for UI wiring).
- If backend uses `HELIX_ACCESS_MODE=private` (api_key mode), set `HELIX_API_KEY` and the app will send `Authorization: Bearer ...`.
- If backend uses `HELIX_AUTH_MODE=firebase`, configure Firebase values above; the app will sign users in with Firebase and send the Firebase ID token as `Authorization: Bearer ...`.

## Using a real Android phone (local dev)

### Option 1: Backend deployed (recommended)

Set:

```
HELIX_BASE_URL=https://your-service.run.app/
```

### Option 2: Backend on your laptop over Wi‑Fi (HTTP)

1. Ensure laptop + phone are on the **same Wi‑Fi**.
2. Start backend:

```bash
HELIX_AUTH_MODE=firebase HELIX_DRY_RUN=true python3 -m uvicorn helix.api:app --host 0.0.0.0 --port 8080
```

3. Find your laptop LAN IP (example `192.168.1.50`) and set:

```
HELIX_BASE_URL=http://192.168.1.50:8080/
```

Note: this Android project allows HTTP **only in debug builds** (`app/src/debug/AndroidManifest.xml`). For release, use HTTPS.

## Using the emulator

Set:

```
HELIX_BASE_URL=http://10.0.2.2:8080/
```

