window.addEventListener('keydown', playSound);

var keys = document.querySelectorAll('.key');
keys.forEach(function (key) {return key.addEventListener('transitionend', removeTransition);});
// each key gets an event listener called transition-end, at which point the removeTransition function is called
keys.forEach(function (key) {return key.addEventListener('click', playSound);});

function playSound(e) {
    var key = document.querySelector('.key[data-key="' + e.keyCode + '"]') || (this.dataset ? this.dataset.key : "");
    var audio = document.querySelector('audio[data-key="' + e.keyCode + '"]') || document.querySelector('audio[data-key="' + key + '"]');
    if (!key) return; // stops function
    audio.currentTime = 0; //rewind audio
    audio.play();
    (key.classList || this.classList).add('playing');
}

function playSoundMidi(k) {
    var key = document.querySelector('.key[data-key="' + k + '"]') || (this.dataset ? this.dataset.key : "");
    var audio = document.querySelector('audio[data-key="' + k + '"]') || document.querySelector('audio[data-key="' + key + '"]');
    if (!key) return; // stops function
    audio.currentTime = 0; //rewind audio
    audio.play();
    (key.classList || this.classList).add('playing');

}
function removeTransition(e) {
    if (e.propertyName !== 'transform') return; // skip if property name is not transform
    this.classList.remove('playing'); // 'this' is what got called against in the event listener, so 'key'
}

/**
* audioQuadFilter module
*/
$("#audioFilter").change(function () {
    playNote(100);
    for (var i = 0; i < nodes.length; i++) {
        nodes[i].node.stop(0);
    }
});

var saveResult = function (data) {
    from = data.from;
};
$("#audioFilterFreq").ionRangeSlider({
    min: 0,
    max: 3000,
    from: 1500,
    prefix: "freq ",
    onStart: function (data) {
        saveResult(data);
    },
    onChange: saveResult,
    onFinish: saveResult
});

/**
* audioGain slider
*/
$("#audioGain").change(function () {
    playNote(100);
    for (var i = 0; i < nodes.length; i++) {
        nodes[i].node.stop(0);
    }
});

var saveGain = function (data) {
    fromGain = data.from;
};
$("#audioGain").ionRangeSlider({
    min: 0,
    max: 1,
    from: 0.5,
    step: 0.01,
    prefix: "vol ",
    onStart: function (data) {
        saveGain(data);
    },
    onChange: saveGain,
    onFinish: saveGain
});

// KEYBOARD
var frequencyByKeyPad = {
    48: 261.626, // C3
    49: 277.183, // C#3
    50: 293.665, // D3
    51: 311.127, // D#3
    52: 329.628, // E3
    53: 349.228, // F3
    54: 369.994, // F#3
    55: 391.995, // G3
    56: 415.305, // G#3
    57: 440.000, // A3
    58: 466.164, // A#3
    59: 493.883, // B3
    60: 523.251, // C4
    61: 554.365, // C#4
    62: 587.330, // D4
    63: 622.254, // D#4
    64: 659.255, // E4
    65: 698.456, // F4
    66: 739.989, // F#4
    67: 783.991, // G4
    68: 830.609, // G#4
    69: 880.000, // A4
    70: 932.328, // A#4
    71: 987.767, // B4
    72: 1046.500, // C5
    100: null //change
};
var context = new AudioContext(),
gain = context.createGain(),
nodes = [];
gain.gain.value = 0.5;
gain.connect(context.destination);

function playNote(note) {
    var osc = context.createOscillator();
    osc.type = "sawtooth";
    try {
        osc.frequency.value = frequencyByKeyPad[note];
        osc.connect(gain);
        try {
            osc.start(0);
        } catch (e) {}
        nodes.push({
            code: note,
            node: osc
        });
    } catch (e) {
        console.log("Wrong key!");
    }

    var biquadFilter = context.createBiquadFilter();
    biquadFilter.type = "allpass";
    biquadFilter.frequency.value = 1000;
    biquadFilter.gain.value = 40;
    osc.disconnect();
    osc.connect(gain);

    switch ($("#audioFilter").children(".active").text()) {
        case "no filter":
        osc.disconnect();
        osc.connect(gain);
        break;
        case "lowpass":
        osc.disconnect();
        osc.connect(biquadFilter);
        biquadFilter.connect(gain);
        biquadFilter.type = "lowpass";
        biquadFilter.frequency.value = 180;
        break;
        case "highpass":
        osc.disconnect();
        osc.connect(biquadFilter);
        biquadFilter.connect(gain);
        biquadFilter.type = "highpass";
        biquadFilter.frequency.value = 1200;
        break;
    }
    biquadFilter.frequency.value = from;
    gain.gain.value = fromGain;
    if (true) {

    }
}

// MIDI GESTION

var midi, data;
// request MIDI access
if (navigator.requestMIDIAccess) {
    navigator.requestMIDIAccess({
        sysex: false
    }).then(onMIDISuccess, onMIDIFailure);
} else {
    alert("No MIDI support in your browser.");
}

// midi functions
function onMIDISuccess(midiAccess) {
    // when we get a succesful response, run this code
    midi = midiAccess; // this is our raw MIDI data, inputs, outputs, and sysex status

    var inputs = midi.inputs.values();
    // loop over all available inputs and listen for any MIDI input
    for (var input = inputs.next(); input && !input.done; input = inputs.next()) {
        // each time there is a midi message call the onMIDIMessage function
        input.value.onmidimessage = onMIDIMessage;
    }
}

function onMIDIFailure(error) {
    // when we get a failed response, run this code
    console.log("No access to MIDI devices or your browser doesn't support WebMIDI API. Please use WebMIDIAPIShim " + error);
}

function onMIDIMessage(message) {
    data = message.data; // this gives us our [command/channel, note, velocity] data.
    // console.log('MIDI data', data); // MIDI data [144, 63, 73]
    if(data[1]==48 && data[0]==145) {playSoundMidi(49);}
    if(data[1]==49 && data[0]==145) {playSoundMidi(50);}
    if(data[1]==50 && data[0]==145) {playSoundMidi(51);}
    if(data[1]==51 && data[0]==145) {playSoundMidi(52);}
    if(data[1]==44 && data[0]==145) {playSoundMidi(53);}
    if(data[1]==45 && data[0]==145) {playSoundMidi(54);}
    if(data[1]==46 && data[0]==145) {playSoundMidi(55);}
    if(data[1]==47 && data[0]==145) {playSoundMidi(56);}
    if(data[1]==36 && data[0]==145) {playSoundMidi(57);}

    if(data[0]==144) {
        playNote(data[1]);
    }
    if(data[0]==128) {
        for (var i = 0; i < nodes.length; i++) {
            if (nodes[i].code === data[1]) {
                nodes[i].node.stop(0);
            }
        }
    }

    if(data[1]==1) {
        from=data[2]/127*3000;
        $("#audioFilterFreq").data("ionRangeSlider").update({from: from});
    }
    if(data[1]==2) {
        fromGain=data[2]/127;
        $("#audioGain").data("ionRangeSlider").update({from: fromGain});
    }
}

// COMPUTER KEYBOARD
var frequencyByKey = {
    65: 261.626, // C4
    87: 277.183, // C#4
    83: 293.665, // D4
    69: 311.127, // D#4
    68: 329.628, // E4
    70: 349.228, // F4
    84: 369.994, // F#4
    71: 391.995, // G4
    89: 415.305, // G#4
    72: 440.000, // A4
    85: 466.164, // A#4
    74: 493.883, // B4
    75: 523.251, // C5
    79: 554.365, // C#5
    76: 587.330, // D5
    80: 622.254 // D#5
};

document.addEventListener('keydown', function (event) {
    var alreadyPressed = false;
    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i].code === event.keyCode) {
            alreadyPressed = true;
            break;
        }
    }
    if (event.keyCode >= 65 && event.keyCode <= 90 && !alreadyPressed) {
        var osc = context.createOscillator();
        osc.type = "sawtooth";
        try {
            osc.frequency.value = frequencyByKey[event.keyCode];
            osc.connect(gain);
            try {
                osc.start(0);
            } catch (e) {}
            nodes.push({
                code: event.keyCode,
                node: osc
            });
        } catch (e) {
            console.log("Wrong key!");
        }

        var biquadFilter = context.createBiquadFilter();
        biquadFilter.type = "allpass";
        biquadFilter.frequency.value = 1000;
        biquadFilter.gain.value = 40;
        osc.disconnect();
        osc.connect(gain);

        switch ($("#audioFilter").children(".active").text()) {
            case "no filter":
            osc.disconnect();
            osc.connect(gain);
            break;
            case "lowpass":
            osc.disconnect();
            osc.connect(biquadFilter);
            biquadFilter.connect(gain);
            biquadFilter.type = "lowpass";
            biquadFilter.frequency.value = 180;
            break;
            case "highpass":
            osc.disconnect();
            osc.connect(biquadFilter);
            biquadFilter.connect(gain);
            biquadFilter.type = "highpass";
            biquadFilter.frequency.value = 1200;
            break;
        }
        biquadFilter.frequency.value = from;
        gain.gain.value = fromGain;
        var piano = document.getElementById("pianoId");
        for (var i = 0; i <= 24; i++) {
            var key = piano.getElementsByTagName("DIV")[i];
            if(key.dataset.numb==event.keyCode) {
                key.classList.add("piano-key-pressed");
            }
        }
    }

}, false);

document.addEventListener('keyup', function (event) {
    var garbage = [];
    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i].code === event.keyCode) {
            nodes[i].node.stop(0);
            nodes[i].node.disconnect();
            garbage.push(i);
        }
    }
    for (var i = 0; i < garbage.length; i++) {
        nodes.splice(garbage[i], 1);
    }
    var piano = document.getElementById("pianoId");
    for (var i = 0; i <= 24; i++) {
        var key = piano.getElementsByTagName("DIV")[i];
        if(key.dataset.numb==event.keyCode) {
            key.classList.remove("piano-key-pressed");
        }
    }
}, false);
