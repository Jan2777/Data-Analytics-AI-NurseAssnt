const textInput = document.getElementById('textInput');
const recordBtn = document.getElementById('recordBtn');
const playBtn = document.getElementById('playBtn');
const submitBtn = document.getElementById('submitBtn');
const output = document.getElementById('output');
const taskSelect = document.getElementById('taskSelect');

let recognition;
let synth = window.speechSynthesis;

// Initialize Speech Recognition (for audio input)
if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.lang = 'ta-IN';  // Tamil (India)
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        textInput.value = transcript;
    };

    recordBtn.onclick = () => {
        recognition.start();
        recordBtn.textContent = 'Recording...';
    };

    recognition.onend = () => {
        recordBtn.textContent = 'Record Audio (Tamil)';
    };
} else {
    alert('Speech recognition not supported in this browser.');
}

// Submit to backend
submitBtn.onclick = async () => {
    const text = textInput.value;
    const task = taskSelect.value;
    if (!text) return alert('Enter text or record audio.');

    const response = await fetch('http://127.0.0.1:5000/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, task })
    });
    const data = await response.json();
    output.textContent = data.output;

    // Speak the output (audio response)
    const utterance = new SpeechSynthesisUtterance(data.output);
    utterance.lang = 'en-US';  // English output; change to 'ta-IN' for Tamil
    synth.speak(utterance);
};

// Play button for manual audio playback
playBtn.onclick = () => {
    if (output.textContent) {
        const utterance = new SpeechSynthesisUtterance(output.textContent);
        utterance.lang = 'en-US';
        synth.speak(utterance);
    }
};