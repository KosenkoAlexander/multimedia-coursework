import { toggleMouth, agentApi, AGENTAPI } from "./threejs_container.js";

const recordButton = document.getElementById('agent_button');
const statusDisplay = document.getElementById('status');
let recognition;
let finalTranscript = '';
let utterance;

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
        agentApi[AGENTAPI.NO]();
        console.error('Speech recognition error:', event.error);
        statusDisplay.textContent = `Error: ${event.error}`;
    };

    recognition.onend = () => {
        statusDisplay.textContent = 'Processing...';
        finalTranscript = 'TEST STRING, COMMENT OUT WHEN DONE.';
        if (finalTranscript) {
            setTimeout(() => {
                statusDisplay.textContent = `You said: "${finalTranscript}"`;
                speakText(finalTranscript);
            }, 1000); // 1 second delay
        } else {
            agentApi[AGENTAPI.NO]();  // TODO Listen-Idle transition too snappy because of No
            statusDisplay.textContent = 'No speech detected.';
        }
    };

    recordButton.addEventListener('mousedown', () => {
        agentApi[AGENTAPI.LISTEN]();
        recognition.start();
    });

    recordButton.addEventListener('mouseup', () => {
        agentApi[AGENTAPI.IDLE]();
        recognition.stop();
    });

} else {
    statusDisplay.textContent = 'Web Speech API is not supported in this browser.';
    recordButton.disabled = true;
}

function speakText(text) {
    if ('speechSynthesis' in window) {
        utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';
        speechSynthesis.speak(utterance);

        utterance.onstart = () => {
            toggleMouth();
        };
        utterance.onend = (event) => {
            toggleMouth();
            statusDisplay.textContent = 'Ready.';
        };
    } else {
        console.warn('Text-to-speech not supported in this browser.');
    }
}