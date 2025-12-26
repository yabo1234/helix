# Helix Android sample client

This is a minimal Android Studio project that calls the Helix backend (`POST /v1/chat`).

## Quick start

1. Open the `android/` folder in Android Studio.
2. Set your backend URL (and optional API key) in your **local** Gradle properties (recommended):

Add to `~/.gradle/gradle.properties` (not committed):

```
HELIX_BASE_URL=https://your-service-host/
HELIX_API_KEY=            # optional; set only if HELIX_ACCESS_MODE=private
```

Notes:
- For emulator → local backend, use `http://10.0.2.2:8080/`
- Base URL must end with `/`

3. Run the app. Type a question and press “Send”.

## Backend modes

- If backend uses `HELIX_DRY_RUN=true`, the API returns a stub response (useful for UI wiring).
- If backend uses `HELIX_ACCESS_MODE=private`, set `HELIX_API_KEY` and the app will send `Authorization: Bearer ...`.

