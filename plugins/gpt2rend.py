"""
Get Answers from Chat GPT

> No need of any API key.

• Examples: 
> {i}gpt2 How to get a url in Python
"""

from io import BytesIO

from . import async_searcher, LOGS, erubot_cmd


@erubot_cmd(pattern="gpt2( ([\s\S]*)|$)")
async def chatgpt2(e):
    query = e.pattern_match.group(2)
    reply = await e.get_reply_message()
    if not query:
        if reply and reply.text:
            query = reply.message
    if not query:
        return await e.eor("Gimme a Question to ask from ChatGPT")

    eris = await e.eor("Generating answer...")
    payloads = {"query": query}
    try:
        response = await async_searcher(
            "https://randydev-ryuzaki-api.hf.space/ryuzaki/chatgpt-old",
            post=True,
            json=payloads,
            re_json=True,
            headers = {"Content-Type": "application/json"},
        )
        if not (response and ["randydev"]["message"] in response):
            LOGS.error(response)
            raise ValueError("Invalid Response from Server")

        response = response["randydev"].get("message")
        if len(response + query) < 4080:
            to_edit = (
                f"Query:\n~ {query}\n\nChatGPT:\n~ {response}"
            )
            await eris.edit(to_edit, parse_mode="html")
            return
        with BytesIO(response.encode()) as file:
            file.name = "gpt_response.txt"
            await e.client.send_file(
                e.chat_id, file, caption=f"{query[:1020]}", reply_to=e.reply_to_msg_id
            )
        await eris.try_delete()
    except Exception as exc:
        LOGS.exception(exc)
        await eris.edit(f"Ran into an Error: \n{exc}" )
