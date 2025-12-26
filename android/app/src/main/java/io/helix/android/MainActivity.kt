package io.helix.android

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
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
    setContent {
      MaterialTheme {
        Surface(modifier = Modifier.fillMaxSize()) {
          MainScreen(vm)
        }
      }
    }
  }
}

@Composable
private fun MainScreen(vm: MainViewModel) {
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

    OutlinedTextField(
      value = state.question,
      onValueChange = vm::onQuestionChanged,
      modifier = Modifier.fillMaxWidth(),
      label = { Text("Ask a question") },
      minLines = 2,
    )

    Button(
      onClick = vm::send,
      enabled = !state.isLoading,
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

