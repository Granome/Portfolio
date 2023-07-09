import logging
from dotenv import load_dotenv
import os
import json
import random
from questions import QUESTIONS, ANSWERS
from aiogram import Bot, Dispatcher, executor, types

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
admin = int(os.getenv('admin')) #admin's telegram ID
censored = os.getenv("censored") #string with words and phrases, that can't be searched
min_video_duration = 300 #default minumal length of saved vidos

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)



#ADMINS' FUNCTIONS

@dp.message_handler(content_types=["video"])
async def save_message(message: types.Message):
    """
    Adds videos to messages.txt file, when it is sent to the bot.
    messages.txt - file, that stores ids, original channel name and description of video.
    All of this videos can be used from bot-admin chat.
    """
    if message.chat.id ==  admin:
        if message.caption:
            if message.video.duration > min_video_duration: #ignores videos, shorter than min_video_duration in seconds
                dictToSave = {}
                dictToSave["message_id"] = message.message_id
                if message.forward_from_chat.username == None:
                    dictToSave["forward_from_chat"] = "Видалений канал"
                else:
                    dictToSave["forward_from_chat"] = message.forward_from_chat.username
                dictToSave["text"] = message.caption.lower().replace("_", " ").replace("\"", "'").replace("'", "-")
                with open ("messages.txt", "a", encoding="UTF-8") as f:
                    f.write(str(dictToSave) + "\n")
        else:
            await bot.send_message(message.chat.id, "У відео нема опису")
            

@dp.message_handler(commands=["getFile"])
async def getFile(message:types.Message):
    """
    Sends messages.txt file in telegram to admins only
    """
    if message.chat.id ==  admin:
        with open ("messages.txt", "rb") as fp:
            await bot.send_document(message.chat.id, fp)


@dp.message_handler(commands=["getUsersFile"])
async def get_users_file(message: types.Message):
    """
    Sends UseraActions.txt file
    """
    if message.chat.id ==  admin:
        with open ("UsersActions.txt", "rb") as fp:
            await bot.send_document(message.chat.id, fp)


@dp.message_handler(content_types=["document"])
async def SaveDocument(message:types.Message):
    """
    Saves received messages.txt and UsersActions.txt file in virtual environment, so you
    don't have to commit it in git it every time.
    """

    if message.chat.id ==  admin:
        if message.document.file_name in ["messages.txt", "UsersActions.txt"]:
            #getting file path and downloading it from telegram's servers
            file_id = message.document.file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path
            await bot.download_file(file_path, message.document.file_name)
            
            await bot.send_message(chat_id=message.chat.id, text="Saved successfully")
        else:
            await bot.send_message(chat_id=message.chat.id, text=f"I dont know this file({message.document.file_name})")


@dp.message_handler(commands=["clear"])
async def clearfile(message: types.Message):
    """
    Clears messages.txt file
    """
    if message.chat.id ==  admin:
        open("messages.txt", "w").close()


@dp.message_handler(commands=["SetMinVideoDuration"])
async def SetMinVidDuration(message:types.Message):
    """
    Function get number from command and saves it into min_video_duration variable
    """
    global min_video_duration

    if message.chat.id == admin:
        try:
            min_video_duration = int(message.text[21:])
            await bot.send_message(chat_id=message.chat.id, text=f"Duration set to {min_video_duration}")
        except:
            ValueError
            await bot.send_message(chat_id=message.chat.id, text="Please give me number") 

@dp.message_handler(commands=["SendTextMessage"])
async def SendTextMessage(message:types.Message):
    """
    Function, that sends text message from bot to someone, who alredy used him
    Reads admin's command and separete smessage to get username and text 
    """
    if message.chat.id == admin:
        target = message.text.split("|")[1]
        text = message.text.split("|")[2]
        await bot.send_message(chat_id=admin, text="Text was sent seccuessfully")
        await bot.send_message(chat_id=target, text=text)

@dp.message_handler(commands=["GetUserProfile"])
async def startFunc(message: types.Message):
    """
    Sends link to user's profile, using his id
    """   
    id = message.text.split("|")[1]
    await bot.send_message(message.chat.id, text=f"[Ось, тримай, повелителю ботів](tg://user?id={id})", parse_mode="MarkdownV2")



#USERS' FUNCTIONS

@dp.message_handler(commands=["start"])
async def startFunc(message: types.Message):
    """
    Starting bot and sending instructions
    """
    #saving action
    if message.chat.id != admin:
        await saveUser(message.date.strftime('%Y/%m/%d %H:%M:%S'), message.from_user.username, message.chat.id, message.text, message.from_user.id)
   
    await bot.send_message(message.chat.id, "Добрий день. Цей бот допоможе вам знайти будь-яке аніме, яке є в каналах українських даберів. Ви отримаєте всі серії підряд, та зможете дивитися їх прямо в телеграмі. Щоб знайти аніме, просто напишіть частину його назви цьому боту. Якщо виникнуть запитання, напишіть /questions")


@dp.message_handler(commands=["random"])
async def randomVideo(message:types.Message):
    """
    Sends random available video
    """
    
    with open ("messages.txt", "r", encoding="UTF-8") as fp:
        line = next(fp)
        for num, aline in enumerate(fp, 2):
            if random.randrange(num):
                continue
            line = aline
        readedDict = json.loads(line.replace("'", "\""))
        await bot.forward_message(message.chat.id, admin, readedDict["message_id"])


@dp.message_handler(commands=["Questions"])
async def ShowQuestions(message:types.Message):
    await bot.send_message(message.chat.id, QUESTIONS, parse_mode="MarkdownV2")

@dp.message_handler(commands=["Q1", "Q2", "Q3", "Q4", "Q5"])
async def ShowAnswer(message:types.Message):
    """
    This function shows answers to requested questions
    """
    question = message.text[:3]
    await bot.send_message(message.chat.id, text=ANSWERS[question].replace(".", "\."), parse_mode="MarkdownV2")
    if message.chat.id != admin:
        await saveUser(message.date.strftime('%Y/%m/%d %H:%M:%S'), message.from_user.username, message.chat.id, message.text, message.from_user.id)
   


@dp.message_handler(content_types=["text"])
async def Search(message: types.Message): 
    """
    Searches and sends video to user.

    Searches by text, that is sent to bot, inside saved videos descriptions.
    Found information is saved in dict(resDictionary) and then bot sends videos by found ids.
    """

    chatID = message.chat.id
    #saving action
    if message.chat.id !=  admin:
        await saveUser(message.date.strftime('%Y/%m/%d %H:%M:%S'), message.from_user.username, chatID, message.text, message.from_user.id)
    #check if search key is valid
    if len(message.text) <= 3:
        await bot.send_message(message.chat.id, "Вкажіть назву з чотирьох або більше букв")
        return
    elif message.text in censored: #censored stores words and prases that can be in many different videous descriptions (such as "episode")
        await bot.send_message(message.chat.id, "Ви не можете цього шукати")
        return
    resDictionary = {} 
    SearchKey = message.text.lower().replace("'", "-").replace("\"", "-")
 

    with open ("messages.txt", "r", encoding="UTF-8") as f:
        for mstext in f:
            readedDict = json.loads(mstext.replace("'", "\""))

            if SearchKey in readedDict["text"]:
                channelTitle = "@" + readedDict["forward_from_chat"]
                msgId = readedDict["message_id"]

                #channelTitle is key in resDictionary that stores list of ids ({"@channel1" : [1, 2], @channel2" : [3, 4]})
                current_ids_list = resDictionary.get(channelTitle, [])
                current_ids_list.append(msgId)
                resDictionary[channelTitle] = current_ids_list
        if len(resDictionary) > 0:
            await bot.send_message(chatID, f"Вдалося знайти в {len(resDictionary)} даберів. Відправляю всі відео по черзі:")

            for i in resDictionary:
                await bot.send_message(chatID, i)
                for j in resDictionary[i]:
                    await bot.forward_message(message.chat.id, admin, j)            
        else:
            await bot.send_message(message.chat.id, "Не вдалося нічого знайти. Перевірте правильність написання, погляньте в пораду, написавши /Q3. Якщо написано правильно, жоден  з підтримуваних даберів не озвучував цього. Щоб побачити список каналів, в яких бот провидить пошук, напишіть /Q1")




async def saveUser(date, username, chat_id, message_text, user_id=None):
    """Function, that handle saving users' actions in file.
    Data have to be saved in format: {"date":date_time, "username":@username, "chat_id":id, "action":message_text}
    Action is command or search query
    """
    if username == None:
        user = "id:" + str(user_id)
    else:
        user = username

    savedData = {"date":date, "username":"@"+user, "chat_id":chat_id, "action":message_text}
    #save into file
    with open ("UsersActions.txt", "a", encoding="UTF-8") as fp:
        fp.write(str(savedData)+"\n")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)