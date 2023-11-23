import discord
from discord.ext import commands 
from discord import app_commands
import requests
from PIL import Image 
import cv2 
import json
import base64
import asyncio
import imageio
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import datetime
import random
import nest_asyncio
nest_asyncio.apply()

intents = discord.Intents.all() # intents是要求機器人的權限
def __init__(self, bot):
    self.bot = bot
    
with open('setting.json', 'r', encoding='utf8') as jfile: 
    jdata = json.load(jfile)

bot = commands.Bot(command_prefix='/', intents=intents) #設定前綴符號
bot.remove_command("help")

@bot.event
async def on_ready():
  print("tmu bot on !")
  synced = await bot.tree.sync()
  print(str(len(synced))+"  com")

   
@bot.tree.command(name="help",description="show all useful commands") #設定help
async def help(interaction:discord.Interaction):
  embed=discord.Embed(color=0x0080ff,title="Commands Menu") #設定嵌入訊息
  embed.add_field(name="ping", value="顯示ping值", inline=False)
  embed.add_field(name="repeat" , value="輸入次數與想重複的訊息", inline=False)
  embed.add_field(name="avatarchange",value="change one's avatar",inline=False)
  embed.add_field(name="wordgif" , value="send wordgif", inline=False)
  embed.add_field(name="lottery" , value="抽運勢", inline=False)
  embed.add_field(name="homework",value="check deadline of homework", inline=False)
  embed.add_field(name="christmastree",value="生成一個聖誕樹～", inline=False)
  await interaction.response.send_message(embed=embed) 

    

@bot.tree.command(name="ping",description="show ping")
async def ping(interaction:discord.Interaction):
    await interaction.response.send_message(content=f'{round(bot.latency*1000)} (ms)') #顯示bot延遲

@bot.event
async def on_member_join(member): #有人加入伺服器
    channel = bot.get_channel(1164849901188956250) #設定傳訊息頻道
    await channel.send(f'{member} join!')

@bot.event
async def on_member_remove(member): #有人離開伺服器
    channel = bot.get_channel(1164849918863745135)
    await channel.send(f'{member} leave!')  

@bot.tree.command(name="lottery",description="抽運勢")
async def lottery(interaction:discord.Interaction):
  result = ''
  grossfortune = ''
  result += ("歡迎來到抽運勢程式！")
  result +='\n'
  fortunes = ["好運即將降臨，保持積極態度！","事情可能有些波折，但不要放棄希望。","愛情運勢看好，有機會遇到意想不到的驚喜。","健康方面需要注意，多注意休息。","新的機會即將到來，抓住它吧！"]
  lucky_number = random.randint(1, 100)
  fortune = random.choice(fortunes)
  result += ("目前運勢： ")
  result += fortune
  result += '\n'
  result += ("幸運指數：")
  result += str(lucky_number)
  result += '\n'
  index = ["凶", "大凶","平","吉","大吉"]
  if lucky_number >= 80:
      grossfortune = index[4]
  elif lucky_number < 80 and lucky_number >=60:
      grossfortune = index[3]
  elif lucky_number < 60 and lucky_number >=40:
      grossfortune = index[2]
  elif lucky_number < 40 and lucky_number >=20:
      grossfortune = index[0]
  elif lucky_number < 20:
      grossfortune = index[1]
  result += '未來運勢: '
  result += grossfortune
  await interaction.response.send_message(result)

@bot.tree.command(name="test",description="test")
async def test(interaction:discord.Interaction):
  result = "test"
  await interaction.response.send_message(result)

@bot.tree.command(name="christmastree",description="生成一個聖誕樹～")
async def christmastree(interaction:discord.Interaction):
    leaf_item = ['*','O','@','/','+']
    leaf_base = '^'
    trunk_body = '|'
    trunk_base = '~'
    left_space = 0
    right_space = 0
    middle_leaf = 0
    order = 5
    max_number = 3
    output = ''
    output_leaf = ''
    
    for i in range(0, order):
        max_number += 4 * i
        c = ''
    
    for i in range(0, order):
        layer = (i + 3)
        for j in range(0, layer):
            leaf_number = int(((2 * i - 1 + j) * 2) + 1) + random.randint(0, 2)
            left_space = int((max_number - leaf_number)/2)
            right_space = int((max_number - leaf_number)/2)
            middle_leaf = leaf_number
            output_leaf = ''
            for k in range(0, leaf_number):
                if (k == 0 or k == (leaf_number - 1)):
                    output_leaf += ''
                else:
                    output_leaf += leaf_item[random.randint(0, 4)]
            output = ' ' * left_space + output_leaf + ' ' * right_space
            c += (output)
            c += '\n'
    
    for m in range(0, 3):
        left_space = int((max_number - 5)/2)
        right_space = int((max_number - 5)/2)
        middle_trunk = '|||||'
        output_trunk = ' ' * left_space + middle_trunk + ' ' * right_space
        c += (output_trunk)
        c += '\n'
        
    for n in range(0, max_number):
        c += (trunk_base)
    embed = discord.Embed(title="Christmas Tree", description=f"```{c}```", color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="repeat",description="repeat!")
async def repeat(interaction:discord.Interaction,次數:int,訊息:str):
    calltimes=0 #計算次數
    if int(次數)<=10:
        await interaction.response.send_message("成功傳送",ephemeral=True) #message should only be visible to the user
        while calltimes < int(次數):
            await interaction.channel.send(訊息)
            calltimes+=1
    else:
        await interaction.response.send_message("次數過多 最多重複10次!")
        
@bot.tree.command(name="avatarchange",description="change the avatar")
@app_commands.choices(what=[
  discord.app_commands.Choice(name='bubble', value=1),
  discord.app_commands.Choice(name='ban', value=2),
  discord.app_commands.Choice(name='rip', value=3)])
async def avatarchange(interaction:discord.Interaction,who:discord.User,what:discord.app_commands.Choice[int]):
    await interaction.response.send_message("please wait!",ephemeral=True)
    url=who.display_avatar.url
    r = requests.get(url)
    with open('D:/cache_data/Desktop/tmu/makepicture/reqavatar.png', 'wb') as outfile:
      outfile.write(r.content) #寫入頭貼
    imageA = Image.open('D:/cache_data/Desktop/tmu/makepicture/reqavatar.png')
    imageA = imageA.convert("RGBA")
    imageB = Image.open('D:/cache_data/Desktop/tmu/makepicture/tex_live_bubble.png')
    imageB = imageB.convert("RGBA")
    imageC = Image.open('D:/cache_data/Desktop/tmu/makepicture/ban.png')
    imageC = imageC.convert("RGBA")
    imageD = Image.open('D:/cache_data/Desktop/tmu/makepicture/rip.png')
    imageD = imageD.convert("RGBA")
    wA=imageA.width #找寬度
    hA=imageA.height #找高度
    if what.value ==1:
      neww=150/wA 
      newh=150/hA
      newimageA  = imageA.resize((int(wA*neww),int(hA*newh))) #重新設定長寬為150
      resultPicture = Image.new('RGBA', imageB.size, (0, 0, 0, 0)) #設定背景
      resultPicture.paste(newimageA,(53,53)) #先貼頭貼 在(53,53)的方位
      resultPicture.paste(imageB, (0,0),imageB) #再貼泡泡
      resultPicture.save("D:/cache_data/Desktop/tmu/makepicture/doneavatar.png") #儲存合成得照片
      pic = discord.File("D:/cache_data/Desktop/tmu/makepicture/doneavatar.png")
      await interaction.channel.send(file=pic) #傳照片
    elif what.value ==2:
      neww=150/wA
      newh=150/hA
      newimageA  = imageA.resize((int(wA*neww),int(hA*newh)))
      resultPicture = Image.new('RGBA', imageC.size, (0, 0, 0, 0))
      resultPicture.paste(newimageA,(53,53))
      resultPicture.paste(imageC, (0,0),imageC)
      resultPicture.save("D:/cache_data/Desktop/tmu/makepicture/banavatar.png")
      pic = discord.File("D:/cache_data/Desktop/tmu/makepicture/banavatar.png")
      await interaction.channel.send(file=pic)
    elif what.value == 3:
      image = cv2.imread("D:/cache_data/Desktop/tmu/makepicture/reqavatar.png")
      greyimg=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #將影像從彩色轉換成灰階
      cv2.imwrite("D:/cache_data/Desktop/tmu/makepicture/grayavater.png",greyimg)
      imageA = Image.open('D:/cache_data/Desktop/tmu/makepicture/grayavater.png')
      imageA = imageA.convert("RGBA")
      wA=imageA.width
      neww=80/wA
      hA=imageA.height
      newh=80/hA
      newimageA  = imageA.resize((int(wA*neww),int(hA*newh)))
      resultPicture = Image.new('RGBA', imageD.size, (0, 0, 0, 0))
      resultPicture.paste(imageD, (0,0))
      resultPicture.paste(newimageA,(88,100))
      resultPicture.save("D:/cache_data/Desktop/tmu/makepicture/ripavatar.png")
      pic = discord.File("D:/cache_data/Desktop/tmu/makepicture/ripavatar.png")
      await interaction.channel.send(file=pic)

@bot.tree.command(name="wordgif",description="send wordgif")
async def wordgif(interaction:discord.Interaction,words:str):
    await interaction.response.send_message("please wait!",ephemeral=True)
    sa=words
    for x in range(len(sa)):    
      s=sa[x]
      count=x+1
      count=str(count)
      tcount=count.zfill(2) #設定指定長度的字串
      url="https://www.arttopng.com/typedownload.php?r=255&g=255&b=255&text={}&font=https://www.arttopng.com/chinese/font/art.ttf".format(s)
      r = requests.get(url)
      soup = BeautifulSoup(r.text,'html.parser')
      images = soup.find_all('img') #找有img
      for image in images:
        link = image['src']
        if link.startswith('data') == True:
          break
      link=link[22:] #刪除前面的data:image/png;base64,
      data = '''{}'''.format(link)
      img = base64.urlsafe_b64decode(data + '=' * (4 - len(data) % 4))
      with open('D:/cache_data/Desktop/tmu/makepicture/文字/try{}.png'.format(tcount), 'wb') as outfile:
        outfile.write(img)
      img=Image.open('D:/cache_data/Desktop/tmu/makepicture/文字/try{}.png'.format(tcount))
      cutimg= img.crop((300,50,500,250))
      cutimg.save('D:/cache_data/Desktop/tmu/makepicture/文字/try{}.png'.format(tcount))

    giflist=[]
    for i in range(len(sa)):
      t=str(i+1)
      tcount=t.zfill(2)
      imageA = Image.open('D:/cache_data/Desktop/tmu/makepicture/文字/try{}.png'.format(tcount))
      imageA = imageA.convert("I")
      giflist.append(imageA) #把照片加到list中
    imageio.mimwrite("D:/cache_data/Desktop/tmu/makepicture/文字/trygif.gif", giflist,fps=4) #按照list順序生成gif
    pic = discord.File("D:/cache_data/Desktop/tmu/makepicture/文字/trygif.gif")
    await interaction.channel.send(file=pic)

@bot.tree.command(name="homework",description="check deadline of homework")
async def homework(interaction:discord.Interaction,imtmu帳號:str,imtmu密碼:str):
  await interaction.response.send_message("please wait!",ephemeral=True) #防止別人看到帳號密碼
  options=Options()
  options.chrome_executable_path="chromedriver.exe" 
  driver = webdriver.Chrome(options=options)
  url="https://im.tmu.edu.tw/dashboard/latestEvent"
  driver.get(url) 
  iddd=driver.find_element(By.NAME,"account") #用name找到輸入帳號位置
  iddd.send_keys(imtmu帳號)
  iddd=driver.find_element(By.NAME,"password") #用name找到輸入密碼位置
  iddd.send_keys(imtmu密碼)
  driver.find_element(By.XPATH,'//button').click() #點登入鍵
  time.sleep(3)
  try:
    driver.find_element(By.CLASS_NAME,'btn.btn-default.keepLoginBtn').click() #空格改. 點保持登入鍵
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    divs = soup.find_all('div',class_="fs-text-center") #找到姓名的class 
    alc=""
    for div in divs:
        alc+=div.text #把所有class是 fs-text-center 的文字合併
    nm=alc.split("等級") #等級前面的字就是姓名 所以用等級切割
    yourname=nm[0]

    trs = soup.find_all('tr') 
    count=0
    task=[] #作業名稱
    classs=[] #課程名稱
    timee=[] #deadline
    lasttime=[] #剩餘天數
    for tr in trs:
        wd=tr.text
        if count!=0: #第一個是 標題來源期限 所以第一個要略過
            r=wd.split("\n")
            task.append(r[0])
            classs.append(r[1])
            timee.append(r[2])
            localtime = datetime.datetime.now()
            chtime=r[2]
            endtime =datetime.datetime.strptime(chtime,"%Y-%m-%d") #把時間轉成datetime.datetime形式
            minus=endtime-localtime #檢查剩下幾天
            lasttime.append(minus.days+1)
        count+=1
    checklink=[] #作業的連結
    hfs = soup.find_all('a')
    for hf in hfs:
            link = hf['href']
            if link.startswith('/course/homework') == True or link.startswith('/course/questionnaire') == True or link.startswith('/course/exam') == True:
                link="https://im.tmu.edu.tw"+link
                checklink.append(link)
    donelist=[] #確認有沒有做
    for i in range(len(checklink)):
        url=checklink[i]
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        hfs = soup.find_all('a')
        done=0
        for hf in hfs:
                rr=hf.text.replace(' ', '') #刪除空白
                try:
                    if rr=="交作業" : #如果沒交作業 會有交作業這個按鈕
                        done+=1
                    elif rr =="開始填寫":
                        done+=1
                    elif rr=="開始測驗":
                        done+=1
                except:
                    pass
        if done!=0:
            donelist.append("x")
        else:
            donelist.append("✓")
    word="{}的作業繳交進度\n".format(yourname)
    word+='{:<6} {:<1} {:<3} {:<11} \n'.format("繳交期限","完成","剩下天數","作業")
    for i in range(len(task)): 
        word+='{:<11} {:<5} {:<3} {:<11} \n'.format(timee[i],donelist[i],lasttime[i],task[i])
        if len(word)>1900:
          await interaction.channel.send(f'```{word}```')
          word="{}的作業繳交進度\n".format(yourname)
          word+='{:<6} {:<1} {:<3} {:<11} \n'.format("繳交期限","完成","剩下天數","作業")
    await asyncio.sleep(5)
    await interaction.channel.send(f'```{word}```')
  except:
    await interaction.channel.send("帳號密碼輸入錯誤") #帳號密碼錯誤 會沒保持登入鍵 可以按

bot.run(jdata['TOKEN']) #隱藏token
