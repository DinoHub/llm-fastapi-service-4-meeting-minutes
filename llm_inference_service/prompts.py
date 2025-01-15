generate_meetings_prompt = [{
                    "role": "system",
                    "content": "You are a highly capable meetings minutes summarizer"
                },
                {
                    "role": "user",
                    "content": "Please summarize this into a detailed and professional meeting minutes format \n \
                        Do include who was present and who presented which ideas.\n \
                        Keep the meeting minutes within 300 words. Summarize the text after the colon only:\n"
                }
]

generate_summary_prompt = [{
                    "role": "system",
                    "content": "You are a highly capable summarization model."
                },
                {
                    "role": "user",
                    "content": "You are provided with a transcript with the speaker and timestamps.\n\
                            The format for each speech segment is: [<Name>] <timestamp>\n <Message>\
                            You are tasked to summarise the transcipt by capturing the key ideas, main points, who provided which ideas and essential details of the meeting. \n\
                            keep the summary below 1000 words \n \
                            Start Summarising the text after the colon :\n"
                }
]
