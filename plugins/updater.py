##kurang lebih gini:
import subprocess

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
async def _(a):
    xx = await a.reply(get_string("upd_1"))
    if a.pattern_match.group(1).strip() and (
        "fast" in a.pattern_match.group(1).strip()
        or "soft" in a.pattern_match.group(1).strip()
    ):
        await xx.reply(
            f'<blockquote><code>Your BOT is </code><strong>up-to-date</strong><code> with </code><strong>nganu</a></strong></blockquote>',
            parse_mode="html",
            link_preview=False,
        )
    out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    teks = f"<b>❒ Status resources {asst.me.mention}:</b>\n"
    memeg = f"<b>Change logs {asst.me.mention}</b>"
    if "Already up to date." in str(out):
        return await pros.edit(f"<blockquote>{teks}┖ {out}</blockquote>")
    elif len(out) > 4096:
        anuk = await pros.edit(
            f"<blockquote>{emo.proses} <b>Hasil akan dikirimkan dalam bentuk file ..</b></blockquote>"
        )
        with open("logs.txt", "w+") as file:
            file.write(out)

        X = f"<blockquote><b>Change logs {asst.me.mention}</b></blockquote>"
        await e.send_document(
            message.chat.id,
            "logs.txt",
            caption=f"{X}",
            reply_to_message_id=message.id,
        )
        await anuk.delete()
        os.remove("logs.txt")
    else:
        format_line = [f"┣ {line}" for line in out.splitlines()]
        if format_line:
            format_line[-1] = f"┖ {format_line[-1][2:]}"
        format_output = "\n".join(format_line)

        await pros.edit(f"<blockquote>{memeg}\n\n{teks}{format_output}</blockquote>", parse_mode="html")
    os.execl(sys.executable, sys.executable, "-m", "erNganu")