### ------ ### Model Management Functions ### ------ ###
# This module is responsible for loading and managing the models used in the application.
import os 
import json
from core.ext._logger import logger, SYSTEM_LEVEL
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
from core.ext.config_loader import load_config





class ModelWrapper:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer



class ModelManager:
    def __init__(self, config_path = "config.json"):
        self.config = load_config(config_path)
        self.conscious = None
        self.subconscious = None

        if self.config["conscious_model"]["enabled"]:
            self.conscious = self.load_model(self.config["conscious_model"])

        if self.config["subconscious_model"]["enabled"]:
            self.subconscious = self.load_model(self.config["subconscious_model"])

    
    #-# load model function #--#
    def load_model(self, model_config: dict) -> ModelWrapper:
        model_path = model_config["path"]
        quantization = model_config.get("quantization", {})
        if not model_path:
            raise ValueError("Model path is not specified.")
            logger.log(SYSTEM_LEVEL, f"[ModelManager] Model path is not specified.")
        if not os.path.exists(model_path):
            raise ValueError(f"Model path {model_path} does not exist.")
            logger.log(SYSTEM_LEVEL, f"[ModelManager] Model path {model_path} does not exist.")
            logger.log(SYSTEM_LEVEL, f"[ModelManager] Starting repair process.")

            #call function to download models/repair framework here, create function in dedicated script

        tokenizer = AutoTokenizer.from_pretrained(model_path)
        if not tokenizer:
            raise ValueError(f"Tokenizer not found for model at {model_path}.")
            logger.log(SYSTEM_LEVEL, f"[ModelManager] Tokenizer not found for model at {model_path}.")


        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            quantization_config=BitsAndBytesConfig(**quantization),
            device_map=quantization.get("device_map", "auto"),
            trust_remote_code=model_config.get("trust_remote_code", False)
        ).to("cuda" if torch.cuda.is_available() else "cpu")

        logger.log(SYSTEM_LEVEL, f"[ModelManager] Model loaded from {model_path} with quantization {quantization}.")

        return ModelWrapper(model, tokenizer)

    
    def get_conscious(self) -> ModelWrapper:
        if self.conscious is None:
            raise ValueError("Conscious model is not loaded.")
            logger.log(SYSTEM_LEVEL, f"[ModelManager] Conscious model is not loaded.")
        return self.conscious
    
    def get_subconscious(self) -> ModelWrapper:
        if self.subconscious is None:
            raise ValueError("Subconscious model is not loaded.")
            logger.log(SYSTEM_LEVEL, f"[ModelManager] Subconscious model is not loaded.")
        return self.subconscious


    def generate(self, prompt: str, max_tokens = 256) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens = max_tokens,
            do_sample = True,
            temperature = 0.7
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens = True)