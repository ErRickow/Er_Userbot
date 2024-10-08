# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import asyncio
import os
import random
import shutil
import time
from random import randint

from ..configs import Var

try:
    from pytz import timezone
except ImportError:
    timezone = None

from telethon.errors import (
    ChannelsTooMuchError,
    ChatAdminRequiredError,
    MessageIdInvalidError,
    MessageNotModifiedError,
    UserNotParticipantError,
)
from telethon.tl.custom import Button
from telethon.tl.functions.channels import (
    CreateChannelRequest,
    EditAdminRequest,
    EditPhotoRequest,
    InviteToChannelRequest,
)
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.types import (
    ChatAdminRights,
    ChatPhotoEmpty,
    InputChatUploadedPhoto,
    InputMessagesFilterDocument,
)
from telethon.utils import get_peer_id
from decouple import config, RepositoryEnv
from .. import LOGS, ERConfig
from ..fns.helper import download_file, inline_mention, updater

db_url = 0


async def autoupdate_local_database():
    from .. import Var, asst, udB, eruser_bot

    global db_url
    db_url = (
        udB.get_key("TGDB_URL") or Var.TGDB_URL or eruser_bot._cache.get("TGDB_URL")
    )
    if db_url:
        _split = db_url.split("/")
        _channel = _split[-2]
        _id = _split[-1]
        try:
            await asst.edit_message(
                int(_channel) if _channel.isdigit() else _channel,
                message=_id,
                file="database.json",
                text="**Do not delete this file.**",
            )
        except MessageNotModifiedError:
            return
        except MessageIdInvalidError:
            pass
    try:
        LOG_CHANNEL = (
            udB.get_key("LOG_CHANNEL")
            or Var.LOG_CHANNEL
            or asst._cache.get("LOG_CHANNEL")
            or "me"
        )
        msg = await asst.send_message(
            LOG_CHANNEL, "**Do not delete this file.**", file="database.json"
        )
        asst._cache["TGDB_URL"] = msg.message_link
        udB.set_key("TGDB_URL", msg.message_link)
    except Exception as ex:
        LOGS.error(f"Error on autoupdate_local_database: {ex}")


def update_envs():
    """Update Var. attributes to udB"""
    from .. import udB
    _envs = [*list(os.environ)]
    if ".env" in os.listdir("."):
        [_envs.append(_) for _ in list(RepositoryEnv(config._find_file(".")).data)]
    for envs in _envs:
        if (
            envs in ["LOG_CHANNEL", "BOT_TOKEN", "BOTMODE", "DUAL_MODE", "language"]
            or envs in udB.keys()
        ):
            if _value := os.environ.get(envs):
                udB.set_key(envs, _value)
            else:
                udB.set_key(envs, config.config.get(envs))


async def startup_stuff():
    from .. import udB

    x = ["bahan/auth", "bahan/downloads"]
    for x in x:
        if not os.path.isdir(x):
            os.mkdir(x)

    CT = udB.get_key("CUSTOM_THUMBNAIL")
    if CT:
        path = "bahan/extra/cater.jpg"
        ERConfig.thumb = path
        try:
            await download_file(CT, path)
        except Exception as er:
            LOGS.exception(er)
    elif CT is False:
        ERConfig.thumb = None
    GT = udB.get_key("GDRIVE_AUTH_TOKEN")
    if GT:
        with open("bahan/auth/gdrive_creds.json", "w") as t_file:
            t_file.write(GT)

    if udB.get_key("AUTH_TOKEN"):
        udB.del_key("AUTH_TOKEN")

    MM = udB.get_key("MEGA_MAIL")
    MP = udB.get_key("MEGA_PASS")
    if MM and MP:
        with open(".megarc", "w") as mega:
            mega.write(f"[Login]\nUsername = {MM}\nPassword = {MP}")

    TZ = udB.get_key("TIMEZONE")
    if TZ and timezone:
        try:
            timezone(TZ)
            os.environ["TZ"] = TZ
            time.tzset()
        except AttributeError as er:
            LOGS.debug(er)
        except BaseException:
            LOGS.critical(
                "Format TimeZone Salah,\nBegini contohnya: Asia/Magelang\nWaktu Default UTC"
            )
            os.environ["TZ"] = "UTC"
            time.tzset()


async def autobot():
    from .. import udB, eruser_bot

    if udB.get_key("BOT_TOKEN"):
        return
    await eruser_bot.start()
    LOGS.info("SEDANG MEMBUATKAN BOT DI @BotFather, Sabar Dulu")
    who = eruser_bot.me
    name = who.first_name + "'s Bot"
    if who.username:
        username = who.username + "_bot"
    else:
        username = "ErUser_" + (str(who.id))[5:] + "_bot"
    bf = "@BotFather"
    await eruser_bot(UnblockRequest(bf))
    await eruser_bot.send_message(bf, "/cancel")
    await asyncio.sleep(1)
    await eruser_bot.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    isdone = (await eruser_bot.get_messages(bf, limit=1))[0].text
    if isdone.startswith("Gw gabisa.") or "20 bots" in isdone:
        LOGS.critical(
            "Tolong buat bot sendiri di @BotFather dan copy token bot sebagai vars BOT_TOKEN, dan restart."
        )
        import sys

        sys.exit(1)
    await eruser_bot.send_message(bf, name)
    await asyncio.sleep(1)
    isdone = (await eruser_bot.get_messages(bf, limit=1))[0].text
    if not isdone.startswith("Bagus sayang."):
        await eruser_bot.send_message(bf, "Asisstent Er Bot")
        await asyncio.sleep(1)
        isdone = (await eruser_bot.get_messages(bf, limit=1))[0].text
        if not isdone.startswith("Bagus sayang."):
            LOGS.critical(
                "Tolong buat bot sendiri di @BotFather dan copy token bot sebagai vars BOT_TOKEN, dan restart."
            )
            import sys

            sys.exit(1)
    await eruser_bot.send_message(bf, username)
    await asyncio.sleep(1)
    isdone = (await eruser_bot.get_messages(bf, limit=1))[0].text
    await eruser_bot.send_read_acknowledge("botfather")
    if isdone.startswith("maaf,"):
        ran = randint(1, 100)
        username = "eruser_" + (str(who.id))[6:] + str(ran) + "_bot"
        await eruser_bot.send_message(bf, username)
        await asyncio.sleep(1)
        isdone = (await eruser_bot.get_messages(bf, limit=1))[0].text
    if isdone.startswith("Sukses Sayangku ahhhhh!"):
        token = isdone.split("`")[1]
        udB.set_key("BOT_TOKEN", token)
        await enable_inline(eruser_bot, username)
        LOGS.info(
            f"Sukses membuat @{username} untuk digunakan sebagai Assistant Bot!"
        )
    else:
        LOGS.info(
            "Silahkan hapus beberapa bot di @BotFather dan copy token bot sebagai vars BOT_TOKEN, dan restart"
        )

        import sys

        sys.exit(1)


async def autopilot():
    from .. import asst, udB, eruser_bot

    channel = udB.get_key("LOG_CHANNEL")
    new_channel = None
    if channel:
        try:
            chat = await eruser_bot.get_entity(channel)
        except BaseException as err:
            LOGS.exception(err)
            udB.del_key("LOG_CHANNEL")
            channel = None
    if not channel:

        async def _save(exc):
            udB._cache["LOG_CHANNEL"] = eruser_bot.me.id
            await asst.send_message(
                eruser_bot.me.id, f"Gagal membuat logs channel karena {exc}.."
            )

        if eruser_bot._bot:
            msg_ = "'LOG_CHANNEL' tidak ditemukan! Tambahkan jikalau mau pake 'BOTMODE'"
            LOGS.error(msg_)
            return await _save(msg_)
        LOGS.info("Membuatkan Logs Channel untuk lu!")
        try:
            r = await eruser_bot(
                CreateChannelRequest(
                    title="Er Userbot Log",
                    about="Er Userbot Log Groups\n\n Join @pamerdong",
                    megagroup=True,
                ),
            )
        except ChannelsTooMuchError as er:
            LOGS.critical(
                "Lu terlalu banyak channel/group keluarkan dulu beberapa lalu restart botnya"
            )
            return await _save(str(er))
        except BaseException as er:
            LOGS.exception(er)
            LOGS.info(
                "Ada kesalahan!! buat bot sendiri di @BotFather dan copy token bot sebagai vars BOT_TOKEN, dan restart."
            )

            return await _save(str(er))
        new_channel = True
        chat = r.chats[0]
        channel = get_peer_id(chat)
        udB.set_key("LOG_CHANNEL", channel)
    assistant = True
    try:
        await eruser_bot.get_permissions(int(channel), asst.me.username)
    except UserNotParticipantError:
        try:
            await eruser_bot(InviteToChannelRequest(int(channel), [asst.me.username]))
        except BaseException as er:
            LOGS.info("Error ketika menambahkan assistant bot lu ke log group")
            LOGS.exception(er)
            assistant = False
    except BaseException as er:
        assistant = False
        LOGS.exception(er)
    if assistant and new_channel:
        try:
            achat = await asst.get_entity(int(channel))
        except BaseException as er:
            achat = None
            LOGS.info("Error ketika mendapatkan log channel dari group")
            LOGS.exception(er)
        if achat and not achat.admin_rights:
            rights = ChatAdminRights(
                add_admins=True,
                invite_users=True,
                change_info=True,
                ban_users=True,
                delete_messages=True,
                pin_messages=True,
                anonymous=False,
                manage_call=True,
            )
            try:
                await eruser_bot(
                    EditAdminRequest(
                        int(channel), asst.me.username, rights, "Assistant"
                    )
                )
            except ChatAdminRequiredError:
                LOGS.info(
                    "Gagal untuk promote 'Assistant Bot' di 'Log Channel' karena 'Admin Privileges'"
                )
            except BaseException as er:
                LOGS.info("Eror ketika jadikan admin Asisstent..")
                LOGS.exception(er)
    if isinstance(chat.photo, ChatPhotoEmpty):
        photo, _ = await download_file(
            "https://telegra.ph/file/d0e52259884ecaf763d13.jpg", "channelphoto.jpg"
        )
        ll = await eruser_bot.upload_file(photo)
        try:
            await eruser_bot(
                EditPhotoRequest(int(channel), InputChatUploadedPhoto(ll))
            )
        except BaseException as er:
            LOGS.exception(er)
        os.remove(photo)


# customize assistant


async def customize():
    from .. import asst, udB, eruser_bot

    rem = None
    try:
        chat_id = udB.get_key("LOG_CHANNEL")
        if asst.me.photo:
            return
        LOGS.info("Meng custom bot lu di @BOTFATHER")
        UL = f"@{asst.me.username}"
        if not eruser_bot.me.username:
            sir = eruser_bot.me.first_name
        else:
            sir = f"@{eruser_bot.me.username}"
        file = random.choice(
            [
                "https://telegra.ph/file/f35111938459684c20dfe.jpg",
                "https://telegra.ph/file/0ba5447759e13546a3122.jpg",
                "bahan/extra/erassistant.jpg",
            ]
        )
        if not os.path.exists(file):
            file, _ = await download_file(file, "profile.jpg")
            rem = True
        msg = await asst.send_message(
            chat_id, "**Auto Costumisasi** Dimulai di @Botfather"
        )
        await asyncio.sleep(1)
        await eruser_bot.send_message("botfather", "/cancel")
        await asyncio.sleep(1)
        await eruser_bot.send_message("botfather", "/setuserpic")
        await asyncio.sleep(1)
        isdone = (await eruser_bot.get_messages("botfather", limit=1))[0].text
        if isdone.startswith("Invalid bot"):
            LOGS.info("Error ketika mengkostum Assistant, skipping...")
            return
        await eruser_bot.send_message("botfather", UL)
        await asyncio.sleep(1)
        await eruser_bot.send_file("botfather", file)
        await asyncio.sleep(2)
        await eruser_bot.send_message("botfather", "/setabouttext")
        await asyncio.sleep(1)
        await eruser_bot.send_message("botfather", UL)
        await asyncio.sleep(1)
        await eruser_bot.send_message(
            "botfather", f"Allo gw Assistant Botnya {sir}"
        )
        await asyncio.sleep(2)
        await eruser_bot.send_message("botfather", "/setdescription")
        await asyncio.sleep(1)
        await eruser_bot.send_message("botfather", UL)
        await asyncio.sleep(1)
        await eruser_bot.send_message(
            "botfather",
            f"Er Userbot Assistant\nNganunya ~ {sir} \n\nSi Perusak @chakszzz",
        )
        await asyncio.sleep(2)
        await msg.edit("Selesai **Auto Costumisasi** di @BotFather.")
        if rem:
            os.remove(file)
        LOGS.info("Customisation Done")
    except Exception as e:
        LOGS.exception(e)


async def plug(plugin_channels):
    from .. import eruser_bot
    from .utils import load_addons

    if eruser_bot._bot:
        LOGS.info("Plugin Channel kga bisa digunakan di 'BOTMODE'")
        return
    if os.path.exists("addons") and not os.path.exists("addons/.git"):
        shutil.rmtree("addons")
    if not os.path.exists("addons"):
        os.mkdir("addons")
    if not os.path.exists("addons/__init__.py"):
        with open("addons/__init__.py", "w") as f:
            f.write("from plugins import *\n\nbot = eruser_bot")
    LOGS.info("• Loading Plugins dari Plugin Channel(s) •")
    for chat in plugin_channels:
        LOGS.info(f"{'•'*4} {chat}")
        try:
            async for x in eruser_bot.iter_messages(
                chat, search=".py", filter=InputMessagesFilterDocument, wait_time=10
            ):
                plugin = "addons/" + x.file.name.replace("_", "-").replace("|", "-")
                if not os.path.exists(plugin):
                    await asyncio.sleep(0.6)
                    if x.text == "#IGNORE":
                        continue
                    plugin = await x.download_media(plugin)
                    try:
                        load_addons(plugin)
                    except Exception as e:
                        LOGS.info(f"Er Userbot - PLUGIN_CHANNEL - ERROR - {plugin}")
                        LOGS.exception(e)
                        os.remove(plugin)
        except Exception as er:
            LOGS.exception(er)


# some stuffs


async def fetch_ann():
    from .. import asst, udB
    from ..fns.tools import async_searcher

    get_ = udB.get_key("OLDANN") or []
    chat_id = udB.get_key("LOG_CHANNEL")
    try:
        updts = await async_searcher(
            "https://ultroid-api.vercel.app/announcements", post=True, re_json=True
        )
        for upt in updts:
            key = list(upt.keys())[0]
            if key not in get_:
                cont = upt[key]
                if isinstance(cont, dict) and cont.get("lang"):
                    if cont["lang"] != (udB.get_key("language") or "id"):
                        continue
                    cont = cont["msg"]
                if isinstance(cont, str):
                    await asst.send_message(chat_id, cont)
                elif isinstance(cont, dict) and cont.get("chat"):
                    await asst.forward_messages(chat_id, cont["msg_id"], cont["chat"])
                else:
                    LOGS.info(cont)
                    LOGS.info(
                        "Invalid Type of Announcement Detected!\nMake sure you are on latest version.."
                    )
                get_.append(key)
        udB.set_key("OLDANN", get_)
    except Exception as er:
        LOGS.exception(er)


async def ready():
    from .. import asst, udB, eruser_bot

    chat_id = udB.get_key("LOG_CHANNEL")
    spam_sent = None
    if not udB.get_key("INIT_DEPLOY"):  # Detailed Message at Initial Deploy
        MSG = """🎇 **Terimakasih Telah Deploy Er Userbot!**
• Ini Basic stuff tentang cara penggunaan userbotnya."""
        PHOTO = "https://telegra.ph/file/c22cea683a0c0dd603fb1.jpg"
        BTTS = Button.inline("• Klik disini •", "initft_2")
        udB.set_key("INIT_DEPLOY", "Selesai")
    else:
        MSG = f"**Er Userbot Telah Terdeploy!**\n➖➖➖➖➖➖➖➖➖➖\n**UserMode**: {inline_mention(eruser_bot.me)}\n**Assistant**: @{asst.me.username}\n➖➖➖➖➖➖➖➖➖➖\n**Support**: @pamerdong\n➖➖➖➖➖➖➖➖➖➖"
        BTTS, PHOTO = None, None
        prev_spam = udB.get_key("LAST_UPDATE_LOG_SPAM")
        if prev_spam:
            try:
                await eruser_bot.delete_messages(chat_id, int(prev_spam))
            except Exception as E:
                LOGS.info("Error ketika menghapus update sebelumnya :" + str(E))
        if await updater():
            BTTS = Button.inline("Update Tersedia Cok", "updtavail")

    try:
        spam_sent = await asst.send_message(chat_id, MSG, file=PHOTO, buttons=BTTS)
    except ValueError as e:
        try:
            await (await eruser_bot.send_message(chat_id, str(e))).delete()
            spam_sent = await asst.send_message(chat_id, MSG, file=PHOTO, buttons=BTTS)
        except Exception as g:
            LOGS.info(g)
    except Exception as el:
        LOGS.info(el)
        try:
            spam_sent = await eruser_bot.send_message(chat_id, MSG)
        except Exception as ef:
            LOGS.exception(ef)
    if spam_sent and not spam_sent.media:
        udB.set_key("LAST_UPDATE_LOG_SPAM", spam_sent.id)
# TODO:    await fetch_ann()


async def WasItRestart(udb):
    key = udb.get_key("_RESTART")
    if not key:
        return
    from .. import asst, eruser_bot

    try:
        data = key.split("_")
        who = asst if data[0] == "bot" else eruser_bot
        await who.edit_message(
            int(data[1]), int(data[2]), "__Dah Selesai tod.__"
        )
    except Exception as er:
        LOGS.exception(er)
    udb.del_key("_RESTART")


def _version_changes(udb):
    for _ in [
        "BOT_USERS",
        "BOT_BLS",
        "VC_SUDOS",
        "SUDOS",
        "CLEANCHAT",
        "LOGUSERS",
        "PLUGIN_CHANNEL",
        "CH_SOURCE",
        "CH_DESTINATION",
        "BROADCAST",
    ]:
        key = udb.get_key(_)
        if key and str(key)[0] != "[":
            key = udb.get(_)
            new_ = [
                int(z) if z.isdigit() or (z.startswith("-") and z[1:].isdigit()) else z
                for z in key.split()
            ]
            udb.set_key(_, new_)


async def enable_inline(eruser_bot, username):
    bf = "BotFather"
    await eruser_bot.send_message(bf, "/setinline")
    await asyncio.sleep(1)
    await eruser_bot.send_message(bf, f"@{username}")
    await asyncio.sleep(1)
    await eruser_bot.send_message(bf, "Search")
    await eruser_bot.send_read_acknowledge(bf)
