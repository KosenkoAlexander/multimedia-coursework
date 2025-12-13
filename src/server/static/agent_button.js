import { agentApi, AGENTAPI } from "./threejs_container.js";

const agentButton = document.getElementById('agent_button');
const agentOutputText = document.getElementById('status');
let recognition;
let finalTranscript = '';

const userInputText = document.getElementById('user_input');


function processTranscript(transcript) {
    userInputText.textContent = transcript;
    fetch("/agent", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            'text': transcript
        })
    })
        .then(response => response.json())
        .then(data => {
            agentOutputText.textContent = data.text;
            speakText(data.text, data.emotion);
            return data.table;
        })
        .then(html => {
            document.getElementById("tableSpan").innerHTML = html;
        });
}

userInputText.addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        const transcript = userInputText.value;
        processTranscript(transcript);
    }
});

const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
    agentOutputText.textContent = 'Ready.';
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
        agentOutputText.textContent = 'Listening...';
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
        agentOutputText.textContent = `Error: ${event.error}`;
    };

    recognition.onend = () => {
        agentOutputText.textContent = 'Answer in progres...';
        // finalTranscript = 'TEST STRING, COMMENT OUT WHEN DONE.';
        // console.log(finalTranscript);
        if (finalTranscript) {
            processTranscript(finalTranscript);
        } else {
            agentApi[AGENTAPI.NO]();
            agentOutputText.textContent = 'No speech detected.';
        }
    };

    agentButton.addEventListener('mousedown', () => {
        agentApi[AGENTAPI.LISTEN]();
        recognition.start();
    });

    // recordButton.addEventListener('mouseup', () => {
    //     agentApi[AGENTAPI.THINK]();
    //     recognition.stop();
    // });
    recognition.onspeechend = () => {
        agentApi[AGENTAPI.THINK]();
        recognition.stop();
    };

} else {
    agentOutputText.textContent = 'Web Speech API is not supported in this browser.';
    agentButton.disabled = true;
    document.getElementById("user_input").readOnly = false;
}



import { toggleMouth } from "./threejs_container.js";
let utterance;

function speakText(text, emotion = "Talk") {
    const new_state = Object.keys(agentApi).includes(emotion) ? emotion : AGENTAPI.TALK;
    // console.log(new_state);
    if ('speechSynthesis' in window & !agentButton.disabled) {
        utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';
        speechSynthesis.speak(utterance);

        utterance.onstart = () => {
            toggleMouth(new_state);
        };
        utterance.onend = () => {
            toggleMouth();
        };
    } else {
        toggleMouth(new_state);
        setTimeout(() => {
            toggleMouth();
        }, text.length * 30);
        // console.warn('Text-to-speech not supported in this browser.');
    }
}
