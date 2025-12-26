package io.helix.android

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import java.io.IOException

data class UiState(
  val question: String = "",
  val isLoading: Boolean = false,
  val answer: String = "",
  val error: String? = null,
)

class MainViewModel : ViewModel() {
  private val api: HelixApi = HelixClient.createApi()

  private val _state = MutableStateFlow(UiState())
  val state: StateFlow<UiState> = _state.asStateFlow()

  fun onQuestionChanged(v: String) {
    _state.value = _state.value.copy(question = v)
  }

  fun send() {
    val q = _state.value.question.trim()
    if (q.isEmpty()) return

    _state.value = _state.value.copy(isLoading = true, error = null, answer = "")

    viewModelScope.launch {
      try {
        val resp = api.chat(ChatRequest(message = q, temperature = 0.2))
        _state.value = _state.value.copy(isLoading = false, answer = resp.response, error = null)
      } catch (e: Exception) {
        val msg =
          when (e) {
            is IOException -> "Network error. Check HELIX_BASE_URL and connectivity."
            else -> e.message ?: "Request failed."
          }
        _state.value = _state.value.copy(isLoading = false, error = msg)
      }
    }
  }
}

