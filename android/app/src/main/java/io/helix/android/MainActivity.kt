package io.helix.android

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

class MainActivity : ComponentActivity() {
  private val vm: MainViewModel by viewModels()

  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    vm.refreshAuthState()
    setContent {
      MaterialTheme {
        Surface(modifier = Modifier.fillMaxSize()) {
          MainScreen(vm, firebaseConfigError = FirebaseInit.ensureInitialized(this))
        }
      }
    }
  }
}

@Composable
private fun MainScreen(vm: MainViewModel, firebaseConfigError: String?) {
  val state by vm.state.collectAsState()

  Column(
    modifier =
      Modifier.fillMaxSize()
        .verticalScroll(rememberScrollState())
        .padding(PaddingValues(16.dp)),
    verticalArrangement = Arrangement.spacedBy(12.dp),
  ) {
    Text(
      text = "Helix",
      style = MaterialTheme.typography.headlineMedium,
    )
    Text(
      text = "Backend: ${BuildConfig.HELIX_BASE_URL}",
      style = MaterialTheme.typography.bodySmall,
      color = MaterialTheme.colorScheme.onSurfaceVariant,
    )

    firebaseConfigError?.let { err ->
      Text(
        text = err,
        color = MaterialTheme.colorScheme.error,
        style = MaterialTheme.typography.bodyMedium,
      )
    }

    if (state.signedInEmail == null) {
      Text(text = "Sign in (Firebase email/password)", style = MaterialTheme.typography.titleMedium)

      OutlinedTextField(
        value = state.email,
        onValueChange = vm::onEmailChanged,
        modifier = Modifier.fillMaxWidth(),
        label = { Text("Email") },
        singleLine = true,
      )
      OutlinedTextField(
        value = state.password,
        onValueChange = vm::onPasswordChanged,
        modifier = Modifier.fillMaxWidth(),
        label = { Text("Password") },
        singleLine = true,
      )

      Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        Button(onClick = vm::signIn, enabled = !state.isLoading) { Text("Sign in") }
        Button(onClick = vm::signUp, enabled = !state.isLoading) { Text("Sign up") }
      }
    } else {
      Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically,
      ) {
        Text(
          text = "Signed in: ${state.signedInEmail}",
          style = MaterialTheme.typography.bodyMedium,
        )
        Button(onClick = vm::signOut, enabled = !state.isLoading) { Text("Sign out") }
      }
    }

    OutlinedTextField(
      value = state.question,
      onValueChange = vm::onQuestionChanged,
      modifier = Modifier.fillMaxWidth(),
      label = { Text("Ask a question") },
      minLines = 2,
    )

    Button(
      onClick = vm::send,
      enabled = !state.isLoading && state.signedInEmail != null,
      modifier = Modifier.align(Alignment.End),
    ) {
      Text("Send")
    }

    if (state.isLoading) {
      Spacer(modifier = Modifier.height(8.dp))
      CircularProgressIndicator()
    }

    state.error?.let { err ->
      Text(
        text = err,
        color = MaterialTheme.colorScheme.error,
        style = MaterialTheme.typography.bodyMedium,
      )
    }

    if (state.answer.isNotBlank()) {
      Text(
        text = "Answer",
        style = MaterialTheme.typography.titleMedium,
      )
      Text(
        text = state.answer,
        style = MaterialTheme.typography.bodyMedium,
      )
    }
  }
}

