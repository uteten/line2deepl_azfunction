import azure.functions as func
import logging

import os
import io
import re
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (ImageMessage, MessageEvent,
                            TextMessage, TextSendMessage)
import DeepL, AzureVision, ChatGPT



# LINE設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ['CUSTOMCONNSTR_LINE_CHANNEL_ACCESS_TOKEN']
LINE_CHANNEL_SECRET = os.environ['CUSTOMCONNSTR_LINE_CHANNEL_SECRET']
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

def iterable_to_stream(iterable, buffer_size=io.DEFAULT_BUFFER_SIZE):
    class IterStream(io.RawIOBase):
        def __init__(self):
            self.leftover = None

        def readable(self):
            return True

        def readinto(self, b):
            try:
                ll = len(b)  # We're supposed to return at most this much
                chunk = self.leftover or next(iterable)
                output, self.leftover = chunk[:ll], chunk[ll:]
                b[:len(output)] = output
                return len(output)
            except StopIteration:
                return 0    # indicate EOF
    return io.BufferedReader(IterStream(), buffer_size=buffer_size)

def getWords(en_text_all):
    teacher=ChatGPT.ChatGPT("dmy",1)
    words=teacher.generate_answer("以下に含まれる英文から、TOEIC500程度の人がわからなそうな単語や慣用句の意味と似た意味の英単語を[行番号. 単語や慣用句:単語の品詞// 日本語の意味 // 似た意味の英単語,似た意味の英単語..]の形式で単語ごとに行を分けて列挙せよ。以下の英語以外は無視してください\n"+en_text_all)
    words=words.replace("詞 //","詞//").replace("名詞//","[名]").replace("副詞//","[副]").replace("動詞//","[動]").replace("形容詞//","[形]").replace("慣用句//","[慣用句]").replace("固有名詞//","[固]").replace("adverb //","[副]").replace("phrase //","[句]").replace("noun //","[名]").replace("verb //","[動]").replace("adjective //","[形]")
    return words

app = func.FunctionApp()
@app.function_name(name="HttpTrigger1")
@app.route(route="hello")
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('----------- triger start ---------------')
    signature = ""
    if 'X-Line-Signature' in req.headers:
        signature = req.headers['X-Line-Signature']
    body = req.get_body().decode()
    logging.info(["body::",body])
    #logging.info(["signature::",signature])

    handler.handle(body, signature)
    return func.HttpResponse("ok", status_code=200)
"""
    try:
        handler.handle(body, signature)
        return func.HttpResponse("ok", status_code=200)
    except InvalidSignatureError:
        logging.info("in error")
        return func.HttpResponse("damepox2")
"""


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    logging.info("in text handler")
    logging.info(["en_text::", event.message.text])
    reply=""
    en_text=event.message.text
    if re.search(r'[あ-んア-ン]', en_text):
        logging.info("日本語")
        en_text = DeepL.DeepL().translateText(en_text,'EN')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=en_text))
    else:
        logging.info("英語")
        jp_text = DeepL.DeepL().translateText(en_text,'JA')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=jp_text))
    # chatgptt単語翻訳やめた
    #words=getWords(en_text)
    #line_bot_api.push_message(event.source.user_id,TextSendMessage(text=words))

@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    logging.info("in image handler")
    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)
    stream = iterable_to_stream(message_content.iter_content())
    en_text_all = AzureVision.AzureVision().image2text(stream)
    reply=""
    for en_text in en_text_all.split(". "):
        if not re.match(r'(\.|\?)$', en_text):
            en_text+= "."
        logging.info(["en_text::", en_text])
        jp_text = DeepL.DeepL().translateText(en_text.replace("\n", " "),'JA')
        reply+= "E: " + en_text + "\nJ: " + jp_text + "\n"
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply))
    # chatgptt単語翻訳やめた
    #words=getWords(en_text_all)
    #line_bot_api.push_message(event.source.user_id,TextSendMessage(text=words))
