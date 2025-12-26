plugins {
  id("com.android.application")
  id("org.jetbrains.kotlin.android")
}

fun readGradleProp(name: String): String? {
  return (findProperty(name) as String?)?.trim()?.takeIf { it.isNotEmpty() }
}

android {
  namespace = "io.helix.android"
  compileSdk = 35

  defaultConfig {
    applicationId = "io.helix.android"
    minSdk = 24
    targetSdk = 35
    versionCode = 1
    versionName = "1.0"

    // Configurable via ~/.gradle/gradle.properties:
    // HELIX_BASE_URL=https://your-host/
    // HELIX_API_KEY=... (optional; only if backend is private)
    val baseUrl = readGradleProp("HELIX_BASE_URL") ?: "http://10.0.2.2:8080/"
    val apiKey = readGradleProp("HELIX_API_KEY") ?: ""

    buildConfigField("String", "HELIX_BASE_URL", "\"$baseUrl\"")
    buildConfigField("String", "HELIX_API_KEY", "\"$apiKey\"")
  }

  buildTypes {
    release {
      isMinifyEnabled = false
      proguardFiles(
        getDefaultProguardFile("proguard-android-optimize.txt"),
        "proguard-rules.pro",
      )
    }
  }

  buildFeatures {
    buildConfig = true
    compose = true
  }

  composeOptions {
    kotlinCompilerExtensionVersion = "1.5.15"
  }

  kotlinOptions {
    jvmTarget = "17"
  }
}

dependencies {
  // Compose
  implementation(platform("androidx.compose:compose-bom:2024.11.00"))
  implementation("androidx.activity:activity-compose:1.9.3")
  implementation("androidx.compose.ui:ui")
  implementation("androidx.compose.ui:ui-tooling-preview")
  implementation("androidx.compose.material3:material3")
  debugImplementation("androidx.compose.ui:ui-tooling")
  implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.7")
  implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.8.7")
  implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.7")

  // Networking
  implementation("com.squareup.okhttp3:okhttp:4.12.0")
  implementation("com.squareup.retrofit2:retrofit:2.11.0")
  implementation("com.squareup.retrofit2:converter-moshi:2.11.0")
  implementation("com.squareup.moshi:moshi-kotlin:1.15.2")

  // Coroutines
  implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.9.0")
}

