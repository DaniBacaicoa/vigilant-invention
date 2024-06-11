import anthropic



api_key = "your_api_key_here"
api = ClaudeAPI(api_key)

# Get a response from Claude
prompt = "What is the capital of France?"
response = api.chat(prompt)
print(response)

# Upload a file
file_path = "path/to/your/file.txt"
file_obj = api.upload_file(file_path)
if file_obj:
    print(f"Uploaded file: {file_obj.name}")


class ClaudeAPI(object):
    def __init__(self):
        path_env = pathlib.Path(os.getcwd()) / '.env'
        load_dotenv(path_env)
        self._claude_api_key = os.getenv("CLAUDE_API_KEY")
        self.client = anthropic.Client(self._claude_api_key)

    def get_kwds(self, prompt):
        response = self.client.completion(
            prompt=prompt,
            model="claude-v1",
            max_tokens_to_sample=1000,
            stop_sequences=[],
        )
        return response.completion

    def upload_file(self, file_path):
        try:
            with open(file_path, "rb") as f:
                file_bytes = f.read()
            upload_response = self.client.upload_file(file_bytes)
            return upload_response.file
        except Exception as e:
            print(f"Error uploading file: {e}")
            return None