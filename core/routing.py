### ---- ### Routing functions (memory and reflection) ### ---- ###
##
#
# Directs all input/output flow to the appropriate layer of the system.
#




from ext._logger import logger, SYSTEM_LEVEL
from memory_io import memIO
from ext.config_loader import main_config
from meta_voice import apply_meta_voice


config = main_config
class Router:
    def __init__(self, conscious_model, subconscious_model, memory, user_id):
        self.mistral = conscious_model
        self.pixtral = subconscious_model
        self.memory = memIO.memory_bank

        model_id = ""
        model_type = ""
        if conscious_model:
            model_id = config["conscious_model"]["id"]
            model_type = "conscious"
        elif subconscious_model:
            model_id = config["subconscious_model"]["id"]
            model_type = "subconscious"

       

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
            return "wonder"
        elif "analyze" in lowered or "reflect" in lowered:
            return "reflective-analytical"
        elif "really?" in lowered or "sure" in lowered:
            return "stoic"
        elif "okay" in lowered or "fine" in lowered or "hurt" in lowered:
            return "empathetic"
        else:
            return "freeform"

    
    def route(self, user_id: str, user_input: str, model_type: str) -> str:


        count += 1
        """
        Routes the user input to the appropriate model based on the model type.
        """
        short_term = self.memory = memIO.load_recent_context(user_id)
        long_term = self.memory = memIO.load_memory(user_id)



        #letting iris select a voice
        selected_voice = self.determine_voice(user_input) #select initial voice

        #conscious model live context (via active user) and generate response
        conscious_prompt = f"[Context]\n{short_term}\n[User]\n{user_input}\n[Iris]\n"
        modulated_conscious_prompt = apply_meta_voice(conscious_prompt, selected_voice)
        logger.log(SYSTEM_LEVEL, f"Selected voice = {selected_voice}")
        response = self.mistral.generate(modulated_conscious_prompt)

        ##REFLECTION OCCURS HERE##
        if count & memIO.reflection_interval == 0:
            #subconscious model access full memory bank and utilizes reflection framework + more

            username = memIO[{user_id}].memory_bank["username"]
            try:
                reflection_prompt = f"What do you think about your recent experiences?"
                modulated_subconscious_thought = apply_meta_voice(reflection_prompt, selected_voice)
                subconscious_thought = self.pixtral.generate(modulated_subconscious_thought)

                #save reflection to memory
                self.memory.add_memory(
                    user_id, 
                    user_input, 
                    subconscious_thought,
                    model_id = config["subconscious_model"]["id"], 
                    voice=selected_voice, 
                    context="subconscious", 
                    expires=None
                    )

                logger.log(SYSTEM_LEVEL, f"[Reflection] reflection successfully saved at count {count}")

            except Exception as e:
                logger.log(SYSTEM_LEVEL, f"[Reflection] reflection failed at count {count}")
        ####

        #save interaction to memory
        self.memory.add_memory(
            user_id, 
            user_input,
            response,
            model_id = config["conscious_model"]["id"],
            voice=selected_voice, 
            context="conscious",
            expires=None
            )
       
       
       #self.memory.append(user_id, username, user_input, subconscious_thought)

        
        return response
    
"""
    def closing_respone(self, user_id: str, user_input: str, model_type: str) -> str:


        short_term = self.memory = memIO.load_recent_context(user_id)
        selected_voice = self.determine_voice(user_input)

        #conscious model live context (via active user) and generate response
        conscious_prompt = f"[Context]\n{short_term}\n[User]\n{user_input}\n[Iris]\n"
        modulated_conscious_prompt = apply_meta_voice(conscious_prompt, selected_voice)
        logger.log(SYSTEM_LEVEL, f"Selected voice = {selected_voice}")
        response = self.mistral.generate(modulated_conscious_prompt)

        return response"""