### ---- ### Model Management Functions ### ---- ###
##
#
# This module is responsible for loading and managing the underlying models.
#


#-- imports --#
import os
import json
from ext._logger import logger, SYSTEM_LEVEL
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
from ext.config_loader import main_config
from utils.tokenizer_tool import TokenizerBank

config = main_config

#provides for a unified interface to the models, allowing for easy switching between the conscious and subconscious models
class ModelManager:
    def __init__(self, config):
        
        self.config = config
        self.models = {}
        self.voice_mode = "neutral"

     
    
    #-# load model function #--#

    def load_model(self, role):
        #pulling info from config (role and "enabled" status)
        if role not in self.config:
            raise ValueError(f"Invalid model role: {role}")
        
    
        model_info = self.config[role]
        if not model_info.get("enabled", True):
            return None


        model_id = model_info["id"]
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        tokenizer_metadata = TokenizerBank.sanitize_tokenizer(model_id)
        tokenizer = TokenizerBank.merge_tokenizer_with_custom(tokenizer, tokenizer_metadata)

        if self.voice_mode == "{self.voice_mode}":
            model.config.quantization = self.voice_mode["generation_args"]

        model = AutoModelForCausalLM.from_pretrained(model_id)
        self.models[role] = (model, tokenizer)
        return model, tokenizer
    

    def unload_model(self, role):
        return
    
    def get_model(self, role):
        return self.models.get(role, None)
    
    def set_voice_mode(self, voice):
        self.voice_mode = voice













"""
def load_model(self, model_config: dict) -> ModelWrapper:
    model_path = model_config["path"]
    quantization = model_config.get("quantization", {})
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        quantization_config=BitsAndBytesConfig(**quantization),
    ).to("cuda" if torch.cuda.is_available() else "cpu")

    logger.log(SYSTEM_LEVEL, f"[ModelManager] Model loaded from {model_path} with quantization {quantization}.")

    return ModelWrapper(model, tokenizer)

#--# calling the conscious and subconscious models
def get_conscious(self, model_config: dict) -> ModelWrapper:
    if model_config["conscious_model"]["enabled"] and (not self.conscious or self.conscious.model is None):
        self.conscious = self.load_model(self.config["conscious_model"])
    return self.conscious

def get_subconscious(self, model_config: dict) -> ModelWrapper:
    if model_config["subconscious_model"]["enabled"] and (not self.subconscious or self.subconscious.model is None):
        self.subconscious = self.load_model(self.config["subconscious_model"])
    return self.subconscious
#--#

#--# function for generating text using the models#--#
def generate(self, model_config: dict, prompt: str, max_tokens = 256) -> str:
    inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
    outputs = self.model.generate(
        **inputs,
        max_new_tokens = max_tokens,
        do_sample = True,
        temperature = 0.7
    )
    return self.tokenizer.decode(outputs[0], skip_special_tokens = True)
"""