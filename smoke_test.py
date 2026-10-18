import anthropic

client = anthropic.Anthropic()
resp = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=50,
    extra_body={"temperature": 1.0},
    messages=[{"role": "user", "content": "Say hi in five words."}],
)
print(resp.content[0].text)