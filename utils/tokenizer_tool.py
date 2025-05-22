### ---- ### Tokenizer Sanitizer and Cleaner Tool ### ---- ###
import json
import os





def extract_tokenizer_metadata(tokenizer_dir):
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

def sanitize_tokenizer(tokenizer_dir, output_path="data/tokenizer_sanitized.json"):
    """
    Save only necessary fields from tokenizer config into a minimalist, portable JSON file.
    """
    metadata = extract_tokenizer_metadata(tokenizer_dir)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as out:
        json.dump(metadata, out, indent=2)

    print(f"[✓] Sanitized tokenizer saved to: {output_path}")
    return metadata

def merge_tokenizer_with_custom(model_tokenizer, sanitized_metadata):
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
