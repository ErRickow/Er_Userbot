##kurang lebih gini:

@erubot_cmd(pattern="up( (.*)|$)")
async def ngapdate(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    pros = await message.reply(
        f"<blockquote>{emo.proses} <b>Memeriksa pembaruan resources {bot.me.mention} ..</b></blockquote>"
    )
    out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    teks = f"<b>❒ Status resources {bot.me.mention}:</b>\n"
    memeg = f"{emo.profil} <b>Change logs {bot.me.mention}</b>"
    if "Already up to date." in str(out):
        return await pros.edit(f"<blockquote>{teks}┖ {out}</blockquote>")
    elif len(out) > 4096:
        anuk = await pros.edit(
            f"<blockquote>{emo.proses} <b>Hasil akan dikirimkan dalam bentuk file ..</b></blockquote>"
        )
        with open("output.txt", "w+") as file:
            file.write(out)

        X = f"<blockquote>{emo.alive} <b>Change logs {bot.me.mention}</b></blockquote>"
        await client.send_document(
            message.chat.id,
            "output.txt",
            caption=f"{X}",
            reply_to_message_id=message.id,
        )
        await anuk.delete()
        os.remove("output.txt")
    else:
        format_line = [f"┣ {line}" for line in out.splitlines()]
        if format_line:
            format_line[-1] = f"┖ {format_line[-1][2:]}"
        format_output = "\n".join(format_line)

        await pros.edit(f"<blockquote>{memeg}\n\n{teks}{format_output}</blockquote>")
    os.execl(sys.executable, sys.executable, "-m", "ubot")