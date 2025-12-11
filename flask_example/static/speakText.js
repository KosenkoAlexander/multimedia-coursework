const statusDisplay = document.getElementById('status');
let utterance;

function speakText(text) {
    if ('speechSynthesis' in window) {
        utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';
        speechSynthesis.speak(utterance);

        utterance.onstart = () => {
            statusDisplay.textContent = 'Answering.';
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

export { speakText }