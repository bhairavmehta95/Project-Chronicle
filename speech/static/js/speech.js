  var final_transcript = '';
  var recognizing = false;
  var ignore_onend;
  var start_timestamp;
  var recognition = new webkitSpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;

  var shownImageIndex = 0;

  recognition.onstart = function() {
    recognizing = true;
  };

  recognition.onerror = function(event) {
    if (event.error == 'no-speech') {
      ignore_onend = true;
    }
    if (event.error == 'audio-capture') {
      ignore_onend = true;
    }
    if (event.error == 'not-allowed') {
      if (event.timeStamp - start_timestamp < 100) {
        showInfo('info_blocked');
      } else {
        showInfo('info_denied');
      }
      ignore_onend = true;
    }
  };

  recognition.onend = function() {
    recognizing = false;
    if (ignore_onend) {
      return;
    }
    
    if (!final_transcript) {
      showInfo('info_start');
      return;
    }
    showInfo('');
    if (window.getSelection) {
      window.getSelection().removeAllRanges();
      var range = document.createRange();
      range.selectNode(document.getElementById('final_span'));
      window.getSelection().addRange(range);
    }
  };

  recognition.onresult = function(event) {
    var interim_transcript = '';
    if (typeof(event.results) == 'undefined') {
      recognition.onend = null;
      recognition.stop();
      upgrade();
      return;
    }
    for (var i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        final_transcript += event.results[i][0].transcript + '. ';
      } else {
        interim_transcript += event.results[i][0].transcript;
      }
    }

    try {
        final_transcript_list = final_transcript.match(/[^\.!\?]+[\.!\?]+/g);

        final_transcript = "";

        for (i = 0; i < final_transcript_list.length; ++i) {
            final_transcript = final_transcript + capitalize(final_transcript_list[i]);
        }
    }

    catch(err){
      final_transcript = capitalize(final_transcript);
    }

    final_span.innerHTML = linebreak(final_transcript);
    interim_span.innerHTML = linebreak(interim_transcript);
  };

  var two_line = /\n\n/g;
var one_line = /\n/g;
function linebreak(s) {
  return s.replace(two_line, '<p></p>').replace(one_line, '<br>');
}

var first_char = /\S/;
function capitalize(s) {
  return s.replace(first_char, function(m) { return m.toUpperCase(); });
}
  
  function startButton(event) {
    if (recognizing) {
      recognition.stop();
      return;
    }

    final_transcript = '';
    recognition.start();
    ignore_onend = false;
    final_span.innerHTML = '';
    interim_span.innerHTML = '';
    showInfo('info_allow');
    showButtons('none');
    start_timestamp = event.timeStamp;
  }

///END BHAIRAV ADDITIONS


$(document).ready(function() {
  bindEvents();
  Data.TimerState = 'New'
  Data.TotalSeconds = '0';
  getImages();
});

function bindEvents() {
  $(document).on('click', '#recordButton', function() {
    Functions.RecordButton.Click();
    startButton();
  })
  $(document).on('click', '#submitButton', function () {
      if (Data.TimerState == "Stopped") {
          document.getElementById("final_transcript").value = final_transcript;
          document.getElementById("form_transcript").submit();
      }
  })
}

var HTML = {
  get TimerSeconds() {
    return $("#seconds");
  },
  get TimerMinutes() {
    return $("#minutes");
  },
  get RecordButton() {
    return $('#recordButton');
  },
  get Timer() {
    return $('#recordTimer');
  },
  get SubmitButton() {
    return $('#submitButton');
  }
}

var Data = {
  get TotalSeconds() {
    return this._seconds;
  },
  set TotalSeconds(seconds) {
    this._seconds = seconds
  },
  get TimerState() {
    return this._timerState;
  },
  set TimerState(state) {
    this._timerState = state;
  }
}

function pad(val) {
}

var Functions = {

  RecordButton: {
    Click: function() {
      switch(Data.TimerState) {
        case 'New':
          HTML.RecordButton.html('<i class="circle icon"></i>Recording');
          break;
        case 'Recording':
          HTML.RecordButton.html('<i class="refresh icon"></i> Start Over');
          break;
        case 'Stopped':
          HTML.RecordButton.html('<i class="circle icon"></i>Recording');
          break;
      }
      Functions.Timer.Set();
    }
  },
  
  Timer: {
    Interval: {},
    Set: function() {
      (Data.TimerState);
      switch (Data.TimerState) {
        case 'New':
          Functions.Timer.Start();
          Data.TimerState = 'Recording';
          break;
        case 'Recording':
          Functions.Timer.Stop();
          Data.TimerState = 'Stopped'
          HTML.SubmitButton.removeClass('disabled');
          break;
        case 'Stopped':
          Functions.Timer.Start();
          Data.TimerState = 'Recording'
          HTML.SubmitButton.addClass('disabled');
          break;
      }
    },
    Start: function() {
      clearInterval(Functions.Timer.Interval);
      HTML.TimerSeconds.html('00');
      HTML.TimerMinutes.html('00');
      Data.TotalSeconds = '0';
      Functions.Timer.Interval = window.setInterval(function() {
        Data.TotalSeconds++;
        
        HTML.TimerSeconds.html(Functions.Pad(parseInt(Data.TotalSeconds) % 60));
        HTML.TimerMinutes.html(Functions.Pad(parseInt(Data.TotalSeconds / 60, 10) % 60));
      }, 1000);
    },
    Stop: function() {
      clearInterval(Functions.Timer.Interval);
    }
  },
  Pad: function(val) {
    return val > 9 ? val : "0" + val;
  }
}

function getImages() {
  var imageContainer = $('.images.container');
  var images = imageContainer.find('img');
  images.each((index, img) => {
    $(img).hide();
  })
  images.eq(shownImageIndex).show();
}

function nextImage() {
  var imageContainer = $('.images.container');
  var images = imageContainer.find('img');
  images.eq(shownImageIndex).hide();
  shownImageIndex++;
  if (shownImageIndex >= images.length) shownImageIndex = 0;
  images.eq(shownImageIndex).show();
}