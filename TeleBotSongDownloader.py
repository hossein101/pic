from pprint import pprint
import telepot
import time
import urllib2
import json

global BASE_URL
global flag
def getVidId(query):
    print "Debug2"
    api="#################################"
    query1=query.split()
    query2=('+').join(query1)
    url="https://www.googleapis.com/youtube/v3/search?part=id%2Csnippet&maxResults=1&q={}&key={}".format(query2,api)
    print url

    response=urllib2.urlopen(url)
    json_text=response.read()
    data=json.loads(json_text)

    vidId=data["items"][0]['id']['videoId']
    return vidId
######

def mp3send(url,chat_id):
    print "Debug3"
    flag=1
    print "title1 :",title1
    bot.sendMessage(chat_id,"Please wait,downloading your song now.Average downloading time is 2-4 minutes.")
    print "Downloading.."
    f=urllib2.urlopen(url)
    print "Downloading..."
    bot.sendAudio(chat_id,(title1+".mp3",f))
    print "Done"
    bot.sendMessage(chat_id,"Uploading finished.You may download your song now.Thanks for using me.")
    flag=0


def handle(msg):
    
    content_type, chat_type, chat_id = telepot.glance(msg)
    name=msg['from']['first_name']
    print msg
    if content_type=="text":
        command=msg['text']
        print 'Got command: %s'% command
    else:
        print content_type
        command=""
    pprint(msg)
    
    if command=='/start':
        bot.sendMessage(chat_id,"Hi "+name+",welcome to song downloader.Please send the song name and artist name in chat box.For example 'hello adele'")
    elif command=="":
        bot.sendMessage(chat_id,"Invalid command!Please enter the song and artist name to download song")
    else:
        if flag==1:
            bot.sendMessage(chat_id,"Server busy.Please try after 2-4 minutes.Sorry for inconvenience caused.")
            print "rejected"
        else:
            print "Debug1"
            query=command
            Id=getVidId(query)
            url=BASE_URL+Id
            print url
            content=urllib2.urlopen(url).read()
            json_data=json.loads(content)
            down_link=json_data['link']
            global title1
            title1=json_data['title']

            mp3send(down_link,chat_id)

BASE_URL="http://youtubeinmp3.com/fetch/?format=JSON&video=http://www.youtube.com/watch?v="
bot=telepot.Bot("243402180:AAF7QSJauUvJTbJUfxAehrW9PEojakoD26c")
flag=0
#print bot.getMe()
if flag==0:
    bot.message_loop(handle)

try:
    while 1:
        time.sleep(10)
except KeyboardInterrupt:
    print "Program Stopped!\nTerminating...."
    
