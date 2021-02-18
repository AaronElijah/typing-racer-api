# Typing Racer built with TypingDNA (Backend)

Welcome! Thanks for checking out my project. This game was built for the DeveloperWeek 2021 Hackathon TypingDNA challenge hosted by DevPost and sponsored by TypingDNA. 

## What's the game?

My game is very simple - you sign up with any username and then TypingDNA verifies your typing pattern. This is so the game can recognise who you are before signing in. Once you've signed, the aim is to type the sentences that come up to score a higher typing speed. You have to type the sentences quickly and correctly as points will be deducted if you type words wrong. If you fail to type fast enough altogether, you will fail! And if that wasn't enough of a challenge, even if you type correctly, TypingDNA must verify the typing pattern you produced from making the sentence. If TypingDNA doesn't think that it was you, then you fail!

## Why did you make this game?

I have always been a fan of type racers and find them a great way to improve keyboard speed and stop silly errors creeping into my documents and blog posts. Once I heard about TypingDNA figuring out a way to record and verify someone based on the way they type on their keyboard, I knew that I had to give it a try

## How did you build it?

* I used [FastAPI](https://fastapi.tiangolo.com/) to create the backend
* The frontend [client](https://github.com/AaronElijah/typing-racer-client) was built in ReactJS.

## Will I need anything to play the game?

Just a computer with a keyboard. Follow the instructions to get yourself set up with a Free Developer account at TypingDNA (instructions on [Typing Racer API](https://github.com/AaronElijah/typing-racer-api))

## Get started with the game locally

1) Go to [TypingDNA](https://www.typingdna.com/clients/login) and sign up for a Developer Account

2) Get the `api key` and `secret key` in the development console 

3) From your `bash_profile` or `bashrc` file at the root of your system directory, add the following exported environment variables

```
export TYPING_DNA_API_KEY=<your api key>
export TYPING_DNA_SECRET_KEY=<your secret key>
```

4) Clone this repo locally and navigate to project directory

5) Do `pip install -r requirements.txt` - make sure you are running Python 3.x - I used Python 3.8 to develop this project

6) Run the command to start the server

```
uvicorn main:app --reload
```
7) Follow commands in [Typing Racer Client](https://github.com/AaronElijah/typing-racer-client) to start running the frontend



