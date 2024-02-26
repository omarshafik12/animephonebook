import fakeyou
import os
from user_input_and_gpt_processor import speech_reader, gpt_processor
import pygame
import time




fake_you = fakeyou.FakeYou()

folder_path = "main\AI__Communication_Functionaility\audioo"
class Talk:
    def __init__(self, username, password, model_name):
        self.username = username
        self.password = password
        self.model_name = model_name

    def login_to_fakeyou(self):
        fake_you.login(self.username, self.password)
    
    def generate_audio(self, text, tm_tokens): #You are gonna need to add a variable for what gpt returns here
        
        # Assuming fake_you.say() returns an instance of the wav class
        wav_instance = fake_you.say(text=text, ttsModelToken=tm_tokens)
        # Call hjson_info method on the instance
        file_name = wav_instance.hjson_info()

        wav_file_path = file_name['state']['maybe_public_bucket_wav_audio_path']

        # Extract the WAV file name from the file path
        wav_file_name = wav_file_path.split('/')[-1]

        folder_path = f"flask_Phonebook_Application\\main\\AI__Communication_Functionaility\\audioo\{wav_file_name}" 

        full_path = os.path.abspath(folder_path)


        # Perform the file rename operation
        pygame.init()
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.play()
        #Omar keep in mind that it works now having the playsound play the specific file path, but be careful since that might not work when you deploy it.
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        
        pygame.mixer.music.stop()

        pygame.mixer.quit()

        os.remove(folder_path)
        return 'complete'