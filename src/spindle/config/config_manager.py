import os
from typing import List
from openai import OpenAI, APIConnectionError
from dotenv import load_dotenv

__All__ = ["ConfigManager"]


class ConfigManager:
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.config/spindle")
        self.env_file = os.path.join(self.config_dir, ".env")
        os.makedirs(self.config_dir, exist_ok=True)
        self._load_env()
        self.client = None
        self.initialize_openai_client()
        self.args = None  # This should be set after initialization if needed

    def _load_env(self):
        load_dotenv(self.env_file)

    def initialize_openai_client(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            self.client = OpenAI(api_key=api_key)

    def get(self, key: str, default: str = None) -> str:
        return os.getenv(key, default)

    def set(self, key: str, value: str):
        os.environ[key] = value
        with open(self.env_file, "a") as f:
            f.write(f"{key}={value}\n")

    def get_config_dir(self) -> str:
        return self.config_dir

    def get_patterns_dir(self) -> str:
        return os.path.join(self.config_dir, "patterns")

    def get_gpt_models(self) -> List[str]:
        gptlist = []
        try:
            if self.client:
                models = [model.id.strip() for model in self.client.models.list().data]
                if "/" in models[0] or "\\" in models[0]:
                    gptlist = [item[item.rfind("/") + 1:] if "/" in item else item[item.rfind("\\") + 1:] for item in models]
                else:
                    gptlist = [item.strip() for item in models if item.startswith("gpt")]
                gptlist.sort()
        except APIConnectionError:
            pass
        except Exception as e:
            print(f"Error fetching GPT models: {getattr(e.__context__, 'args', [''])[0]}")

        return gptlist

    def get_claude_models(self) -> List[str]:
        if os.getenv("CLAUDE_API_KEY"):
            return [
                'claude-3-5-sonnet-20240620',
                'claude-3-opus-20240229',
                'claude-3-sonnet-20240229',
                'claude-3-haiku-20240307',
                'claude-2.1'
            ]
        else:
            return []

    def get_google_models(self) -> List[str]:
        googleList = []
        try:
            import google.generativeai as genai
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        googleList.append(m.name)
        except ImportError:
            print("Google GenerativeAI library is not installed.")
        except Exception as e:
            print(f"Error fetching Google models: {str(e)}")

        return googleList

    def get_ollama_models(self) -> List[str]:
        fullOllamaList = []
        try:
            import ollama
            remoteOllamaServer = getattr(self.args, 'remoteOllamaServer', None)

            if remoteOllamaServer:
                client = ollama.Client(host=remoteOllamaServer)
                default_modelollamaList = client.list()['models']
            else:
                default_modelollamaList = ollama.list()['models']

            for model in default_modelollamaList:
                fullOllamaList.append(model['name'])
        except ImportError:
            print("Ollama library is not installed.")
        except Exception as e:
            print(f"Error fetching Ollama models: {str(e)}")

        return fullOllamaList

    def set_args(self, args):
        self.args = args