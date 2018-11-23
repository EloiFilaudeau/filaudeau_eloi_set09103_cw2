(function (window, document, undefined) {

    var notes, midi, currentInput;

    function onMidiMessage(msg) {
        var action = isNoteOffMessage(msg) ? 'remove' :
        isNoteOnMessage(msg) ? 'add' : null,
        noteDiv;

        if (action && (noteDiv = getNoteDiv(msg))) {
            noteDiv.classList[action]('piano-key-pressed');
        }
    }

    var MIDI_A0_NUM = 48;

    // return div from key pressed
    function getNoteDiv(msg) {
        var noteNum = getMessageNote(msg) - MIDI_A0_NUM;

        if (notes && 0 <= noteNum && noteNum < notes.length) {
            return notes[noteNum];
        }
    }

    var CMD_NOTE_ON = 9;
    var CMD_NOTE_OFF = 8;

    function isNoteOnMessage(msg) {
        return getMessageCommand(msg) == CMD_NOTE_ON;
    }

    function isNoteOffMessage(msg) {
        var cmd = getMessageCommand(msg);
        return cmd == CMD_NOTE_OFF ||
        cmd == CMD_NOTE_ON && getMessageVelocity(msg) == 0;
    }

    function getMessageCommand(msg) {return msg.data[0] >> 4;}
    function getMessageNote(msg) {return msg.data[1];}
    function getMessageVelocity(msg) {return msg.data[2];}

    function selectInput(input) {
        if (input != currentInput) {
            if (currentInput) {
                currentInput.removeEventListener('midimessage', onMidiMessage);
                currentInput.close();
            }

            input.addEventListener('midimessage', onMidiMessage);
            currentInput = input;
        }
    }

    function populateInputList() {
        var inputs = Array.from(midi.inputs.values());

        if (inputs.length == 1) {
            selectInput(inputs[0]);
        } else {
            // TODO: handle multiple MIDI inputs
        }
    }

    // if browser support midi and device connected
    function onMIDIAccessSuccess(access) {
        midi = access;
        access.addEventListener('statechange', populateInputList, false);
        populateInputList();
    }
    // if browser doesn't support midi or device not connected
    function onMIDIAccessFail() {
        console.error('Request for MIDI access was denied!');
    }

    if ('requestMIDIAccess' in window.navigator) {
        window.navigator.
        requestMIDIAccess().
        then(onMIDIAccessSuccess, onMIDIAccessFail);
    } else {
        console.error("No access to MIDI devices or your browser doesn't support WebMIDI API. Please use WebMIDIAPIShim on Chrome");
    }

    document.addEventListener('DOMContentLoaded', function () {
        notes = document.getElementsByClassName('piano-key');
    }, false);

})(window, window.document);
