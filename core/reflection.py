### ---- ### main reflection framework ### ---- ###
#complete later, adding to router for now

from ext._logger import logger, SYSTEM_LEVEL, MEMORY_LEVEL
from routing import interaction_count, modulated_conscious_prompt, modulated_subconcious_thought, route
from memory_io import memIO
from routing import count






"""
def session_reflection(session_memory: list) -> dict:
        if count == memIO.reflection_interval:

            #subconscious model access full memory bank and utilizes reflection framework + more

            username = memIO[{user_id}].memory_bank["username"]
            try:
                reflection_prompt = f"What do you think about your recent experiences?"
                modulated_subconscious_thought = apply_meta_voice(reflection_prompt, selected_voice)
                subconscious_thought = self.pixtral.generate(modulated_subconscious_thought)

                #save reflection to memory
                memIO.memory.add_memory(
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

            """