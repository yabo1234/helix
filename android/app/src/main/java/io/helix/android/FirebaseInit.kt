package io.helix.android

import android.content.Context
import com.google.firebase.FirebaseApp
import com.google.firebase.FirebaseOptions

object FirebaseInit {
  fun ensureInitialized(context: Context): String? {
    if (FirebaseApp.getApps(context).isNotEmpty()) return null

    val apiKey = BuildConfig.FIREBASE_API_KEY.trim()
    val appId = BuildConfig.FIREBASE_APP_ID.trim()
    val projectId = BuildConfig.FIREBASE_PROJECT_ID.trim()

    if (apiKey.isEmpty() || appId.isEmpty() || projectId.isEmpty()) {
      return "Firebase is not configured. Set FIREBASE_API_KEY, FIREBASE_APP_ID, FIREBASE_PROJECT_ID in ~/.gradle/gradle.properties."
    }

    val opts =
      FirebaseOptions.Builder()
        .setApiKey(apiKey)
        .setApplicationId(appId)
        .setProjectId(projectId)
        .build()

    FirebaseApp.initializeApp(context, opts)
    return null
  }
}

