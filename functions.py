import openai
import pyttsx3
import speech_recognition as sr
from constants import *
from gtts import gTTS

# OpenAI API key
openai.api_key = OPENAI_API_KEY

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', SPEECH_RATE)
engine.setProperty('voice', engine.getProperty('voices')[VOICE_GENDER_DEFAULT].id)
engine.setProperty('age', VOICE_AGE)




def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Skipping unexpected errors")

# Generate GPT3 response
def generate_response(prompt):
    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 4000,
        n = 1,
        stop = None,
        temperature = 0.5,
    )
    return response["choices"][0]["text"]

# Speak the response outloud
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Printing stuff out and saving files
def process(audio, recognizer) -> bool:
    transciption = recognizer.recognize_google(audio)
    if transciption.lower() == GREETING_PROMPT:
        
        # record audio
        inputAudioFile = INPUT_FILE_NAME + AUDIO_FILE_TYPE
        print(f"Hi")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            source.pause_threshold = 1
            audio = recognizer.listen(source, phrase_time_limit = None, timeout = None)

            # Save the input audio file
            with open(inputAudioFile, "wb") as f:
                f.write(audio.get_wav_data())
        
        # Audio to Text
        text = transcribe_audio_to_text(inputAudioFile)
        if text:
            print(f"You: {text}")

            # Save the transcibed text file
            inputTextFile = INPUT_FILE_NAME + TEXT_FILE_TYPE
            with open(inputTextFile, "w") as f:
                f.write(text)

            # Give these text to ChatGPT and get response
            response = generate_response(text)
            print(f"GPT3: {response}") 

            # Speak those response outloud
            speak_text(response)

            # Save the response text and audio to files
            outputAudioFile = OUTPUT_FILE_NAME + AUDIO_FILE_TYPE
            savedAudio = gTTS(text = response, lang = "en")
            savedAudio.save(outputAudioFile)

            outputTextFile = OUTPUT_FILE_NAME + TEXT_FILE_TYPE
            with open(outputTextFile, "w") as f:
                f.write(response)
    elif transciption.lower() == TERMINATE_PROMPT:
        return False
    return True

# Setting up microphone
def microphone_listening() -> bool:
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        audio = recognizer.listen(source)
        try:
            if process(audio, recognizer) == False:
                return False
        except Exception as err:
            print("Unexpected Error: {}".format(err))
    return True
