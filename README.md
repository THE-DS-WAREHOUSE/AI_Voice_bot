Here is a custom README.md file tailored specifically to your AI restaurant receptionist project. You can copy and paste this directly into your project folder.

Markdown
# Happy Meat AI Receptionist

A real-time, voice-activated AI assistant designed to act as a receptionist for a fictional New York steakhouse called "Happy Meat." 

This project captures audio from your microphone, transcribes it in real-time, generates a conversational AI response based on a specific prompt, and streams the response back to you as high-quality synthesized speech.

## Features

* **Real-time Speech-to-Text:** Uses AssemblyAI to transcribe user microphone input continuously.
* **Conversational AI:** Powered by OpenAI's `gpt-3.5-turbo` to handle reservations, ask for party sizes, and maintain a polite, efficient persona.
* **Real-time Text-to-Speech:** Uses ElevenLabs to stream natural-sounding audio responses (using the voice "Aria") back to the user without waiting for the entire response to generate.
* **Automatic Session Management:** Pauses the microphone while the AI is "speaking" and automatically terminates the program when the user says "bye" or "goodbye".

## Prerequisites

Before running this project, you will need active API keys from the following services:
* [AssemblyAI](https://www.assemblyai.com/) (For real-time transcription)
* [OpenAI](https://openai.com/) (For the ChatGPT conversational model)
* [ElevenLabs](https://elevenlabs.io/) (For AI voice generation)

You also need a working microphone and speakers connected to your computer.

## Installation

1. **Clone the repository** (or create a new folder for your project).
2. **Install the required Python packages:**

```bash
pip install assemblyai elevenlabs openai
