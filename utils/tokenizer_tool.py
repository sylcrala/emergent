### ---- ### Tokenizer Sanitizer and Cleaner Tool ### ---- ###
import json
import os


class TokenizerBank:
#made into class to allow tool to see multiple tokenizer paths
    def __init__(self, base_dir="data/tokenizers/"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
        self.tokenizers = {}






    def extract_tokenizer_metadata(self, tokenizer_dir):
        """
        Extract key metadata from tokenizer config files for portable use in Iris.
        """
        tokenizer_json_path = os.path.join(tokenizer_dir, "tokenizer.json")
        tokenizer_config_path = os.path.join(tokenizer_dir, "tokenizer_config.json")

        data = {}

        if os.path.exists(tokenizer_config_path):
            with open(tokenizer_config_path, 'r') as f:
                config_data = json.load(f)
                data["special_tokens_map"] = config_data.get("special_tokens_map", {})
                data["bos_token_id"] = config_data.get("bos_token_id")
                data["eos_token_id"] = config_data.get("eos_token_id")

        if os.path.exists(tokenizer_json_path):
            with open(tokenizer_json_path, 'r') as f:
                tokenizer_data = json.load(f)
                data["added_tokens_decoder"] = tokenizer_data.get("added_tokens_decoder", {})

        return data

    def sanitize_tokenizer(self, tokenizer_dir, model_name):
        """
        Save only necessary fields from tokenizer config into a minimalist, portable JSON file.
        """
        metadata = self.extract_tokenizer_metadata(tokenizer_dir)

        path = os.path.join(self.base_dir, f"{model_name}_sanitized.json")
        
        with open(path, "w") as out:
            json.dump(metadata, out, indent=2)
        self.tokenizers[model_name] = metadata

        print(f"[✓] Sanitized tokenizer saved to: {path}")
        return metadata

    def merge_tokenizer_with_custom(self, model_tokenizer, sanitized_metadata):
        """
        Add back any essential tokens to a loaded tokenizer dynamically.
        """
        decoder = sanitized_metadata.get("added_tokens_decoder", {})
        if decoder:
            for token_id, token_obj in decoder.items():
                content = token_obj.get("content")
                if content:
                    model_tokenizer.add_tokens([content], special_tokens=True)
        return model_tokenizer
    
    def load(self, model_name):
        path = os.path.join(self.base_dir, f"{model_name}_sanitized.json")

        if not os.path.exists(path): return None
        with open(path, "r") as f:
            self.tokenizers[model_name] = json.load(f)
        return self.tokenizers[model_name]
