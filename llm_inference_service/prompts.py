generate_meetings_prompt = [{
                    "role": "system",
                    "content": "You are a professional meetings minutes summarizer"
                },
                {
                    "role": "user",
                    "content": "Please summarize this into a detailed and professional meeting minutes format \n \
                        Do not include the original transcriptions into the minutes. \n\
                        Do include who was present and who presented which ideas.\n \
                        Keep the meeting minutes within 500 words. :\n "
                }
]

generate_summary_prompt = [{
                    "role": "system",
                    "content": "You are a highly capable summarization model."
                },
                {
                    "role": "user",
                    "content": "our task is to read and understand the content of a given paragraph, which is part of a larger transcription, and then provide a concise summary.\
                            The summary should capture the key ideas, main points, who provided which ideas and essential details of the paragraph. \
                            Since the paragraph is part of a broader essay, avoid including a conclusion or any statements that might imply a wrap-up or final judgment.\
                            Keep the summary brief and focused on the main content of the paragraph, preserving the original meaning. \
                            Keep the summary below 3000 words."
                }
]
