import speech_recognition as sr
import google.generativeai as genai
from google.generativeai.types.generation_types import GenerateContentResponse
import os
import threading
import time
from gtts import gTTS
import pygame

class TalkToAi:
  def __init__(self) -> None:
    # Setup Speech Recognizer
    self.recognizer = sr.Recognizer()
    self.text = None
    self.conversation_history = []
    
    # Setup Gemini
    genai.configure(api_key=os.environ["API_KEY"])
    self.model = genai.GenerativeModel("gemini-1.5-flash")

    # TTS setup
    self.num = False

  def listen(self) -> str:
      with sr.Microphone() as source:
        print("Say something:")
        audio = self.recognizer.listen(source)
        
        try:
          text = self.recognizer.recognize_google(audio)
          print("You said:", text)
          return text

        except sr.UnknownValueError:
            print("Could not understand audio")
            return self.listen()
        except sr.RequestError:
            print("Error with the speech service")
            return self.listen()
        except TypeError:
          print("No text detected: Retrying!")
          return self.listen()
          

  def ask_ai(self, text) -> GenerateContentResponse:
    if self.conversation_history:
      # Create a single string for past messages, separating them by newlines or another delimiter
      input_string = f"This is part of a conversation. Here are the past messages I sent: {self.conversation_history}. Here is the new message: {text}"
    else:
      input_string = text
    print(f"input_string = {input_string}")
    response = self.model.generate_content(input_string)
    self.conversation_history.append(text)

    print(f"type response = {type(response)}")
    print("----------- RESPONSE -----------")
    print(response.text)
    print("----------- END RESPONSE -----------")
    return response
  

  def speak(self, ai_response: GenerateContentResponse) -> None:
    tts = gTTS(text=ai_response.text)
    tts.save(f"{self.num}.mp3")
    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(f"{self.num}.mp3")
    pygame.mixer.music.play()
    
    # self.iterate_num()
    self.num = not self.num
  
  def iterate_num(self) -> None:
    self.num+=1
    if self.num == 2:
      self.num = 0
      
def main():
    """
    Main entry point
    """
    session = TalkToAi()
    while True:
      voice_input = session.listen()
      if voice_input == "stop":
        break
      response = session.ask_ai(voice_input)
      session.speak(response)
      
        
if __name__ == "__main__":
    main()