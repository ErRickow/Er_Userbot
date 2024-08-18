# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.


# -----------------Random Stuff--------------

import math

from telethon.tl import functions, types

from .. import LOGS

# -----------
# @buddhhu


async def get_uinfo(e):
    user, data = None, None
    reply = await e.get_reply_message()
    if reply:
        user = await e.client.get_entity(reply.sender_id)
        data = e.pattern_match.group(1)
    else:
        ok = e.pattern_match.group(1).split(maxsplit=1)
        if len(ok) > 1:
            data = ok[1]
        try:
            user = await e.client.get_entity(await e.client.parse_id(ok[0]))
        except IndexError:
            pass
        except ValueError as er:
            await e.eor(str(er))
            return None, None
    return user, data


# Random stuffs dk who added


async def get_chat_info(chat, event):
    if isinstance(chat, types.Channel):
        chat_info = await event.client(functions.channels.GetFullChannelRequest(chat))
    elif isinstance(chat, types.Chat):
        chat_info = await event.client(functions.messages.GetFullChatRequest(chat))
    else:
        return await event.eor("`Gunakan ini untuk group/channel.`")
    full = chat_info.full_chat
    chat_photo = full.chat_photo
    broadcast = getattr(chat, "broadcast", False)
    chat_type = "Channel" if broadcast else "Group"
    chat_title = chat.title
    try:
        msg_info = await event.client(
            functions.messages.GetHistoryRequest(
                peer=chat.id,
                offset_id=0,
                offset_date=None,
                add_offset=-0,
                limit=0,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
    except Exception as er:
        msg_info = None
        if not event.client._bot:
            LOGS.exception(er)
    first_msg_valid = bool(
        msg_info and msg_info.messages and msg_info.messages[0].id == 1
    )

    creator_valid = bool(first_msg_valid and msg_info.users)
    creator_id = msg_info.users[0].id if creator_valid else None
    creator_firstname = (
        msg_info.users[0].first_name
        if creator_valid and msg_info.users[0].first_name is not None
        else "Deleted Account"
    )
    creator_username = (
        msg_info.users[0].username
        if creator_valid and msg_info.users[0].username is not None
        else None
    )
    created = msg_info.messages[0].date if first_msg_valid else None
    if not isinstance(chat.photo, types.ChatPhotoEmpty):
        dc_id = chat.photo.dc_id
    else:
        dc_id = "Null"

    restricted_users = getattr(full, "banned_count", None)
    members = getattr(full, "participants_count", chat.participants_count)
    admins = getattr(full, "admins_count", None)
    banned_users = getattr(full, "kicked_count", None)
    members_online = getattr(full, "online_count", 0)
    group_stickers = (
        full.stickerset.title if getattr(full, "stickerset", None) else None
    )
    messages_viewable = msg_info.count if msg_info else None
    messages_sent = getattr(full, "read_inbox_max_id", None)
    messages_sent_alt = getattr(full, "read_outbox_max_id", None)
    exp_count = getattr(full, "pts", None)
    supergroup = "<b>Yes</b>" if getattr(chat, "megagroup", None) else "No"
    creator_username = "@{}".format(creator_username) if creator_username else None

    if admins is None:
        try:
            participants_admins = await event.client(
                functions.channels.GetParticipantsRequest(
                    channel=chat.id,
                    filter=types.ChannelParticipantsAdmins(),
                    offset=0,
                    limit=0,
                    hash=0,
                )
            )
            admins = participants_admins.count if participants_admins else None
        except Exception as e:
            LOGS.info(f"Exception: {e}")
    caption = "ℹ️ <blockquote>[<u>CHAT INFO</u>]</blockquote>\n"
    caption += f"🆔 <blockquote>ID: <code>{chat.id}</code></blockquote>\n"
    if chat_title is not None:
        caption += f"📛 <blockquote>{chat_type} nama: <code>{chat_title}</code></blockquote>\n"
    if chat.username:
        caption += f"🔗 <blockquote>Link: @{chat.username}</blockquote>\n"
    else:
        caption += f"🗳 <blockquote>{chat_type} type: Private</blockquote>\n"
    if creator_username:
        caption += f"🖌 <b>Creator: {creator_username}</blockquote>\n"
    elif creator_valid:
        caption += f'🖌 <blockquote>Creator: <a href="tg://user?id={creator_id}">{creator_firstname}</a></blockquote>\n'
    if created:
        caption += f"🖌 <blockquote>Created: <code>{created.date().strftime('%b %d, %Y')} - {created.time()}</code></blockquote>\n"
    else:
        caption += f"🖌 <blockquote>Created: <code>{chat.date.date().strftime('%b %d, %Y')} - {chat.date.time()}</code> ⚠</blockquote>\n"
    caption += f"🗡 <blockquote>Data Centre ID: {dc_id}</blockquote>\n"
    if exp_count is not None:
        chat_level = int((1 + math.sqrt(1 + 7 * exp_count / 14)) / 2)
        caption += f"⭐️ <blockquote>{chat_type} level: <code>{chat_level}</code></blockquote>\n"
    if messages_viewable is not None:
        caption += f"💬 <blockquote>Pesan Yang Kelihatan: <code>{messages_viewable}</code></blockquote>\n"
    if messages_sent:
        caption += f"💬 <blockquote>Pesan dikirim: <code>{messages_sent}</code></blockquote>\n"
    elif messages_sent_alt:
        caption += f"💬 <blockquote>Pesan dikirim: <code>{messages_sent_alt}</code> ⚠</blockquote>\n"
    if members is not None:
        caption += f"👥 <blockquote>Members: <code>{members}</code></blockquote>\n"
    if admins:
        caption += f"👮 <blockquote>Administrators: <code>{admins}</code></blockquote>\n"
    if full.bot_info:
        caption += f"🤖 <blockquote>Bots: <code>{len(full.bot_info)}</code></blockquote>\n"
    if members_online:
        caption += f"👀 <blockquote>Sedang Online: <code>{members_online}</code></blockquote>\n"
    if restricted_users is not None:
        caption += f"🔕 <blockquote>Restricted users: <code>{restricted_users}</code></blockquote>\n"
    if banned_users:
        caption += f"📨 <blockquote>Banned users: <code>{banned_users}</code></blockquote>\n"
    if group_stickers:
        caption += f'📹 <blockquote>{chat_type} stickers: <a href="t.me/addstickers/{full.stickerset.short_name}">{group_stickers}</a></blockquote>\n'
    if not broadcast:
        if getattr(chat, "slowmode_enabled", None):
            caption += f"👉 <blockquote>Slow mode: <code>True</code></blockquote>"
            caption += f", 🕐<blockquote> <code>{full.slowmode_seconds}s</code></blockquote>\n"
        else:
            caption += f"🦸‍♂ <b>Supergroup:</b> {supergroup}\n"
    if getattr(chat, "restricted", None):
        caption += f"🎌 <b>Restricted:</b> {chat.restricted}\n"
        rist = chat.restriction_reason[0]
        caption += f"> Platform: {rist.platform}\n"
        caption += f"> Reason: {rist.reason}\n"
        caption += f"> Text: {rist.text}\n\n"
    if getattr(chat, "scam", None):
        caption += "⚠ <b>Scam:</b> <b>Yes</b>\n"
    if getattr(chat, "verified", None):
        caption += f"✅ <b>Verified by Telegram:</b> <code>Yes</code>\n\n"
    if full.about:
        caption += f"🗒 <b>Description:</b> \n<code>{full.about}</code>\n"
    return chat_photo, caption
