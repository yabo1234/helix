# Android client (Kotlin) – Helix API

This service is meant to run as a backend (Cloud Run / VM / local dev). Your Android app calls it over HTTPS.

## Endpoint

- `POST /v1/chat`
- `GET /healthz`
- `GET /readyz`
- `GET /openapi.json`

## Auth modes

- **Public** (`HELIX_ACCESS_MODE=public`): no auth header.
- **Private** (`HELIX_ACCESS_MODE=private`): send **one** of:
  - `Authorization: Bearer <HELIX_API_KEY>`
  - `X-API-Key: <HELIX_API_KEY>`

## Retrofit example

### Gradle (app)

```kotlin
dependencies {
  implementation("com.squareup.retrofit2:retrofit:2.11.0")
  implementation("com.squareup.retrofit2:converter-moshi:2.11.0")
  implementation("com.squareup.okhttp3:okhttp:4.12.0")
  implementation("com.squareup.moshi:moshi-kotlin:1.15.2")
}
```

### Models

```kotlin
import com.squareup.moshi.JsonClass

@JsonClass(generateAdapter = true)
data class ChatMessage(
  val role: String, // "user" | "assistant" | "system"
  val content: String
)

@JsonClass(generateAdapter = true)
data class ChatRequest(
  val message: String,
  val messages: List<ChatMessage> = emptyList(),
  val context_documents: List<String> = emptyList(),
  val system_prompt: String? = null,
  val model: String? = null,
  val temperature: Double? = null,
  val max_output_tokens: Int? = null,
  val metadata: Map<String, Any?> = emptyMap()
)

@JsonClass(generateAdapter = true)
data class ChatResponse(
  val id: String,
  val created_at: String,
  val model: String,
  val response: String,
  val openai_response_id: String? = null,
  val usage: Map<String, Any?>? = null
)
```

### API interface

```kotlin
import retrofit2.http.Body
import retrofit2.http.POST

interface HelixApi {
  @POST("/v1/chat")
  suspend fun chat(@Body req: ChatRequest): ChatResponse
}
```

### Retrofit client (with optional auth)

```kotlin
import okhttp3.Interceptor
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import com.squareup.moshi.Moshi

fun createHelixApi(
  baseUrl: String,
  helixApiKey: String? = null, // set if backend is in private mode
): HelixApi {
  val authInterceptor = Interceptor { chain ->
    val reqBuilder = chain.request().newBuilder()
    if (!helixApiKey.isNullOrBlank()) {
      reqBuilder.addHeader("Authorization", "Bearer $helixApiKey")
      // alternatively: reqBuilder.addHeader("X-API-Key", helixApiKey)
    }
    chain.proceed(reqBuilder.build())
  }

  val okHttp = OkHttpClient.Builder()
    .addInterceptor(authInterceptor)
    .build()

  val moshi = Moshi.Builder().build()

  return Retrofit.Builder()
    .baseUrl(baseUrl) // e.g. "https://your-service.run.app/"
    .client(okHttp)
    .addConverterFactory(MoshiConverterFactory.create(moshi))
    .build()
    .create(HelixApi::class.java)
}
```

### Calling it

```kotlin
val api = createHelixApi(
  baseUrl = "https://YOUR_HOST/",
  helixApiKey = null // or your key
)

val resp = api.chat(
  ChatRequest(
    message = "Explain the Triple Helix model and give 3 policy interventions.",
    temperature = 0.2
  )
)

val answerText = resp.response
```

## Note about dry-run

If the backend is deployed with `HELIX_DRY_RUN=true`, the API returns a stub response without calling OpenAI. This is useful while wiring up the Android UI.

