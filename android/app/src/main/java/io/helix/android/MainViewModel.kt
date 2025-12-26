package io.helix.android

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.google.firebase.auth.FirebaseAuth
import kotlinx.coroutines.tasks.await
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
  val email: String = "",
  val password: String = "",
  val signedInEmail: String? = null,
)

class MainViewModel : ViewModel() {
  private val api: HelixApi = HelixClient.createApi()
  private val auth: FirebaseAuth = FirebaseAuth.getInstance()

  private val _state = MutableStateFlow(UiState())
  val state: StateFlow<UiState> = _state.asStateFlow()

  fun refreshAuthState() {
    val u = auth.currentUser
    _state.value = _state.value.copy(signedInEmail = u?.email)
  }

  fun onQuestionChanged(v: String) {
    _state.value = _state.value.copy(question = v)
  }

  fun onEmailChanged(v: String) {
    _state.value = _state.value.copy(email = v)
  }

  fun onPasswordChanged(v: String) {
    _state.value = _state.value.copy(password = v)
  }

  fun signUp() {
    val email = _state.value.email.trim()
    val password = _state.value.password
    if (email.isEmpty() || password.isEmpty()) return

    _state.value = _state.value.copy(isLoading = true, error = null)
    viewModelScope.launch {
      try {
        auth.createUserWithEmailAndPassword(email, password).await()
        val token = auth.currentUser?.getIdToken(true)?.await()?.token.orEmpty()
        AuthTokenStore.firebaseIdToken = token
        refreshAuthState()
        _state.value = _state.value.copy(isLoading = false, error = null)
      } catch (e: Exception) {
        _state.value = _state.value.copy(isLoading = false, error = e.message ?: "Sign up failed.")
      }
    }
  }

  fun signIn() {
    val email = _state.value.email.trim()
    val password = _state.value.password
    if (email.isEmpty() || password.isEmpty()) return

    _state.value = _state.value.copy(isLoading = true, error = null)
    viewModelScope.launch {
      try {
        auth.signInWithEmailAndPassword(email, password).await()
        val token = auth.currentUser?.getIdToken(true)?.await()?.token.orEmpty()
        AuthTokenStore.firebaseIdToken = token
        refreshAuthState()
        _state.value = _state.value.copy(isLoading = false, error = null)
      } catch (e: Exception) {
        _state.value = _state.value.copy(isLoading = false, error = e.message ?: "Sign in failed.")
      }
    }
  }

  fun signOut() {
    auth.signOut()
    AuthTokenStore.firebaseIdToken = ""
    refreshAuthState()
  }

  fun send() {
    val q = _state.value.question.trim()
    if (q.isEmpty()) return

    _state.value = _state.value.copy(isLoading = true, error = null, answer = "")

    viewModelScope.launch {
      try {
        // Refresh token before API calls (tokens expire).
        val token = auth.currentUser?.getIdToken(false)?.await()?.token.orEmpty()
        AuthTokenStore.firebaseIdToken = token
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

