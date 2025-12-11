const recordButton = document.getElementById('agent_button');
const statusDisplay = document.getElementById('status');
let recognition;
let finalTranscript = '';
let speechSynthesisUtterance;

if ('webkitSpeechRecognition' in window) {
    statusDisplay.textContent = 'Ready.';
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
        statusDisplay.textContent = 'Listening...';
        finalTranscript = ''; // Reset transcript on new recording
    };

    recognition.onresult = (event) => {
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                finalTranscript += event.results[i][0].transcript;
            }
        }
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        statusDisplay.textContent = `Error: ${event.error}`;
    };

    recognition.onend = () => {
        statusDisplay.textContent = 'Processing...';
        if (finalTranscript) {
            setTimeout(() => {
                statusDisplay.textContent = `You said: "${finalTranscript}"`;
                speakText(finalTranscript);
            }, 1000); // 1 second delay
        } else {
            statusDisplay.textContent = 'No speech detected.';
        }
    };

    recordButton.addEventListener('mousedown', () => {
        recognition.start();
    });

    recordButton.addEventListener('mouseup', () => {
        recognition.stop();
    });

} else {
    statusDisplay.textContent = 'Web Speech API is not supported in this browser.';
    recordButton.disabled = true;
}

function speakText(text) {
    if ('speechSynthesis' in window) {
        speechSynthesisUtterance = new SpeechSynthesisUtterance(text);
        speechSynthesisUtterance.lang = 'en-US';
        speechSynthesis.speak(speechSynthesisUtterance);
        speechSynthesisUtterance.onend = () => {
            statusDisplay.textContent = 'Ready.';
        };
    } else {
        console.warn('Text-to-speech not supported in this browser.');
    }
}