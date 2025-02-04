import logging
import re

logging.basicConfig(
    format="%(levelname)s | %(asctime)s | %(message)s", level=logging.INFO
)

def construct_prompt(messages):
    """
    To format the prompts for LLM usage

    Attributes:
        messages (list of dictionaries): Prompt to help the LLM understand its task better, e.g.
        
        [{
            "role": "system",
            "content": ""
        },
        {
            "role": "user",
            "content": ""
        }
    ]
    
    Return:
        String: Formatted prompt for LLM usage
    """
    
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
    
    Return:
        Boolean: whether chunking is necessary or not
    """
    
    word_count = len(text.split())
    return word_count >= max_length


def chunk_message_brute(text, max_length = 1000):
    
    words = text.split()  # Split the text into words
    chunks = [" ".join(words[i:i+max_length]) for i in range(0, len(words), max_length)]
    
    return chunks

def split_into_speech_segments(text):
    """
    Split speech segments in a transcription up for better chunking

    Attributes:
        text (str): text that is being checked
    """
    
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

def chunking_orchestrator(text, max_length = 1000, chunking_choice = 'by_speech'):
    
    if chunking_choice == "by_speech":
        
        chunks = chunk_message_by_speech(text, max_length)
        
    else:
        
        chunks = chunk_message_brute(text, max_length)
    
    logging.info("Number of chunks: %s", len(chunks))
    
    return chunks

def limit_number_of_words_in_string(text, max_no_words):
    
    words = text.split()
    return ' '.join(words[:max_no_words])