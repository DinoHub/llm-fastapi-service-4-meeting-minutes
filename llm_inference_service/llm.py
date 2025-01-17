from vllm import LLM, SamplingParams
from prompts import generate_meetings_prompt, generate_summary_prompt
from utils import construct_prompt, check_if_chunking_neccessary, chunk_message_brute, chunk_message_by_speech
import logging

logging.basicConfig(
    format="%(levelname)s | %(asctime)s | %(message)s", level=logging.INFO
)
class LLMForSummary:
    
    def __init__(self, 
                 model_path, 
                 gpu_memory_utilization = 0.6, 
                 max_model_len = 16000,
                 tensor_parallel_size = 1,
                 max_context_length = 7000):
        
        logging.info("Starting up LLM")
        
        self.llm = LLM(model = model_path, 
                         tensor_parallel_size = tensor_parallel_size,
                         gpu_memory_utilization = gpu_memory_utilization,
                         max_model_len = max_model_len)
        
        self.max_context_length = max_context_length
        self.sampling_params = SamplingParams(max_tokens=self.max_context_length, temperature=1)
        
        logging.info("LLM started up")
        
        
    def generate_meeting_minutes(self, text):
        
        logging.info("Generating meeting mintues")
        
        final_minutes = ""
        
        prompt = construct_prompt(generate_meetings_prompt)
        prompt_with_transcription = prompt + text
        # print(prompt_with_transcription)
        
        outputs = self.llm.generate(prompt_with_transcription, self.sampling_params)
        for output in outputs:
            final_minutes+=output.outputs[0].text
            
        logging.info("Summary_text: %s", final_minutes)
        
        return final_minutes
    
    def generate_summary(self, text):
        
        logging.info("Generating summary")
        
        final_summary = ""
        
        prompt = construct_prompt(generate_summary_prompt)
        
        #prompt = 'Summarize the following dialouge:\n'
        
        prompt_with_transcription = prompt + text
        
        # logging.info("Summary_text: %s", prompt_with_transcription)
        
        outputs = self.llm.generate(prompt_with_transcription, self.sampling_params)
        
        for output in outputs:
            final_summary+=output.outputs[0].text
            
        logging.info("Summary_text: %s", final_summary)
        return final_summary
    
    def chunking_loop(self, text):
        
        logging.info("Chunking is necessary")
        
        # NOTE: can chunk by speech or brute force 
        text_chunks = chunk_message_brute(text, self.max_context_length)
        summary_text = ''
        count = 0
        
        for text_chunk in text_chunks:
            summary_chunk = self.generate_summary(text_chunk)
            summary_text += f"This is text chunk {count}:\n"+summary_chunk
            count += 1
        
        if check_if_chunking_neccessary(summary_text, max_length=self.max_context_length):
            summary_text = self.chunking_loop(summary_text)
            
        return summary_text
    
    def orchestrator(self, text):
        logging.info("Entering Orchestrator")
        
        if check_if_chunking_neccessary(text, max_length=self.max_context_length):
        
            text = self.chunking_loop(text)
            
        meeting_minutes = self.generate_meeting_minutes(text)
        
        return meeting_minutes