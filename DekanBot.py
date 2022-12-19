import telebot
import pymongo
import random
import numpy as np
import threading

bot = telebot.TeleBot('1061329648:AAFb0ExHkofy2LEv4DKrJv18dxm0ydtysoc')
db_client = pymongo.MongoClient("mongodb+srv://wotrex:i98wbdz9@bohdanbot.rnchtwf.mongodb.net/?retryWrites=true&w=majority")
dat = db_client['BohdanBot']['Chats']


timechat = {}

def mytimer(chatid):
    if len(dat.find_one({'id': chatid})['mem_to_game']) >= 2:
        game(chatid, dat.find_one({'id': chatid})['mem_to_game'])
        dat.update_one({'id': chatid},{ "$set": { 'mem_to_game': [] } })
        dat.update_one({'id': chatid},{ "$set": { 'g_status': 0 } })
        timechat.pop(chatid)
    else:
        dat.update_one({'id': chatid},{ "$set": { 'mem_to_game': [] } })
        dat.update_one({'id': chatid},{ "$set": { 'g_status': 0 } })
        bot.send_message(chat_id=chatid, text='Достатня кількість учасників не набралась, гру відмінено')
        timechat.pop(chatid)
       
def game(chadid, players):
    players3 = np.zeros((0), dtype = [('name', object),('role', object),('died', object),('count', int), ('money', int)])
    mm = dat.find_one({'id': chadid})['members']
    for p in range(len(players)):
        players3 = np.insert(players3, len(players3),(players[p],None,None,0,0), axis = 0)
        if  mm.__contains__(players[p]) == False:
            mm[players[p]] = {'wins':0,'kills':0,'lose':0, 'money':0}
    def storonu():
        for p in range(len(players)):
            players3[p][1] = None
        countPlr = []
        for p in range(len(players)):
            countPlr.append(p)
        allReady = 0
        while 1:
            if allReady == len(players):
                break
            randomPlayer = random.choice(countPlr)
            rand = random.randint(1,3)
            def randRole():
                if rand == 1:
                    if np.count_nonzero("Мєнт" == players3['role']) <= np.count_nonzero("Разбойнік" == players3['role']):
                        players3[randomPlayer][1] = "Мєнт"
                    else:
                        players3[randomPlayer][1] = "Разбойнік"
                if rand == 2:
                    if np.count_nonzero("Мєнт" == players3['role']) >= np.count_nonzero("Разбойнік" == players3['role']):
                        players3[randomPlayer][1] = "Разбойнік"
                    else:
                        players3[randomPlayer][1] = "Мєнт"
            randRole()
            if rand == 3:
                if np.count_nonzero("Мер" == players3['role']) == 0:
                    players3[randomPlayer][1] = "Мер"
                else:
                    rand = random.randint(1,2)
                    randRole()
            countPlr.remove(randomPlayer)
            allReady += 1
    storonu()
    while 1 :
        if len(players) != 2:
            if "Мер" in players3[:][1]:
                break
            else:
                storonu()
        else:
            break
    message = ""
    for k in range(len(players)):
        if players3[k][0] != None:
            message += ("@{} - {}\n".format(players3[k][0], players3[k][1]))
    bot.send_message(chadid, message)
    countPlayer = []
    for p in range(len(players)):
        countPlayer.append(p)
    lifeMer = 1
    rabstvo = []
    avtoritet = 0
    for l in countPlayer:
        if players3[l][1] == "Разбойнік":
            avtoritet += 1
    avtoritet_changable = avtoritet + 1
    message = ""
    def raund():
        nonlocal message
        def win(hunter, victim, H1, h1, h2, V1, V2, v2, win_g, win_m):
            rep = random.randint(1,5)
            nonlocal message
            if rep == 1:
                message += ("{} @{} знищив очко {} @{} \n \n".format(H1, hunter, v2, victim))
            if rep == 2:
                message += ("{} @{} розтарабанив очко {} @{} \n \n".format(H1, hunter, v2, victim))
            if rep == 3:
                message += ("{} @{} кінчив в штани коли його їбав {} @{} \n \n".format(V1, victim, h1, hunter))
            if rep == 4:
                message += ("{} @{} спіткала анальна кара {} @{} \n \n".format(V2, victim, h2, hunter))
            if rep == 5:
                message += ("Ракета {} @{} стрімко влетіла в чорну диру {} @{} \n \n".format(h2, hunter, v2, victim))
            if win_m:
                message += ("{} @{} потрапив в анальне рабство до {} @{} \n".format(V1, victim, h2, hunter))
                message += ("Анальні раби {} @{}: ".format(h2, hunter))
                for k in rabstvo:
                    message += ("@{}, ".format(k))
                message = message[:-4]
                message += " \n \n"
            if win_g:
                money = []
                potential_money = [5000, 10000, 15000, 20000, 25000, 30000, 40000, 50000, 75000, 100000]
                for l in range(len(Gangster)):
                    money.append(random.choice(potential_money))
                numb = 0
                players3[p][4] += max(money)
                max_money = max(money)
                money.remove(max(money))
                for l in Gangster:
                    if players3[l][0] != players3[p][0]:
                        players3[l][4] += money[numb]
                        numb += 1
                message += ("{} @{} залутав з мера {}$. Гроші розділені між разбойніками \n".format(H1, hunter, str(sum(money)+max_money)))
                for l in Gangster:
                    message += ("{} @{} тепер має {}$ \n".format(players3[l][1], players3[l][0], players3[l][4]))
                message += " \n"
        
        def lose(hunter, victim, H1, h1, h2, H3, V1, v1, v2, V3):
            life = random.randint(1,5)
            nonlocal message
            if life == 1:
                message += ("{} @{} промазав своїм пенісом і {} @{} зірвався та втік \n \n".format(H1, hunter, v1, victim))
            if life == 2:
                message += ("{} @{} вдалося уникнути пеніса {} @{} \n \n".format(V3, victim, h2, hunter))
            if life == 3:
                message += ("{} @{} не вдалося впіймати {} @{} \n \n".format(H3, hunter, v2, victim))
            if life == 4:
                message += ('{} @{} в останній момент використав "стан" і втік від {} @{} \n \n'.format(V1, victim, h2, hunter))
            if life == 5:
                message += ("{} @{} в останній момент насрав в штани і {} @{} вимушений був відступити \n \n".format(V1, victim, h1, hunter))
        def result():
            mm[players[p]]['kills'] += 1
            mm[players[i]]['lose'] += 1
        countPlayer2 = []
        for p in countPlayer:
            countPlayer2.append(p)
        Mer = []
        Police = []
        Gangster = []
        for l in countPlayer:
            if players3[l][1] == "Мер":
                Mer.append(l)
            if players3[l][1] == "Мєнт":
                Police.append(l)
            if players3[l][1] == "Разбойнік":
                Gangster.append(l)
        timer = 10 
        while 1:
            p = None
            i = None
            cho = [1,2,3]
            if not Mer:
                cho.remove(1)
            if not Police:
                cho.remove(2)
            if not Gangster:
                cho.remove(3)
            choice = random.choice(cho)
            choice2 = random.choice(cho)
                
            if choice == 1 :
                p = random.choice(Mer)
            if choice == 2 :
                p = random.choice(Police)
            if choice == 3 :
                p = random.choice(Gangster)
            if choice2 == 1 :
                i = random.choice(Mer)
            if choice2 == 2 :
                i = random.choice(Police)
            if choice2 == 3 :
                i = random.choice(Gangster)
            timer = timer - 1
            nonlocal avtoritet_changable
            if (choice != choice2 and (players3[p][3] == None or players3[p][3] == 0)) or timer == 0:
                timer = 20

                if players3[p][1] == "Мер":
                    if players3[i][1] == "Мєнт":
                        message += ("Мер @{} помітив мєнта @{} \n".format(players[p], players[i]))
                        die = random.randint(1,2)
                        if p in countPlayer2:
                            countPlayer2.remove(p)
                        players3[p][3] = 4
                        for c in range(len(players)):
                            if players3[c][3] != 0 and players3[c][3] != None:
                                players3[c][3] = players3[c][3] - 1
                        if die == 1:
                            rand = random.randint(1,avtoritet)
                            rand2 = random.randint(1,avtoritet_changable)
                            if rand <= rand2:
                                rabstvo.append(players3[i][0])
                                win(players[p], players[i], "Мер", "мер", "мера", "Мєнт", "Мєнта", "мєнта", False, True)
                                players3[i][2] = "Died"
                                countPlayer.remove(i)
                                Police.remove(i)
                                if i in countPlayer2:
                                    countPlayer2.remove(i)
                                result()
                            else:
                                message += ("Меру @{} не вистачило авторитета скористатися очком мєнта @{} \n \n".format(players[p], players[i]))
                        else:
                            lose(players[p], players[i], "Мер", "мер", "мера", "Меру", "Мєнт", "мєнт", "мєнта", "Мєнту")
                if players3[p][1] == "Мєнт":
                    if players3[i][1] == "Разбойнік":
                        message += ("Мєнт @{} помітив разбойніка @{} \n".format(players[p], players[i]))
                        die = random.randint(1,2)
                        if p in countPlayer2:
                            countPlayer2.remove(p)
                        players3[p][3] = 4
                        for c in range(len(players)):
                            if players3[c][3] != 0 and players3[c][3] != None:
                                players3[c][3] = players3[c][3] - 1
                        if die == 1:
                            if players3[i][4] != 0:
                                potential_money = [1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,5000,5000,5000,5000,5000,5000,5000,5000,
                                                   10000,10000,10000,10000,10000,10000,10000,15000,15000,15000,15000,15000,15000,20000,20000,20000,20000,20000, 
                                                   25000,25000,25000,25000, 30000,30000,30000, 40000, 40000, 50000, 75000]
                                rands = random.choice(potential_money)
                                if rands < players3[i][4]:
                                    players3[i][4] -= rands
                                    message += ("Разбойнік @{} виплатив взятку мєнту @{} в розмірі {}$ \n".format(players[i], players[p], rands))
                                    rands2 = random.randint(1,10)
                                    if rands2 == 1:
                                        message += ("Мєнт @{} наїбав разбойніка @{} і виїбав його в сраку \n \n".format(players[p], players[i]))
                                        players3[i][2] = "Died"
                                        countPlayer.remove(i)
                                        Gangster.remove(i)
                                        if len(Mer) != 0:
                                            avtoritet_changable -= 1
                                            message = message[:-3]
                                            message += ("Авторитет мера падає \n \n")
                                        if i in countPlayer2:
                                            countPlayer2.remove(i)
                                        result()
                                    else:
                                        message +=" \n"
                                else:
                                    message += ("Разбойніку @{} не вистачило коштів на взятку мєнту @{}, тому його спіткала анальна кара. Розмір взятки {}$ \n \n".format(players[i], players[p], rands))
                                    players3[i][2] = "Died"
                                    countPlayer.remove(i)
                                    Gangster.remove(i)
                                    if len(Mer) != 0:
                                        avtoritet_changable -= 1
                                        message = message[:-3]
                                        message += ("Авторитет мера падає \n \n")
                                    if i in countPlayer2:
                                        countPlayer2.remove(i)
                                    result()
                            else:
                                win(players[p], players[i], "Мєнт", "мєнт", "мєнта", "Разбойнік", "Разбойніка", "разбойніка", False, False)
                                if len(Mer) != 0:
                                    message = message[:-3]
                                    message += ("Авторитет мера падає \n \n")
                                    avtoritet_changable -= 1
                                players3[i][2] = "Died"
                                countPlayer.remove(i)
                                Gangster.remove(i)
                                if i in countPlayer2:
                                    countPlayer2.remove(i)
                                result()
                        else:
                            lose(players[p], players[i], "Мєнт", "мєнт", "мєнта", "Мєнту", "Разбойнік", "разбойнік", "разбойніка", "Разбойніку")
                if players3[p][1] == "Разбойнік":
                    if players3[i][1] == "Мер":
                        message += ("Разбойнік @{} помітив мера @{} \n".format(players[p], players[i]))
                        die = random.randint(1,2)
                        if p in countPlayer2:
                            countPlayer2.remove(p)
                        players3[p][3] = 4
                        for c in range(len(players)):
                            if players3[c][3] != 0 and players3[c][3] != None:
                                players3[c][3] = players3[c][3] - 1
                        if die == 1:
                            if len(rabstvo) != 0:
                                message += ("Мер @{} переодягнувся в мєнта і втік. Замість нього разбойнік @{} трахнув раба @{} \n \n".format(players[i],players[p],rabstvo[0]))
                                rabstvo.remove(rabstvo[0])
                            else:
                                players3[i][2] = "Died"
                                win(players[p], players[i], "Разбойнік", "разбойнік", "разбойніка", "Мер", "Мера", "мера", True, False)
                                countPlayer.remove(i)
                                Mer.remove(i)
                                if i in countPlayer2:
                                    countPlayer2.remove(i)
                                result()
                        else:
                            lose(players[p], players[i], "Разбойнік", "разбойнік", "разбойніка", "Разбойніку", "Мер", "мер", "мера", "Меру")
            if len(players) > 4:
                nonlocal lifeMer
                ## rand = random.randint(1,2)
                rand = 1
                for r in range(len(players)):
                    for c in range(3):
                        if players3[r][c] == "Мер" and players3[r][c+1] == "Died" and lifeMer == 1 and rand == 1:
                            players3[r][c+1] = None
                            message += ("Мер @{} платить за востановлєніє свого очка і повертається до гри \n \n".format(players[r]))
                            countPlayer.append(r)
                            lifeMer = 0
            if countPlayer2 == None or len(cho) == 1 or len(countPlayer2) == 2:
                break                           
    raund()
    while 1:
        if np.count_nonzero("Died" == players3['died']) >= (len(players) / 2) :
            for p in range(len(players)):
                if players3[p][2] != "Died":
                    mm[players[p]]['wins'] += 1
                    if players3[p][1] == "Разбойнік":
                        mm[players[p]]['money'] = mm[players[p]]['money'] + players3[p][4]
                    # for h in range(len(mm)):
                    #     if mm[h]['name'] == players[p]:
                    #         mm[h]['wins'] = mm[h]['wins'] + 1
                    #         if players3[p][1] == "Разбойнік":
                    #             mm[h]['money'] = mm[h]['money'] + players3[p][4]
                    #         break
            try:
                dat.update_one({'id': chadid},{ "$set": { 'members': mm } })
            except e:
                print(e)
            bot.send_message(chadid, message)
            message = ""
            for p in range(len(players)):
                if players3[p][2] != "Died":
                    if players3[p][1] == "Разбойнік" and players3[p][4] != 0:
                        message += ("{} @{} зберіг своє очко та {}$ \n".format(players3[p][1], players[p], players3[p][4]))
                    else:
                        message += ("{} @{} зберіг своє очко та виграв \n".format(players3[p][1], players[p]))
                        if players3[p][1] == "Мер" and len(rabstvo) != 0:
                            for j in rabstvo:
                                message += ("@{}, ".format(j))
                            message = message[:-4]
                            message += (" залишилися(залишився) в рабстві мера @{} \n".format(players[p]))
            bot.send_message(chadid, message)
            break
            return
        else:
            raund()


def top(chatid):
    mm = dat.find_one({'id': chatid})['members']
    top_wins = [{'name':'Ніхто', 'wins':0},{'name':'Ніхто', 'wins':0},{'name':'Ніхто', 'wins':0}]
    top_kills = [{'name':'Ніхто', 'kills':0},{'name':'Ніхто', 'kills':0},{'name':'Ніхто', 'kills':0}]
    top_lose = [{'name':'Ніхто', 'lose':0},{'name':'Ніхто', 'lose':0},{'name':'Ніхто', 'lose':0}]
    top_money = [{'name':'Ніхто', 'money':0},{'name':'Ніхто', 'money':0},{'name':'Ніхто', 'money':0}]
    list_keys = list(mm.keys())
    for i in list_keys:
        wins = True
        kills = True
        lose = True
        money = True
        for t in range(len(top_wins)):
            if wins:
                if top_wins[t]['name'] != 'Ніхто':
                    if top_wins[t]['wins'] < mm[i]['wins']:
                        if t == 0:
                            top_wins[t+2] = top_wins[t+1]
                            top_wins[t+1] = top_wins[t]
                            top_wins[t] = {'name': i,'wins': mm[i]['wins']}
                            wins = False
                        elif t == 1:
                            top_wins[t+1] = top_wins[t]
                            top_wins[t] = {'name': i,'wins': mm[i]['wins']}
                            wins = False
                        else:
                            top_wins[t] = {'name': i,'wins': mm[i]['wins']}
                            wins = False
                else:
                    top_wins[t] = {'name': i,'wins': mm[i]['wins']}
                    wins = False
            if kills:
                if top_kills[t]['name'] != 'Ніхто':
                    if top_kills[t]['kills'] < mm[i]['kills']:
                        if t == 0:
                            top_kills[t+2] = top_kills[t+1]
                            top_kills[t+1] = top_kills[t]
                            top_kills[t] = {'name': i,'kills': mm[i]['kills']}
                            kills = False
                        elif t == 1:
                            top_kills[t+1] = top_kills[t]
                            top_kills[t] = {'name': i,'kills': mm[i]['kills']}
                            kills = False
                        else:
                            top_kills[t] = {'name': i,'kills': mm[i]['kills']}
                            kills = False
                else:
                    top_kills[t] = {'name': i,'kills': mm[i]['kills']}
                    kills = False
            if lose:
                if top_lose[t]['name'] != 'Ніхто':
                    if top_lose[t]['lose'] < mm[i]['lose']:
                        if t == 0:
                            top_lose[t+2] = top_lose[t+1]
                            top_lose[t+1] = top_lose[t]
                            top_lose[t] = {'name': i,'lose': mm[i]['lose']}
                            lose = False
                        elif t == 1:
                            top_lose[t+1] = top_lose[t]
                            top_lose[t] = {'name': i,'lose': mm[i]['lose']}
                            lose = False
                        else:
                            top_lose[t] = {'name': i,'lose': mm[i]['lose']}
                            lose = False
                else:
                    top_lose[t] = {'name': i,'lose': mm[i]['lose']}
                    lose = False
            if money:
                if top_money[t]['name'] != 'Ніхто':
                    if top_money[t]['money'] < mm[i]['money']:
                        if t == 0:
                            top_money[t+2] = top_money[t+1]
                            top_money[t+1] = top_money[t]
                            top_money[t] = {'name': i,'money': mm[i]['money']}
                            money = False
                        elif t == 1:
                            top_money[t+1] = top_money[t]
                            top_money[t] = {'name': i,'money': mm[i]['money']}
                            money = False
                        else:
                            top_money[t] = {'name': i,'money': mm[i]['money']}
                            money = False
                else:
                    top_money[t] = {'name': i,'money': mm[i]['money']}
                    money = False
    
    return top_wins, top_kills, top_lose, top_money
            




## Sam bot

@bot.message_handler(content_types=['text'], chat_types = ['group','supergroup'])
def message_to(message):
    if dat.find_one({'id': message.chat.id}) == None:
        fields = {
            'id': message.chat.id,
            'status': 1,
            'g_status': 0,
            'mem_to_game': [],
            'members': {}
        }
        dat.insert_one(fields)
    else:
        if dat.find_one({'id': message.chat.id})['status'] == 1:
            if message.from_user.username == 'handsome_qitfi  s' or message.from_user.username == 'handsome_qitfis':
                print(message.from_user.username)
                shputya = ["Коля поїш гамна", "Я єбав тебе в рот, Коля", "Коля дебіл, шо за флешка?","Коля блять","продам тебе циганам","це декан так сказав?","Коля гавно своє їсть","в рот собі насри",
                            "ти обісраний", "Хай коля отсосе", "Коля, ти блатний як двері", "а уїбать", "Коля ти овощ", "Коля ти тупий", "Ти дебіл коля",
                            "Завали їбало", "Пашол нахуй Коля", "Ти підарастіческа хуйня їбана", "Ти кріпак засраний, іди сіно кидай", "ти загноение  підзалупного міра", "Шкода що такого божества в японській міфології не було, чи звідки там Колі беруться", "Ти став схожим не на Колю,  а на людину", "Коля слішком скіловий, я не можу", 
                            "Коля слабоумний", "Коля хуєблядска піздопройобіна"]
                shputyaSticker = ["CAACAgIAAxkBAAMLXk2JdD3e2ofsBDLlagIzUwaTHXoAAhkAA_z2jxuxgnHkHXK-oRgE", "CAACAgIAAxkBAAMMXk2KENg_--cBz-PQarldNjh5RZcAAh4AA_z2jxu3VCMC9M_xsRgE",
                                    "CAACAgIAAxkBAAMNXk2KSCpnTJ_KdG3R-5_D5krV1jgAAhYAA_z2jxsapXncRh_8JBgE", "CAACAgIAAxkBAAMOXk2KkQbgieGHmSSbC7yDZig5_eMAAhcAA_z2jxsfunL3I_azCBgE",
                                    "CAACAgIAAxkBAAMPXk2K2S4x7TQNMNlApek7wtEvzE8AAhoAA_z2jxs18TpPKoBrkRgE", "CAACAgIAAxkBAAMQXk2LMFh_VyOv2MWnYfM1iWvxHcIAAiAAA_z2jxsr0peTWHBxFhgE",
                                    "CAACAgIAAxkBAAMRXk2MEdLmfm8Y2AOrAgABtwoTVqaXAAJeAQACzcBIGJ_GOFgleipFGAQ", "CAACAgIAAxkBAAMSXk2MYj04L-zmPrWW3qYeD0QOtsMAAhwAA-b8Dxmrv56G5K6GqhgE",
                                    "CAACAgIAAxkBAAMTXk2MoukYFa1k5OyKHI0BhH4AAR8GAAIxAAPm_A8ZNUSF17VXQ_sYBA", "CAACAgIAAxkBAAMUXk2M0vFtF97w6kWrwjLkvcrPfj8AAjQAA-b8Dxl0Kmt-bE6nvxgE",
                                    "CAACAgIAAxkBAAMVXk2NAAE8WeT9tKg-AaACyvYhjRq_AAI4AAPm_A8Zo8L_zAxh4NIYBA", "CAACAgIAAxkBAAMWXk2NeiHTcue4AwrRBZ7nhpKu2lgAAvEAA_NWPxcqR0IBe-SHxhgE",
                                    "CAACAgIAAxkBAAMXXk2N3kpBhcD3sZWhiHQrrReJOpkAAiIAA3lx3hbdu_UH5ZkpgxgE"]
                rand1 = random.randint(0,1)
                if rand1 == 1:
                    bot.send_message(reply_to_message_id=message.id, chat_id=message.chat.id, text=random.choice(shputya))
                else:
                    bot.send_sticker(reply_to_message_id=message.id, chat_id=message.chat.id, sticker=random.choice(shputyaSticker))
                
            if message.text == '/off' or message.text == '/off@BogdanKarmanBot':
                dat.update_one({'id': message.chat.id},{ "$set": { 'status': 0 } })
                dat.update_one({'id': message.chat.id},{ "$set": { 'g_status': 0 } })
                dat.update_one({'id': message.chat.id},{ "$set": { 'mem_to_game': [] } })
                bot.send_message(chat_id=message.chat.id, text='Ну і йдіть нахуй, я пішов срать')
            if dat.find_one({'id': message.chat.id})['g_status'] == 0:
                if message.text == '/game' or message.text == '/game@BogdanKarmanBot':
                    dat.update_one({'id': message.chat.id},{ "$set": { 'g_status': 1 } })
                    bot.send_message(chat_id=message.chat.id, text='Почалася гра "Мер, Мєнти та Разбойніки".\n\nПравила гри:\nМЕР(Мер може бути тільки один) повинен трахнути МЄНТІВ, МЄНТИ повинні трахнути РОЗБІЙНИКІВ, РОЗБІЙНИКИ повинні трахнути МЕРА. Кожен повинен зберегти своє очко. Хто зберіг своє очко - той виграв. Якщо кількість гравців буде більше 5, то мер отримує шанс 1 раз воскреснути. Все відбувається рандомно. Ви можете тіки подивитись результати.\n\nГра автоматично почнеться або буде припинена через 40 хвилин!!!\n\nЩоб прийняти участь в грі відправте: {} .\n\nЩоб почати гру(коли наберуться учасники) відправте: /start\n\nЩоб закінчити гру: /stop\n\n/list - подивиться список учасників\n\n/statistic - подивиться статискику\n\n/top3 - подивиться топ3.'.format('"Плюс"'))
                    time = threading.Timer(2400.0, mytimer, [message.chat.id])
                    time.start()
                    timechat[message.chat.id] = time
                    print(timechat)
            else:
                messages = ['+', 'go','Go', 'го', 'Го', 'plus', 'Plus', 'плюс', 'Плюс']
                mes_min = ["Шо самий умний?", "В жопу свій мінус засунь", "ти довбойоб?", "мінуси тільки підари ставлять", "ще раз мінус поставиш - я приїду і виїбу тебе в очко"]
                minus = ['-', 'мінус', 'Мінус', 'Минус', 'минус', 'minus', 'Minus']
                if message.text in minus:
                    bot.send_message(reply_to_message_id=message.id, chat_id=message.chat.id, text=random.choice(mes_min))
                if message.text in messages:
                    mem = dat.find_one({'id': message.chat.id})['mem_to_game']
                    if message.from_user.username not in mem:
                        mem.append(message.from_user.username)
                        dat.update_one({'id': message.chat.id},{ "$set": { 'mem_to_game': mem } })
                        bot.send_message(chat_id=message.chat.id, text='@{} бере участь в грі'.format(message.from_user.username))
                    else:
                        bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.id, text='Ти вже приймаєш участь в грі')
                if message.text == '/stop'or message.text == '/stop@BogdanKarmanBot':
                    dat.update_one({'id': message.chat.id},{ "$set": { 'mem_to_game': [] } })
                    dat.update_one({'id': message.chat.id},{ "$set": { 'g_status': 0 } })
                    try:
                        timechat[message.chat.id].cancel()
                        timechat.pop(message.chat.id)
                    except:
                        pass
                    bot.send_message(chat_id=message.chat.id, text='Гру відмінено')
                if message.text == '/list'or message.text == '/list@BogdanKarmanBot':
                    mem = dat.find_one({'id': message.chat.id})['mem_to_game']
                    if len(mem)==0:
                        bot.send_message(chat_id=message.chat.id, text='Немає гравців')
                    else:
                        string = "Список гравців:\n"
                        for m in mem:
                            string = string + '@' + m + '\n'
                        bot.send_message(chat_id=message.chat.id, text=string)
                if message.text == '/start'or message.text == '/start@BogdanKarmanBot':
                    if len(dat.find_one({'id': message.chat.id})['mem_to_game']) > 1:
                        game(message.chat.id, dat.find_one({'id': message.chat.id})['mem_to_game'])
                        dat.update_one({'id': message.chat.id},{ "$set": { 'mem_to_game': [] } })
                        dat.update_one({'id': message.chat.id},{ "$set": { 'g_status': 0 } })
                        try:
                            timechat[message.chat.id].cancel()
                            timechat.pop(message.chat.id)
                        except:
                            pass
                    else:
                        bot.send_message(chat_id=message.chat.id, text='Мало гравців(Мінімум 2)')
            if message.text == '/top3' or message.text == '/top3@BogdanKarmanBot': ## top3
                top_w, top_k, top_l, top_m =top(message.chat.id)
                bot.send_message(chat_id=message.chat.id,text='Топ 3 побідітєлєй:\n1. @{} виграв {} раз(a).\n2. @{} виграв {} раз(a).\n3. @{} виграв {} раз(a).'.format(top_w[0]['name'], top_w[0]['wins'] , top_w[1]['name'], top_w[1]['wins'],top_w[2]['name'], top_w[2]['wins']))
                bot.send_message(chat_id=message.chat.id,text='Топ 3 анальних винищувачів:\n1. @{} знищив {} анусів.\n2. @{} знищив {} анусів.\n3. @{} знищив {} анусів.'.format(top_k[0]['name'], top_k[0]['kills'] , top_k[1]['name'], top_k[1]['kills'],top_k[2]['name'], top_k[2]['kills']))
                bot.send_message(chat_id=message.chat.id,text='Три самі пасивні гея:\n1. @{} втратив анальну дєвствєнность {} раз(a).\n2. @{} втратив анальну дєвствєнность {} раз(a).\n3. @{} втратив анальну дєвствєнность {} раз(a).'.format(top_l[0]['name'], top_l[0]['lose'] , top_l[1]['name'], top_l[1]['lose'],top_l[2]['name'], top_l[2]['lose']))
                bot.send_message(chat_id=message.chat.id,text='Топ 3 магната:\n1. @{} - {}$ \n2. @{} - {}$ \n3. @{} - {}$ '.format(top_m[0]['name'], top_m[0]['money'] , top_m[1]['name'], top_m[1]['money'],top_m[2]['name'], top_m[2]['money']))

            if message.text == '/statistic' or message.text == '/statistic@BogdanKarmanBot':
                mm = dat.find_one({'id': message.chat.id})['members']
                if  mm.__contains__(message.from_user.username ):
                    bot.send_message(chat_id=message.chat.id, text='Статистика @{}:\nВиграв ігор - {} \nКількість знищених ворожих анусів - {} \nКількість разів коли втратив анальну дєвствєнность - {} \nЗагальна кількість виграних грошей - {}$'.format(message.from_user.username, mm[message.from_user.username]['wins'],mm[message.from_user.username]['kills'], mm[message.from_user.username]['lose'], mm[message.from_user.username]['money']))
                else:
                    bot.send_message(reply_to_message_id=message.id, chat_id=message.chat.id, text='В тебе немає статистики')
        else:
            if message.text == '/on' or message.text == '/on@BogdanKarmanBot':
                dat.update_one({'id': message.chat.id},{ "$set": { 'status': 1 } })
                bot.send_message(chat_id=message.chat.id, text='Ну шо, я зробив свою справу')


# @bot.message_handler(commands=['on'], chat_types = ['group','supergroup'])
# def command_on(message):
#     print(message)
#     if dat.find_one({'id': message.chat.id}) == None:
#         fields = {
#             'id': message.chat.id,
#             'status': 1,
#             'members': []
#         }
#         dat.insert_one(fields)
#         print('yes')
#     else:
#         if dat.find_one({'id': message.chat.id})['status'] == 0:
#             dat.update_one({'id': message.chat.id},{ "$set": { 'status': 1 } })
#             bot.send_message(chat_id=message.chat.id, text='Ну шо, я зробив свою справу')

# @bot.message_handler(commands=['off'], chat_types = ['group','supergroup'])
# def command_off(message):
#     print(dat.find_one({'id': message.chat.id}))
#     if dat.find_one({'id': message.chat.id}) == None:
#         fields = {
#             'id': message.chat.id,
#             'status': 1,
#             'members': []
#         }
#         dat.insert_one(fields)
#     else:
#         if dat.find_one({'id': message.chat.id})['status'] == 1:
#             dat.update_one({'id': message.chat.id},{ "$set": { 'status': 0 } })
#             bot.send_message(chat_id=message.chat.id, text='Ну і йдіть нахуй, я пішов срать') 



bot.polling(none_stop=True, interval=0)