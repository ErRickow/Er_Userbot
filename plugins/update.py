from . import get_help

__doc__ = get_help("help_updater")

import re
import asyncio
import os
import sys
import shutil
import subprocess

try:
    from git import Repo
except ImportError:
    LOGS.error("bot: 'gitpython' module not found!")
    Repo = None

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

def check_command(command):
    return shutil.which(command) is not None
    
@erubot_cmd(pattern="up( (.*)|$)")
async def _(e):
    xx = await e.reply(get_string("upd_1"))
    if e.pattern_match.group(1).strip() and (
        "fast" in e.pattern_match.group(1).strip()
        or "soft" in e.pattern_match.group(1).strip()
    ):
        await bash("git pull -f && pip3 install -r requirements.txt")
        call_back()
        await xx.edit(get_string("upd_7"))
        os.execl(sys.executable, "python3", "-m", "erNganu")
        # return
        out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
        teks = f"<b>❒ Status resources :</b>\n"
        memeg = f"<b>Perubahan logs </b>"
        if len(out) > 4096:
          anuk = await pros.edit(
            f"<blockquote> <b>Hasil akan dikirimkan dalam bentuk file ..</b></blockquote>"
        )
        with open("output.txt", "w+") as file: 
          file.write(out)

#os.remove("output.txt")
format_line = [f"┣ {line}" for line in out.splitlines()]
if format_line:
  format_line[-1] = f"┖ {format_line[-1][2:]}"
  format_output = "\n".join(format_line)
pros.edit(f"<blockquote>{memeg}\n\n{teks}{format_output}</blockquote>")
os.execl(sys.executable, sys.executable, "python3", "-m", "erNganu")
  
@callback("updtavail", owner=True)
async def updava(event):
    await event.delete()
    await asst.send_file(
        udB.get_key("LOG_CHANNEL"),
        ULTPIC(),
        caption="• **Update Available** •",
        force_document=False,
        buttons=Button.inline("Changelogs", data="changes"),
    )
