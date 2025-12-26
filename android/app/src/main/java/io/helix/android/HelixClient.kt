package io.helix.android

import com.squareup.moshi.Moshi
import okhttp3.Interceptor
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory

object HelixClient {
  private val moshi: Moshi = Moshi.Builder().build()

  fun createApi(): HelixApi {
    val apiKey = BuildConfig.HELIX_API_KEY.trim()

    val authInterceptor = Interceptor { chain ->
      val b = chain.request().newBuilder()
      // Prefer Firebase user token when present (HELIX_AUTH_MODE=firebase on backend).
      val firebaseToken = AuthTokenStore.firebaseIdToken.trim()
      if (firebaseToken.isNotEmpty()) {
        b.addHeader("Authorization", "Bearer $firebaseToken")
      } else if (apiKey.isNotEmpty()) {
        // Backend supports either Authorization Bearer or X-API-Key
        b.addHeader("Authorization", "Bearer $apiKey")
      }
      chain.proceed(b.build())
    }

    val okHttp = OkHttpClient.Builder()
      .addInterceptor(authInterceptor)
      .build()

    return Retrofit.Builder()
      .baseUrl(BuildConfig.HELIX_BASE_URL)
      .client(okHttp)
      .addConverterFactory(MoshiConverterFactory.create(moshi))
      .build()
      .create(HelixApi::class.java)
  }
}

