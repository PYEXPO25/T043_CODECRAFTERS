// Check for browser support
const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

if (!SpeechRecognition) {
  alert(
    "உங்கள் உலாவி குரல் அங்கீகாரத்தை ஆதரிக்கவில்லை. தயவுசெய்து Chrome பயன்படுத்தவும்."
  );
} else {
  const recognition = new SpeechRecognition();

  // Set language to Tamil (Corrected Comment)
  recognition.lang = "ta-IN"; // Tamil language
  recognition.interimResults = true; // Show words while speaking
  recognition.continuous = true; // Keep listening until manually stopped

  let isListening = false;

  // Get buttons and transcript display
  const startBtn = document.getElementById("startBtn");
  const speakBtn = document.getElementById("speakBtn");
  const transcriptDisplay = document.getElementById("transcript");

  // Start/Stop voice recognition
  startBtn.addEventListener("click", () => {
    if (!isListening) {
      recognition.start();
      startBtn.textContent = "⏹ நிறுத்து";
      startBtn.style.backgroundColor = "red";
      isListening = true;
    } else {
      recognition.stop();
      startBtn.textContent = "🎙 கேட்க தொடங்கவும்";
      startBtn.style.backgroundColor = "";
      isListening = false;
    }
  });

  // Process voice input
  recognition.addEventListener("result", (event) => {
    let transcript = "";
    for (const result of event.results) {
      transcript += result[0].transcript + " ";
    }
    transcriptDisplay.textContent = transcript.trim();
  });

  // Handle errors
  recognition.addEventListener("error", (event) => {
    console.error("Speech recognition error:", event.error);
  });

  // Restart recognition automatically if not manually stopped
  recognition.addEventListener("end", () => {
    if (isListening) {
      recognition.start();
    }
  });

  // Convert text to speech (TTS)
  speakBtn.addEventListener("click", () => {
    const text = transcriptDisplay.textContent;
    if (text.trim() === "" || text === "உங்கள் உரை இங்கே தோன்றும்...") {
      alert("வாசிக்க உரை இல்லை!");
      return;
    }
    speakText(text);
  });

  function speakText(text) {
    const speech = new SpeechSynthesisUtterance();
    speech.text = text;
    speech.lang = "ta-IN"; // Tamil language
    speech.rate = 1;
    speech.pitch = 1;

    // Wait for voices to load before selecting Tamil voice
    let voices = speechSynthesis.getVoices();
    if (voices.length === 0) {
      speechSynthesis.onvoiceschanged = () => {
        voices = speechSynthesis.getVoices();
        setTamilVoice(speech, voices);
        speechSynthesis.speak(speech);
      };
    } else {
      setTamilVoice(speech, voices);
      speechSynthesis.speak(speech);
    }
  }

  function setTamilVoice(speech, voices) {
    const tamilVoice = voices.find((voice) => voice.lang === "ta-IN");
    if (tamilVoice) {
      speech.voice = tamilVoice;
    } else {
      alert("உங்கள் உலாவியில் தமிழ் குரல் கிடைக்கவில்லை.");
    }
  }
}

