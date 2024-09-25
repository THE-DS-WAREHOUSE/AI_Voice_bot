import assemblyai as aai
from elevenlabs import generate, stream
from openai import OpenAI
import os


class Assistant:
    def __init__(self):
        aai.settings.api_key = os.environ['ASSEMBLY_AI_API_KEY']
        self.openai = OpenAI(api_key=os.environ['CHAT_GPT_API_KEY'])
        self.elevenlabs_api_key = os.environ['ELEVEN_LABS_API_KEY']

        self.transcriber = None  # empty transcriber object

        # Prompt before the conversation
        self.full_transcript = [
            {'role': "system", "content": "You are a receptionist at a famous restaurant in New York City called "
                                          "'Quality Meats'. De kind,"
                                          "efficient and polite."}
        ]

    def start_transcription(self):
        self.transcriber = aai.RealtimeTranscriber(
            sample_rate=16000,
            on_data=self.on_data,
            on_error=self.on_error,
            on_open=self.on_open,
            on_close=self.on_close
        )

        self.transcriber.connect()
        microphone_steam = aai.extras.MicrophoneStream(sample_rate=16000)
        self.transcriber.stream(microphone_steam)

    def stop_transcription(self):
        if self.transcriber:
            self.transcriber.close()
            self.transcriber = None

    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        # print("Session ID:", session_opened.session_id)
        return

    def on_data(self, transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return

        if isinstance(transcript, aai.RealtimeFinalTranscript):
            self.generate_ai_response(transcript)
        else:
            print(transcript.text, end="\r")

    def on_error(self, error: aai.RealtimeError):
        # print("An error occurred:", error)
        return

    def on_close(self):
        # print("Closing Session")
        return

    def generate_ai_response(self, transcript):

        self.stop_transcription()

        self.full_transcript.append({"role": "user", "content": transcript.text})
        print(f"\nPatient {transcript.text}", end="\r\n")

        response = self.openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.full_transcript,
        )

        ai_response = response.choices[0].message.content

        self.generate_audio(ai_response)

        self.start_transcription()

    def generate_audio(self, text):
        self.full_transcript.append({"role": "assistant", "content": text})
        print(f"\nAI Receptionist {text}", end="\r\n")

        audio_stram = generate(
            api_key=self.elevenlabs_api_key,
            text=text,
            voice="Lily",
            stream=True
        )

        stream(audio_stram)


greeting = "Thank you for calling 'Quality Meats' New York best Steakhouse. My name is Rachel, how can I help you?"
ai_assistant = Assistant()
ai_assistant.generate_audio(greeting)
ai_assistant.start_transcription()
