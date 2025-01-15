
Running the LLM Inference Server container:
Note: The volume mount dir for the templates and models should match your current file dir.

docker run --rm -p 8000:8000 --gpus all -v ./templates:/tmp/templates -v ./models:/tmp/models dinohub/vllm:Llama-3.2-3B \
    --served-model-name meta-llama/Llama-3.2-3B-Instruct --model /tmp/models/llama/Llama-3.2-3B-Instruct \
    --chat-template /tmp/templates/tool_chat_template_llama3.2_json.jinja --disable-log-requests --gpu-memory-utilization=0.60  --max-model-len=18000

To test the serve:
Note: The model name should be the same as the '--served-model-name' used in the server.

curl -X POST "http://localhost:8000/v1/chat/completions" \
	-H "Content-Type: application/json" \
	--data '{
		"model": "meta-llama/Llama-3.2-3B-Instruct",
		"messages": [
			{
				"role": "user",
				"content": [
					{
						"type": "text",
						"text": "Why is the sky blue?"
					}
				]
			}
		]
	}'