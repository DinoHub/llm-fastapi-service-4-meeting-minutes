import logging

logging.basicConfig(
    format="%(levelname)s | %(asctime)s | %(message)s", level=logging.INFO
)

def construct_prompt(messages):
    
    prompt = ""
    for msg in messages:
        if msg["role"] == "system":
            prompt += f"[System]\n{msg['content']}\n\n"
        elif msg["role"] == "user":
            prompt += f"[User]\n{msg['content']}\n\n"
        elif msg["role"] == "assistant":
            prompt += f"[Assistant]\n{msg['content']}\n\n"
    return prompt


def check_if_chunking_neccessary(text, max_length = 1000):
    
    word_count = len(text.split())
    return word_count >= max_length


def chunk_message_brute(text, max_length = 1000):
    
    words = text.split()  # Split the text into words
    chunks = [" ".join(words[i:i+max_length]) for i in range(0, len(words), max_length)]
    
    logging.info("Number of chunks: %s", len(chunks))
    
    return chunks
        
        