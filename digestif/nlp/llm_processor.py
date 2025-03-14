from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


class NlpException(Exception):
    pass


class LLMProcessor:
    def __init__(
        self,
        client: OpenAI,
        prompt: str,
        model_name: str = "gpt-4o-mini",
        max_tokens: int = 2048,
    ):
        self.llm = client
        self.base_prompt = prompt
        self.model = model_name
        self.max_tokens = max_tokens

    def __call__(
        self, text: str, conversation: list[ChatCompletionMessageParam] = []
    ) -> str:
        current_prompt = self.base_prompt
        messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": current_prompt},
        ]

        messages.extend(conversation)
        messages.append({"role": "user", "content": text})

        completion = self.llm.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0,
            max_tokens=self.max_tokens,
            top_p=1,
            stop=None,
            seed=2402,
        )
        completion = completion.choices[0].message.content
        if completion is None:
            raise NlpException("No response returned")
        return completion
