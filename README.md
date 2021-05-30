<img src="https://i.imgur.com/uuWWP39.png" alt="jarvis banner" />

# jarvis

Jarvis is a simple IA for home automation with voice commands written in Python. Mainly based on HomeAssistant API, the
more devices you have on HomeAssistant, the more you will be able to teach to Jarvis.

**This is only the server-side of Jarvis, you can download the client [here](https://github.com/M4TH1EU/jarvis-client)
.**

### Languages

It only supports french for now, but with some changes you should be able to use english or another language.

### Compatiblity

The server can run on anything that runs Python 3+ *(linux recommended)*

## Installation

First of all, run the command `python -m pip3 install -r requirements.txt` to install the basic requirements for the
project.  
Then, you need to download a [spacy model](https://spacy.io/usage/models)
for [NLP](https://en.wikipedia.org/wiki/Natural_language_processing) (Natural Language Processing). Go to the
spacy [website](https://spacy.io/usage/models) and select your language, whether you want efficiency or accuracy *(
keep `spacy.load()` for the loading style)*.  
When everything is selected, the website will give you a command to install the model of your choice, copy it and run
it.

*(If you are in an development environnement, like PyCharm, you will need to go to the Python Console and
type : `import spacy` followed by `spacy.cli.download("model")` replace model by what the website gives you, must look
like `fr_core_news_sm`.)*

You should be good to go.

# Usage (Work In Progress !)
*(Warning : this is a work in progress, the documentation is far from complete, if you need/want more informations contact me on discord : ``M4TH1EU_#0001``)*

To run the server, type the command :  
`python server.py`

To train the model with your intents run :  
`python server.py train`  
*(Warning : You will need to train your model every time you add new intents)*

# Intents

Jarvis uses intents to execute actions, an intent looks like this :

```json
{
  "tag": "turn_on_tv",
  "service": "homeassistant/switch/turn_on",
  "data": {
    "entity_id": "switch.tv_philips"
  },
  "patterns": [
    "turn on the tv",
    "please turn on the tv",
    "could you turn on the tv",
    "could you please turn on the television"
  ],
  "responses": [
    "Turning on the TV",
    "I'm turning on the TV sir",
    "The TV is starting ",
    "Turning on the television"
  ]
}
```

Let's split that and explain it

## Tag

```json 
"tag": "turn_on_tv"
```

The tag is like the ID of your intent, it is used to retrieve informations about the intent later in the code, like
retriving the service.

## Service

```json 
"service": "homeassistant/switch/turn_on"
```

The service is used to specify what the intent should do, an intent without service is just gonna return a random
responses specified below, won't do anything else. There are 2 types of service for now, ``jarvis``
and ``homeassistant`` *(and ``homeassistant$``)*

### Jarvis services

The jarvis services are "home-made" services, there is a few available by default :

#### Client

```json 
service: "jarvis/client/play_sound"
requires in data: 
  sound_name : str
```

#### Jokes

```json 
service: "jarvis/jokes/random"
no data required
```

#### Spotify

```json 
service: "jarvis/spotify/play_a_song"
requires in data: 
  sentence: true
```

#### Wiki

```json 
service: "jarvis/wiki/search_wikipedia"
requires in data: 
  sentence: true
```

### HomeAssistant services

HomeAssistant services are a direct call to the HomeAssistant API  
*(most of the HA API is supported, have a look at ``POST /api/services/<domain>/<service>`` [here](https://developers.home-assistant.io/docs/api/rest/))*  

Here are a few examples :
#### Light

```json 
service: "homeassistant/light/turn_on"
service: "homeassistant/light/turn_off"
service: "homeassistant/light/toggle"

requires in data:
  entity_id: str
```

#### Media Player
```json 
service: "homeassistant/media_player/media_next_track"
service: "homeassistant/media_player/media_previous_track"

requires in data:
  entity_id: str
```

## Data
```json 
"data": {
   "entity_id": "switch.tv_philips"
}
```
Data is where you will pass the args for your request, let's take for example I want to send a notification on my phone with HomeAssistant notify service.  
Under Service in development tools, for the notify service, it asks for ``title`` and ``message`` so in my intent I will write this :
```json 
"service": "homeassistant/notify/mobile_app_phone"
"data": {
   "message": "This is my notification message",
   "title": "This is the title of my notification"
}
```

## Patterns
```json 
"patterns": [
    "turn on the tv",
    "please turn on the tv",
    "could you turn on the tv",
    "could you please turn on the television"
]
```
Patterns are just sentences you would say to do a specific action.  
The above patterns are for turning ON the TV, as you can see there's only 4 sentences.  
Fortunately there is no need to say exactly what is written into the patterns, after training your model (see at the top) it will be possible to say e.g. ``turn the television on`` or ``please could you turn the television on`` and Jarvis will understand it.  
If he don't then just add the sentence he didn't understand to the actuals patterns and retrain your model.

## Responses
Responses are what Jarvis will say after doing an action.
```json 
"responses": [
    "Turning on the TV",
    "I'm turning on the TV sir",
    "The TV is starting ",
    "Turning on the television"
]
```
Here, Jarvis will select a random response and speak it after turning on the TV

```
Me      :  Hey Jarvis ?  
Jarvis  :  *listening sound*
Me      :  Turn on the TV
Jarvis  :  I'm turning on the TV sir
```