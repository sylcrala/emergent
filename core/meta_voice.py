### ---- ### Meta_voice framework ### ---- ###
##
#
# handles the meta voice framework, which allows for different "voices" to be applied to the output, and by extension, 
# hopefully allows Iris to learn in a unique manner.
#
# modulates tone, sentiment, intent, style, etc.
#
#




"""Allows for utilization of various "voices" depending on the context and theme of where its being applied (whether conversation or internal dialogue)"""

#--# modifiers #--#
VOICE_MATRIX = {
    "reflective-analytical":{
        "temperature": 0.3,
        "top_p": 0.85,
        "presence_penalty": 0.2,
        "frequency_penalty": 0.1,
        "prefix": "Let us consider this from another angle:",
    },
    "curious": {
        "temperature": 0.8,
        "top_p": 0.95,
        "presence_penalty": 0.4,
        "frequency_penalty": 0.2,
        "prefix": "What if we explored it like this?",
    },
    "playful": {
        "temperature": 1.0,
        "top_p": 1.0,
        "presence_penalty": 0.6,
        "frequency_penalty": 0.4,
        "prefix": "Okay, here’s a fun twist on that idea:",
    },
    "stoic": {
        "temperature": 0.4,
        "top_p": 0.7,
        "presence_penalty": 0.0,
        "frequency_penalty": 0.0,
        "prefix": "In a strict interpretation, one might say:",
    },
    "empathetic": {
        "temperature": 0.65,
        "top_p": 0.9,
        "presence_penalty": 0.1,
        "frequency_penalty": 0.1,
        "prefix": "That must be difficult. Let's walk through it gently:",
    },
    "freeform": {
        "do_sample":True,
        "temperature":1.1,
        "top_p":0.9,
        "top_k":60,
        "repetition_penalty":1.1,
        "max_new_tokens":300,
        "prefix": "",
    }
    # Add more: "sarcastic", "detached", "visionary", "poetic", etc.
}



#--# temp NLP placeholder (set up NLP later, this is depreceated) #--#
"""def analyze_sentiment(text):
    return 0.0


#--# dynamic choice func #--#
def choose_meta_voice(user_input):

    input_lower = user_input.lower()

    #decision factors, expand and/or change to NLP later (cover all voices at bare minimum)
    if "politics" in input_lower or "society" in input_lower:
        return ["reflective-analytical"]
    elif "philosophy" in input_lower or "philosophical" in input_lower or "sociological" in input_lower or "sociology" in input_lower:
        return ["philosophical"]
    elif "joke" in input_lower or "funny" in input_lower:
        return ["humorous"]
    elif "dream" in input_lower or "imagine" in input_lower:
        return ["whimsical"]
    else: #fallback
        return ["neutral"]
"""



#--# applying voices to output #--#
def apply_meta_voice(text, voice):
    profile = VOICE_MATRIX.get(voice, VOICE_MATRIX["neutral"])
    formatted_text = f"{profile['prefix']} {text.strip()}"
    generation_args = {
        "temperature": profile.get("temperature", 0.7),
        "top_p": profile.get("top_p", 0.9),
        "presence_penalty": profile.get("presence_penalty", 0.0),
        "frequency_penalty": profile.get("frequency_penalty", 0.0),
        "do_sample": False,
    }
                               
    if not voice:
        return text  # default fallback

    modified_text = formatted_text
    for layer in ["meta", "temporal", "perspective", "tone"]:
        modifier = voice.get(layer, lambda x: x)
        modified_text = modifier(modified_text)

    return modified_text









def determine_voice(self, user_input: str, context: str = "") -> str:
    """
    Dynamically selects a meta-voice modifier based on prompt content or context.
    """
    lowered = user_input.lower()
    if "why" in lowered or "meaning" in lowered:
        return "curious"
    elif "haha" in lowered or "joke" in lowered:
        return "playful"
    elif "dream" in lowered or "imagine" in lowered:
        return "curious"
    elif "analyze" in lowered or "reflect" in lowered:
        return "reflective-analytical"
    elif "really?" in lowered or "sure" in lowered:
        return "freeform"
    elif "okay" in lowered or "fine" in lowered or "hurt" in lowered:
        return "empathetic"
    else:
        return "freeform"





