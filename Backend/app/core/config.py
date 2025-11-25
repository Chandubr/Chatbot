from pydantic_settings import BaseSettings
import base64

class EnvConfig(BaseSettings):
    openai_api_key_encoded: str
    generation_model_openai: str
    langsmith_api_key_encoded: str
    langsmith_tracing: bool = True
    host: str
    port: int

    class Config:
        env_file = ".env"
        extra = "allow"

    @property
    def openai_api_key(self) -> str:
        return base64.b64decode(self.openai_api_key_encoded).decode()

    @property
    def langsmith_api_key(self) -> str:
        return base64.b64decode(self.langsmith_api_key_encoded).decode()
    


envconfig = EnvConfig()
