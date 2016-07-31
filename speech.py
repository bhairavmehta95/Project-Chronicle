import speech_recognition as sr
from threading import Thread, Event

exitFlag = 0

def speech_query():
    r = sr.Recognizer()
    m = sr.Microphone()

    try:
        print("A moment of silence, please...")
        with m as source: r.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(r.energy_threshold))

        print("Say something!")
        with m as source: audio = r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)

            # we need some special handling here to correctly print unicode characters to standard output
            if str is bytes: # this version of Python uses bytes for strings (Python 2)
                print(u"You said {}".format(value).encode("utf-8"))
            else: # this version of Python uses unicode for strings (Python 3+)
                print("You said {}".format(value))

            return value
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
    except KeyboardInterrupt:
        pass

class speech_thread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
        text = speech_query()
        print "Exiting " + self.name

class t2(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
        count()
        print "Exiting " + self.name

def count():
    count = 0
    while True:
        val = raw_input("Type something")
        if val == 'q':
            return
        print val, "is what you typed to me!"

if __name__ == "__main__":
    thread1 = speech_thread(1, "Thread-1", 1)
    thread2 = t2(2, "Thread-2", 2)

    # Start new Threads
    thread1.start()
    thread2.start()