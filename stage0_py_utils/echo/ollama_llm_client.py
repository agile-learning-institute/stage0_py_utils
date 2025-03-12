import ollama

class OllamaLLMClient:
    """_summary_
    Wrapper for the ollama Library for chat function
    """
    def __init__(self, base_url="http://localhost:11434", model="llama3.2:latest"):
        """
        Initializes the LLMClient to communicate with an Ollama server.
        
        :param base_url: URL of the Ollama API server.
        :param model: Default model to use.
        """
        self.base_url = base_url
        self.model = model

    def chat(self, model: str, messages: list):
        """
        Sends a chat message to the LLM and returns the response.
        
        :param model: The model name to be used
        :messages: An array of messages passed to the model.
        :return: LLM-generated response or an error message.
        """

        response = ollama.chat(model=model, messages=messages)
        # response.raise_for_status()
        return response

    def set_model(self, model_name: str):
        """
        Sets a new model to be used by the LLMClient.
        
        :param model_name: Name of the model.
        """
        self.model = model_name
