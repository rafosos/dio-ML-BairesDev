import speech_recognition as sr
from gtts import gTTS
import os
import playsound
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read,user-read-currently-playing,streaming,user-read-playback-state,user-modify-playback-state,app-remote-control,playlist-read-private,playlist-read-collaborative"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope=scope,
    client_id="",
    client_secret="",
    redirect_uri="http://localhost:3000"
))

#get mic audio
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        # wait for a second to let the recognizer adjust the
        # energy threshold based on the surrounding noise level
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(said)
        except sr.UnknownValueError:
            speak("Sorry, I did not get that.")
        except sr.RequestError:
            speak("Sorry, the service is not available")
    return said.lower()

#speak converted audio to text
def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = ".\\voice.mp3"
    try:
        os.remove(filename)
    except OSError:
        pass
    tts.save(filename)
    playsound.playsound(filename)

#function to respond to commands
def respond(text: str):
    print("Text from get audio: " + text)

    if "open" in text:
        os.startfile("C:\\Users\\<<USERNAME>>/\\AppData\\Local\\Microsoft\\WindowsApps\\Spotify.exe")
    elif text.startswith("play"):
        song_name = text.removeprefix("play ")
        if "current" in text or "a song" in text or "music" in text:
            speak("Playing current song.")
            sp.start_playback()
        else:
            res = sp.search(q=song_name, market="BR", limit=1)
            if len(res["tracks"]):
                speak(f"Playing {song_name}")
                sp.start_playback(uris=[res["tracks"]["items"][0]["uri"]])
            else:
                speak("I couldn't find the desired song, please try again")
    elif "stop" in text or "pause in text":
        sp.pause_playback()
        speak("Stopping playback")
    elif 'exit' in text or "close" in text:
        speak("See you later, alligator!")
        exit()

print("Hi there! I am Roger, your personal Spotify assistant. What woukd you like me to do?")
print("- Play a song: say 'play song-name'")
print("- Stop playing: say 'stop playing'")
print("- Close: say 'exit'")

while True:
    print("I am listening...")
    text = get_audio()
    respond(text)