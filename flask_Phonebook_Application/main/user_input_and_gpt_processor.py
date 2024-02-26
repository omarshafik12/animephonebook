import speech_recognition
from openai import OpenAI
import os

client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))
####Remember to hide this and the json folder

# Set the environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'flask_Phonebook_Application//main//AI__Communication_Functionaility//animephonebook-0270dbf1ed47.json'


#recognizes and transcribes user speech into english text
def speech_reader(charac):
    recognizer = speech_recognition.Recognizer()
    try:

        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration= 0.2)
            audio = recognizer.listen(mic)
            
            user_said = recognizer.recognize_google_cloud(audio) #remember to figure out amazons rule
            user_said = user_said.lower() + ". " + f"Please write the answer in Romanji and impersonate {charac}. Also write the english translation on the next line of the romaji with 'English: ' right behind the first word" #make sure to use an f string and put the first name of the character in here.

            return user_said
    except speech_recognition.UnknownValueError as e:
        recognizer = speech_recognition.Recognizer()
        print("Error:", e)
        return "Please Stop"
    
#accepts input via speech reader and provides a Rumaji(English way of writing Japanese) response 
def gpt_processor(user_said):
    response = ""

    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_said}],
        max_tokens=100,
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content
    return str(response)