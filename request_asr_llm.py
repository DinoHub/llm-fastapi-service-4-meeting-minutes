import requests
import json

LLM_SERVICE_URL = "http://localhost:8000/llm_generate"
ASR_SERVICE_URL = "http://localhost:8001/v1/transcribe_diarize_denoise_filepath"
FILENAME = "steroids_120sec.wav"
DIRECTORY = "examples/"
FILEPATH = DIRECTORY + FILENAME

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

def ping_llm_container(text):
    try:
        
        headers = {
            "Content-Type": "application/json",
        }
        data =[
                {
                    "role": "system",
                    "content": "You are a professional meetings minutes summarizer"
                },
                {
                    "role": "user",
                    "content": "Please summarize this into detailed and professional meeting minutes format \n \
                        Do not include the original transcriptions into the minutes. Do include who was present and who present which ideas. :\n"+ text
                }
        ]
        prompt = construct_prompt(data)
        payload = {
            "message": prompt
        }
        response = requests.post(LLM_SERVICE_URL, headers=headers, json=payload)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)

def ping_asr_container():
    try:
        audio_bytes = {"file": open(FILEPATH, "rb")}
        response = requests.post(ASR_SERVICE_URL, files=audio_bytes)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)

output_summary_file = "output_summary_"+FILENAME.split('.')[0]+'.txt'
output_transcription_file = "output_transcription_"+FILENAME.split('.')[0]+'.txt'
output_summary_filepath = 'output/' + output_summary_file
output_transcription_filepath = 'output/' + output_transcription_file
    
def main():
    status_code, asr_response_text = ping_asr_container()
    with open(output_transcription_filepath, "w") as file:
        file.write(json.loads(asr_response_text)["transcription"])
    
    status_code, llm_response_text = ping_llm_container(json.loads(asr_response_text)["transcription"])
    print(f"Status Code: {status_code}, Response: {llm_response_text}")
    
    response_text = json.loads(llm_response_text)
    
    with open(output_summary_filepath, "w") as file:
        file.write(response_text['text'])
    
    
    
    
main()