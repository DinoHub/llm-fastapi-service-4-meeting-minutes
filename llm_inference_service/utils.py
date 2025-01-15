import logging
import re

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
    """
    Check if chunking is neccessary based on max_length of words provided

    Attributes:
        text (str): text that is being checked
        max_length (int): max word length allowed
    """
    
    word_count = len(text.split())
    return word_count >= max_length


def chunk_message_brute(text, max_length = 1000):
    
    words = text.split()  # Split the text into words
    chunks = [" ".join(words[i:i+max_length]) for i in range(0, len(words), max_length)]
    
    logging.info("Number of chunks: %s", len(chunks))
    
    return chunks
def split_into_speech_segments(text):
    
    pattern = r"(\[[^\]]+\] \d{2}:\d{2}:\d{2}\n.*?(?=\[[^\]]+\] \d{2}:\d{2}:\d{2}|\Z))" # NOTE: Pattern for MIT Transcript
    #pattern = r"(\[\d{1,2}\.\d{2} - \d{1,2}\.\d{2}\] \[speaker_\d\] :.*?(?=\[\d{1,2}\.\d{2} - |\Z))" # NOTE: For Ian's Representation of diarization (Minutes)
    
    segments = re.findall(pattern, text, re.DOTALL)
    
    return segments

def chunk_message_by_speech(text, max_length = 1000):
    
    segments = split_into_speech_segments(text)
    chunks = []
    current_chunk = []
    current_word_count = 0

    for segment in segments:
        word_count = len(segment.split())
        
        if current_word_count + word_count > max_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = [segment]
            current_word_count = word_count
        else:
            current_chunk.append(segment)
            current_word_count += word_count
            
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
