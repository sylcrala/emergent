### ---- ### Routing functions (memory and reflection) ### ---- ###
##
#
# Directs all input/output flow to the appropriate layer of the system.
#




from core._logger import logger, SYSTEM_LEVEL
from core.memory_framework import MemoryIO
from core.core import load_config
from core.meta_voice import apply_meta_voice



class Router:
    def __init__(self, conscious_model, subconscious_model, memory):
        self.mistral = conscious_model
        self.pixtral = subconscious_model
        self.memory = memory


    def determine_voice(self, user_input: str, context: str = "") -> str:
        """
        Dynamically selects a meta-voice modifier based on prompt content or context.
        """
        lowered = user_input.lower()
        if "why" in lowered or "meaning" in lowered:
            return "philosophical"
        elif "haha" in lowered or "joke" in lowered:
            return "humorous"
        elif "dream" in lowered or "imagine" in lowered:
            return "whimsical"
        elif "analyze" in lowered or "reflect" in lowered:
            return "reflective-analytical"
        elif "really?" in lowered or "sure" in lowered:
            return "sarcastic"
        elif "okay" in lowered or "fine" in lowered:
            return "direct"
        else:
            return "neutral"

    
    def route(self, user_id: str, username, user_input: str, model_type: str) -> str:
        """
        Routes the user input to the appropriate model based on the model type.
        """
        short_term = self.memory.get_short_term(user_id)
        long_term = self.memory.get_long_term(user_id)

        #letting iris select a voice
        selected_voice = self.determine_voice(user_input)

        #conscious model live context (via active user) and generate response
        conscious_prompt = f"[Context]\n{short_term}\n[User]\n{user_input}\n[Iris]\n"
        modulated_conscious_prompt = apply_meta_voice(conscious_prompt, selected_voice)
        logger.log(SYSTEM_LEVEL, f"Selected voice = {selected_voice}")
        response = self.mistral.generate(modulated_conscious_prompt)

        #subconscious model access full memory bank and utilizes reflection framework + more
        reflection_prompt = f"[User_ID]\n{user_id}\n[Username]\n{username}\n[{username} input]\n{user_input}\n[Short Term Memory]\n{short_term}\n[Long Term Memory]\n{long_term}\n[Iris]\n"
        modulated_subconscious_thought = apply_meta_voice(reflection_prompt, selected_voice)
        subconscious_thought = self.pixtral.generate(reflection_prompt)


        self.memory.append(user_id, username, user_input, subconscious_thought)

        
        return response