async function main() {

 const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
  method: 'POST',
  headers: {
    Authorization: `Bearer ${process.env.OR}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'openrouter/free',
    stream: true,
    messages: [
      {
        role: 'user',
        content: 'What is the meaning of life?',
      },
    ],
  }),
})


const reader = response.body.getReader();
const decoder = new TextDecoder();



while (true) {
  const { done, value } = await reader.read();

  if (done) break;

  const chunk = decoder.decode(value);

    const lines = chunk.split("\n");

    for (const line of lines) {
      if (!line.startsWith("data: ")) continue;

      const data = line.slice(6);

      if (data === "[DONE]") return;

      try {
        const json = JSON.parse(data);

        const content =
          json.choices?.[0]?.delta?.content;

        if (content) {
          process.stdout.write(content);
        }
      } catch {}
    }
  }
}

main();