package io.helix.android

import com.squareup.moshi.JsonClass
import retrofit2.http.Body
import retrofit2.http.POST

@JsonClass(generateAdapter = true)
data class ChatMessage(
  val role: String, // "user" | "assistant" | "system"
  val content: String,
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
  val metadata: Map<String, Any?> = emptyMap(),
)

@JsonClass(generateAdapter = true)
data class ChatResponse(
  val id: String,
  val created_at: String,
  val model: String,
  val response: String,
  val openai_response_id: String? = null,
  val usage: Map<String, Any?>? = null,
)

interface HelixApi {
  @POST("/v1/chat")
  suspend fun chat(@Body req: ChatRequest): ChatResponse
}

