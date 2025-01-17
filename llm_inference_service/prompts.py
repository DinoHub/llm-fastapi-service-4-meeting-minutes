generate_meetings_prompt = [{
                    "role": "system",
                    "content": "You are a highly capable meetings minutes summarizer"
                },
                {
                    "role": "user",
                    "content": "###Instruction### You MUST summarize this into a detailed and professional meeting minutes format \n \
                        Do include who was present and who presented which ideas.\n\
                        Keep the meeting minutes within 300 words. Summarize the text after the colon only:\n  ###TEXT###\n"
                }
]

generate_summary_prompt = [{
                    "role": "system",
                    "content": "You are a highly capable summarization model."
                },
                {
                    "role": "user",
                    "content": "###Instruction### You are provided with a transcript with the speaker and timestamps.\n\
                            The format for each speech segment is: [<Name>] <timestamp>\n <Message>\
                            You MUST summarise the transcipt by capturing the key ideas, main points, who provided which ideas and essential details of the meeting. \n\
                            DO NOT include any other text besides the summary. DO NOT include the transcription in the final summary.\n\
                            DO start the summarization with '<Summarisation>' \n \
                            Start Summarising the text after the colon:\n ###TRANSCRIPT### \n"
                }
]
