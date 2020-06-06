import asyncio

from pyrogram.errors.exceptions.bad_request_400 import YouBlockedUser

from userbot import userbot, Message


@userbot.on_cmd("quote", about={
    'header': "Quote a message",
    'usage': "{tr}quote [text or reply to msg]"})
async def quotecmd(message: Message):
    """quotecmd"""
    asyncio.get_event_loop().create_task(message.delete())
    args = message.input_str
    replied = message.reply_to_message
    async with userbot.conversation('QuotLyBot') as conv:
        try:
            if replied and not args:
                await conv.forward_message(replied)
            else:
                if not args:
                    await message.err('input not found!')
                    return
                await conv.send_message(args)
        except YouBlockedUser:
            await message.edit('first **unblock** @QuotLyBot')
            return
        quote = await conv.get_response(mark_read=True)
        if not quote.sticker:
            await message.err('something went wrong!')
        else:
            message_id = replied.message_id if replied else None
            await userbot.send_sticker(chat_id=message.chat.id,
                                      sticker=quote.sticker.file_id,
                                      file_ref=quote.sticker.file_ref,
                                      reply_to_message_id=message_id)