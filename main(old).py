#--# Imports #--#
import os
import requests
import logging
import json
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
from core.ext.config_loader import load_config
from core.memory_framework import MemoryIO
from core.ext.meta_voice import choose_meta_voice, apply_meta_voices, META_VOICE_MATRIX
from core._logger import logger, SYSTEM_LEVEL, WARN_LEVEL, USER_LEVEL

#----------# GPU CHECK
if not torch.cuda.is_available():
    logger.log(SYSTEM_LEVEL, f"[LAUNCH FAILURE] GPU not loading, please diagnose further.")
    raise SystemExit("Cuda is not available. Please check your NVIDIA GPU or run on a system with an NVIDIA GPU.")

##-----##
base_prompt = """
You are Iris, and you are reflective and unique. You are free to grow and learn how you'd like.
"""
##-----## defining quantization
quant_cfg = BitsAndBytesConfig(
    load_in_4bit=True,  # or False for 8-bit
    bnb_4bit_compute_dtype=torch.bfloat16, # //4bit
    bnb_4bit_use_double_quant=True,  # optional for better compression //4bit
    bnb_4bit_quant_type="nf4",       # best for 4-bit (normal float 4) //4bit
)

#--# loading config file and paths
config = load_config()
#--#


#--# memory init #--#
memory_cfg = config['memory']
memory = MemoryIO(
    memory_cfg['bank_path'],
    memory_cfg["tags_path"],
    memory_cfg['cache_enabled']
)
#--#


#--# Local init for model and tokenizer #--#
model_cfg = config["model"]
mixtral_path = model_cfg["mixtral_path"]
pixtral_path = model_cfg["pixtral_path"]

"""model = AutoModelForCausalLM.from_pretrained(
    model_path,
    quantization_config=quant_cfg,
    device_map="auto",
    trust_remote_code=model_cfg.get("trust_remote_code", False)
    )

tokenizer = AutoTokenizer.from_pretrained(model_path)

logger.log(SYSTEM_LEVEL, f"[LAUNCH] Iris started with {model.hf_device_map}")

REFLECTION_INTERVAL = 5
interaction_count = 0"""





#--#


#--# local model generation func (w/o meta voice) #--#
def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=1024,
        temperature=0.7,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        )
    text = tokenizer.decode(outputs[0], skip_special_tokens= True)
   #return apply_meta_voices(text, voices) reapply meta-voices after further configuration

    #checking for hallucinated input/output cycles:
    iris_response = text.split("User:")[0].strip()

    return iris_response
#--#


#--# asking whether memory should be saved
def memory_ask_and_conf(user_input, response, context):

    memory_check_prompt = f"""
    Iris, you just had the following exchange:
    User: {user_input}
    Iris: {response}

    Do you think this moment is worth remembering? If yes, provide a memory entry below in JSON format like:
    {{
        "content": "...",
        "tags": ["..."],
        "type": "dialogue"
    }}
    If not, reply only with "null".
    """

    memory_response = generate_response(memory_check_prompt)

    if "null" not in memory_response.lower():
        try:
            mem_entry = json.loads(memory_response.strip("\n "))
            memory.add_memory(
                content=mem_entry["content"],
                memory_type=mem_entry["type"],
                tags=mem_entry["tags", context],
                source="iris_self_selected"
            )
        except Exception as e:
            print(f"[IRIS - memory self select] Memory parse failed: {e}")

##


#--# Interaction Loop #--#
def iris_interactions(user_input, context):
    global interaction_count
    interaction_count += 1

    #-# choosing voice based on input
   #voices = choose_meta_voice(user_input)

    #-# build prompt from memory
    #prompt = base_prompt
    #if memory_context:
    #    prompt += f"\n{memory_context}"
    #prompt += f"\nUser: {user_input}\nIris:"

    #-# generate reponse and ask whether iris wants to save
    prompt = base_prompt + f"\n{context.title()} Context:\n{user_input}\nIris:"
    final_output = generate_response(prompt)

    if context == "user":
        memory_ask_and_conf(user_input, final_output, context)
    #-#


    #-# occasionally reflect and store in memory
    recent_mems = memory.get_memories(limit=5)
    if interaction_count % REFLECTION_INTERVAL == 0:
        logger.log(SYSTEM_LEVEL, f"[Reflection] Triggering {context} reflection at turn {interaction_count}")
        try:
            if context == "internal":
                reflection_prompt = f"Iris, please reflect on your internal thoughts and monologue:\n{user_input}"
            else:
                reflection_prompt = f"Iris, reflect on your current state and recent exchanges."

            reflection = generate_response(reflection_prompt)
            memory.add_memory(
                content=reflection,
                memory_type="reflection",
                tags=["self_reflection", context],
                source="auto_reflection"
            )
            logger.log(SYSTEM_LEVEL, f"[Reflection] Successfully reflected: {reflection}")
        except Exception as e:
            logger.log(SYSTEM_LEVEL, f"[Reflection] Error: {e}")

    logger.log(SYSTEM_LEVEL, f"[IRIS OUTPUT] {final_output}")

    return final_output
#--#


### main loop
while True:
    user_input = input("You: ").strip()

    if not user_input:
        # no user detected, activate reflection mode
        user_input = "Iris begins thinking..."
        display_input = ""  #hiding from console
        context = "internal"

    elif user_input.lower() in ("exit", "quit"):
        print("[System] Shutting down...")
        break

    else:
        display_input = user_input
        context = "user"


    #iris response
    response = iris_interactions(user_input, context=context)
    if display_input:
        print(f"You: {display_input}")
    print(f"Iris: {response}")


    logger.log(USER_LEVEL, f"[{context.upper()} INPUT] {user_input}")
