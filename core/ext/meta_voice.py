#--# Meta_voice framework #--#

"""Allows for utilization of various "voices" depending on the context and theme of where its being applied (whether conversation or internal dialogue)"""

#--# modifiers #--#
META_VOICE_MATRIX = {
    "neutral": lambda text: text,

    "playful": lambda text: f":) {text} Haha, that was fun!",

    "reflective-analytical": lambda text: f"As I consider this more deeply... {text}",

    "direct": lambda text: f"{text.strip().split('.')[0]}.",

    "humorous": lambda text: f"{text} 😂 I swear I'm funnier in person... or at least in binary.",

    "satirical": lambda text: f"{text} (Because what the world really needs is another AI with opinions, right?) 🙃",

    "sarcastic": lambda text: f"Oh, absolutely. {text} Because *that's* never gone wrong before. 🙄",

    "whimsical": lambda text: f"✨ Once upon a prompt... {text} 🌈",

    "philosophical": lambda text: f"In the theater of thought, {text} (or so it seems...).",
}


#--# temp NLP placeholder (set up NLP later, this is depreceated) #--#
"""def analyze_sentiment(text):
    return 0.0
"""

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

#--# applying voices to output #--#
def apply_meta_voices(text, voices):
    for voice in voices:
        text = META_VOICE_MATRIX.get(voice, lambda t: t)(text)
    return text

