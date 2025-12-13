import { agentApi, AGENTAPI } from "./threejs_container.js";
import { speakText } from "./speakText.js";

const recordButton = document.getElementById('agent_button');
const statusDisplay = document.getElementById('status');
let recognition;
let finalTranscript = '';

const speechReplacement = document.getElementById('speechReplacement');


function processTranscript(transcript){
    statusDisplay.textContent = transcript;
    fetch("/agent", {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({
            'text':transcript
        })
    })
        .then(response => response.json())
        .then(data => {
            statusDisplay.textContent = data.text;
            speakText(finalTranscript);
            // something with data.emotion
            return data.table;
        })
        .then(html => {
            document.getElementById("tableSpan").innerHTML = html;
        });
}

speechReplacement.addEventListener('keypress', function(event){
    if (event.key === 'Enter'){
        const transcript = speechReplacement.value;
        processTranscript(transcript);
    }
});

if ('webkitSpeechRecognition' in window) {
    statusDisplay.textContent = 'Ready.';
    recognition = new webkitSpeechRecognition();
    //recognition.processLocally = true;
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
        statusDisplay.textContent = 'Answer in progres...';
        // finalTranscript = 'TEST STRING, COMMENT OUT WHEN DONE.';
        // console.log(finalTranscript);
        finalTranscript = document.getElementById('speechReplacement').value //TODO remove!
        if (finalTranscript) {
            //setTimeout(() => {
            //    statusDisplay.textContent = "Ready.";
            //}, 5 * 1000);
            // TODO process finalTranscript
            // make request to python api here!!!
            //statusDisplay.textContent = finalTranscript;
            //speakText(finalTranscript);
            processTranscript(finalTranscript);
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
