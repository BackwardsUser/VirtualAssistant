import regex as re
import speech_recognition as sr
from func import get_time, get_phrase, all_phrase_banks
from weather import get_weather
from elevenlabs import generate, play

f = open("token.txt")
token = f.readline()

voices = [
    [
        [ "George", "eleven_multilingual_v2" ]
    ],
    [
        [ "Alice", "eleven_turbo_v2" ]
    ]
]

def tts(text="Sorry, it seems I've forgotten what I was going to say..")
    audio = generate(
        api_key=token,
        text=text,
        voice=voice[1][0],
        model="eleven_turbo_v2"
    )

    play(audio)

    return text


Running = True


def callback(recgonizer, audio):
    global Running
    print("Voice detected")
    print("Running voice through recognizer.")
    voice = r.recognize_sphinx(audio)
    print("Heard: " + voice)

    last = ""

    if re.search(r"(^good\s?(night|bye)$){e<=2}", voice):
        tts(get_phrase("Phrase Bank/goodbye.txt"))
        stop_listening(wait_for_stop=False)
        Running = False
    if re.search(r"(^((what'?s?)|(how'?s?)).*(weather)){e<=2}", voice):
        last =tts(get_weather())
        return
    if re.search(r"(^(what'?s?).*(time).*){e<=2}", voice):
        last = tts(f"It is currently {get_time()}")
        return
    if re.search(r"(^pardon$|(could|what (did|was that))\s*(you (repeat|say))?){e<=2}", voice):
        if last == "":
            last = "I haven't said anything yet. "
        tts(last)
        return


r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)
    print("Adjustment Made")

tts(get_phrase("Phrase Bank/intro.txt"))
print("Listening...")
stop_listening = r.listen_in_background(m, callback)

while Running:
    pass
