import requests
import json

SERVICE_URL = "http://localhost:8000/llm_orchestrator"

def ping_container():
    try:
        headers = {
            "Content-Type": "application/json",
        }
        
        # prompt = "[0.00 - 0.10] [speaker_2] :  - You mentioned from personal experience, being aware of the dark side of anabolic use. What is that? \
        #     [0.09 - 1.01] [speaker_1] :  How long do you have anxiety like you would not believe? Every day that I'm on high doses, I wake up in the morning afraid of the rest of my day. Intrusive thoughts. I think about violence all the time. Well, if your testosterone is 25 times what it's supposed to be, what the hell do you think it's going to make you think about? Another one is a marked proximate reduction of IQ. Like right now, as I talk to you, I'm on contest prop. I'm on a considerable dose of anabolics. I'm not as smart right now and I can feel it. It's this awe, an inability to perceive a broad spectrum of positive human emotion. I live in a really beautiful area in Michigan and I walk out and there's a pond and these trees and I know that I like looking at them, but it's memory to me. I go work out every morning and I look at the pond and the trees and I'm like, like all I feel is rage and frustration and anger and anxiety. That's my daily life.\
        #     [1.00 - 2.00] [speaker_0] :  Welcome to another episode of the Checkup Podcast with Dr. Mike. Today, I, Dr. Mike, am excited to welcome Dr. Mike to the Checkup Podcast with Dr. Mike. No, I'm not inviting myself onto my own show. I'm talking about Dr. Mike Israetel, a popular YouTube educator, but also someone who holds a PhD in sports physiology. Whether you're looking to start putting on muscle, restarting a forgotten regimen, understanding the impact of mental health on your fitness journey, or uncovering the harsh realities of steroid use, this conversation covers that and so much more. We got into some topics I truly didn't expect to address, but found extremely interesting, including the fact that he believes AI and gene therapy will get us to the point where exercise becomes completely useless. What? Bottom line, get ready to get re-energized and educated on how to pack on muscle and why it's actually crucial for your health to do so. Please welcome the other Dr. Mike to the Checkup Podcast."

        txt_files = ["examples/MIT_Transcript_1.txt", "examples/MIT_Transcript_2.txt"]
        prompt = ""

        for txt_file in txt_files:
            with open(txt_file, "r") as file:
                content = file.read()
            prompt+=content
        
        payload = {
            "message": prompt
        }
        response = requests.post(SERVICE_URL, headers=headers, json=payload)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)

output_file = 'trial_orchestrator.txt'
output_filepath = 'output/' + output_file
def main():
    status_code, response_text = ping_container()
    print(f"Status Code: {status_code}, Response: {response_text}")
    
    response_text = json.loads(response_text)
    
    with open(output_filepath, "w") as file:
        file.write(response_text['text'])
    
    
    
main()