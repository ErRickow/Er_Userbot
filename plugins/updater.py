##kurang lebih gini:
from . import get_help

__doc__ = get_help("help_updater")

from . import (
    ATRA_COL,
    LOGS,
    OWNER_NAME,
    ULTROID_IMAGES,
    Button,
    Carbon,
    Telegraph,
    Var,
    allcmds,
    asst,
    bash,
    call_back,
    callback,
    def_logs,
    eor,
    get_string,
    heroku_logs,
    in_pattern,
    inline_pic,
    restart,
    shutdown,
    start_time,
    time_formatter,
    udB,
    erubot_cmd,
    eruserbot_version,
    updater,
)


@erubot_cmd(pattern="up( (.*)|$)")
async def ngapdate(client):
    emo = client.me.username()
    await emo.initialize()
    pros = await client.reply(
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

        await pros.edit(f"<blockquote>{memeg}\n\n{teks}{format_output}</blockquote>", parse_mode="html")
    os.execl(sys.executable, sys.executable, "-m", "erNganu")