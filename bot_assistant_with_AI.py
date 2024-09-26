import assemblyai as aai  # assemblyAI enables audio stream and transcription in real time
from elevenlabs import generate, stream  # this enables AI answers in real time
from openai import OpenAI  # to generate a response for the audios
import os  # to access Environment Variables


class Assistant:  # AI assistant class
    def __init__(self):  # we define an assistant with:
        aai.settings.api_key = os.environ['ASSEMBLY_AI_API_KEY']  # initialize AssemblyAI API KEY
        self.openai = OpenAI(api_key=os.environ['CHAT_GPT_API_KEY'])  # initialize Open AI client with key
        self.elevenlabs_api_key = os.environ['ELEVEN_LABS_API_KEY']  # initialize elevenlabs api key

        self.transcriber = None  # empty transcriber object

        # Prompt before the conversation
        self.full_transcript = [
            {'role': "system",  # set content/context to the transcript AI
             "content": "You are a receptionist at a famous restaurant in New York called 'Happy Meat'. Be kind, "
                        "efficient, and polite."}
        ]

    def start_transcription(self):  # start transcription
        self.transcriber = aai.RealtimeTranscriber(  # real time transcriber
            sample_rate=16000,  # 16000 Hz: This means that the audio input will be sampled 16,000 times per second
            on_data=self.on_data,  # on_data method
            on_error=self.on_error,  # on_error method
            on_open=self.on_open,  # on_open method
            on_close=self.on_close  # on_closed method
        )
        self.transcriber.connect()  # activate transcriber
        microphone_steam = aai.extras.MicrophoneStream(sample_rate=16000)  # capture audio from the microphone
        self.transcriber.stream(microphone_steam)  # begins the process of streaming audio from the microphone

    def stop_transcription(self):  # stop transcription
        if self.transcriber:  # if we have a transcriber active then
            self.transcriber.close()  # close it
            self.transcriber = None  # set value to None again

    def on_open(self, session_opened: aai.RealtimeSessionOpened):  # this is to request IDs or validation data
        # print("Session ID:", session_opened.session_id)
        return

    def on_data(self, transcript: aai.RealtimeTranscript):
        if not transcript.text:  # if we do not have text in transcript
            return  # return nothing

        if isinstance(transcript, aai.RealtimeFinalTranscript):  # but if we do
            self.generate_ai_response(transcript)  # then we generate an AI response
        else:
            print(transcript.text, end="\r")  # and print the transcript text

    def on_error(self, error: aai.RealtimeError):  # is called when an error occurs during the transcription process.
        # print("An error occurred:", error)
        return

    def on_close(self):  # This function is called when the real-time transcription session is closed.
        # print("Closing Session")
        return

    def generate_ai_response(self, transcript):  # generate Response using ChatGPT

        self.stop_transcription()  # after we stop the transcription

        self.full_transcript.append({"role": "user", "content": transcript.text})  # ww add transcription to context
        print(f"\nCustomer: {transcript.text}", end="\r\n")  # print it

        response = self.openai.chat.completions.create(  # now we create a response using chatGPT
            model="gpt-3.5-turbo",  # model
            messages=self.full_transcript,  # prompt is our transcript
        )

        ai_response = response.choices[0].message.content  # we take the response

        self.generate_audio(ai_response)  # now we generate audio for the response using Eleven Labs

        self.start_transcription()  # and we start for another transcription

    def generate_audio(self, text):  # generate audio
        self.full_transcript.append({"role": "assistant", "content": text})  # use response generated as content
        print(f"\nAI Receptionist: {text}", end="\r\n")  # print the response from AI

        audio_stream = generate(  # we stream audio
            api_key=self.elevenlabs_api_key,
            model="eleven_multilingual_v2",  # model
            text=text,  # stream the text
            voice="Aria",  # voice
            stream=True  # stream
        )

        stream(audio_stream)  # stream audio


greeting = (
    "Thank you for calling 'Happy Meat', the best steakhouse in New York. My name is Rachel, how can I help you?")
ai_assistant = Assistant()
ai_assistant.generate_audio(greeting)
ai_assistant.start_transcription()
