#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import dataset
from functools import wraps
from telegram import *
from telegram.ext import *

import locale

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
db = dataset.connect("sqlite:///" + os.path.dirname(os.path.realpath(__file__)) + "/bot.db"); 

token = os.environ['TOKEN']

updater = Updater(token=token)
dispatcher = updater.dispatcher


def add_member(challenge_id, member_id, member_username):
    members = db["members"];
    member = members.find(challenge_id = challenge_id, member_id = member_id);
    member = list(member);
    if len(member) == 0:
        members.insert(dict(challenge_id = challenge_id, member_id = member_id, member_username = member_username, qnt = 0, day = 0));

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Eu sou um bot, mas você pode me entender como uma convolução cíclica multivariável");

def create_challenge(name, description):
    challenges = db["challenges"];
    challenges.insert(dict(name = name, description = description));

def list_challenges(bot, update):
    challenges = db["challenges"];
    challenges = list(challenges.all())
    custom_keyboard = [];
    text = "";

    if(len(challenges) == 0):
        bot.send_message(
            chat_id = update.message.chat_id,
            text="Não existe nenhum desafio =[");

    else:
        text="Mostrando " + str(len(challenges)) + " desafios disponíveis:";
        for row in challenges:
            custom_keyboard.append([InlineKeyboardButton(row["name"], callback_data="select_challenge " + str(row["id"]))])
        reply_markup = InlineKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=update.message.chat_id,
                         parse_mode = ParseMode.MARKDOWN,
                         text=text,
                         reply_markup=reply_markup)
    #custom_keyboard.append([InlineKeyboardButton("Criar desafio...", callback_data="append_challenge")]);

def delete_challenge(id):
    db["challenges"].delete(id = id);

#challenge_options
def query_result(bot, update):
    query = update.callback_query

    data = query.data.split();


    if data[0] == "append_challenge":
        create_challenge(bot, update);

    elif data[0] == "select_challenge":
        select_challenge(bot, update, int(data[1]));

    elif data[0] == "challenge":
        challenge_options(bot, update);
    elif query.data == '1':
        edit_message(bot, update)
    else:
        bot.edit_message_text(chat_id=query.message.chat_id,
                          parse_mode = ParseMode.MARKDOWN,
                          message_id=query.message.message_id,
                          text=query.data)

def get_challenge_data(cid):
    challenge = db["challenges"].find_one(id = cid);

    members = db["members"].find(challenge_id = cid);
    text = "*" + challenge["name"] + "*\n";
    text += challenge["description"] + '\n\n\n';

    text += '`Participante' + 6*' ' + "Dias  Contagem" + '\n\n';
    for row in members:
        username = row["member_username"];
        day = str(row["day"]);
        cnt = str(row["qnt"]);
        tot = str(row["tot"]);

        text += username + "  " + (16-len(username))*' ' + (3-len(day))*' '  + day + (10-len(cnt))*' ' + cnt + '\n';
        text += "  └Total: " + (3 - len(tot))*' ' + tot + '\n\n';
    text += '`'

    return text;

def challenge_menu(bot, update, cid):
    query = update.callback_query

    text = get_challenge_data(cid);

#   button_add = InlineKeyboardButton("Adicionar", callback_data = 'challenge ' + str(cid) + " inc");
    button1 = InlineKeyboardButton("+1", callback_data ='challenge ' + str(cid) + " add 1")
    button5 = InlineKeyboardButton("+5", callback_data ='challenge ' + str(cid) + " add 5")
    button10 = InlineKeyboardButton("+10", callback_data ='challenge ' + str(cid) + " add 10")
    button_new_day = InlineKeyboardButton("Começar novo dia", callback_data ='challenge ' + str(cid) + " new_day")
    button_participate = InlineKeyboardButton("Participar", callback_data ='challenge ' + str(cid) + " participate")
    button_hide = InlineKeyboardButton("Esconder Menu", callback_data ='challenge ' + str(cid) + ' hide')

    custom_keyboard = [[button1, button5, button10], [button_new_day], [button_participate], [button_hide]];
    reply_markup = InlineKeyboardMarkup(custom_keyboard)
    bot.edit_message_text(chat_id=query.message.chat_id,
                          parse_mode = ParseMode.MARKDOWN,
                          message_id=query.message.message_id,
                          text=text, reply_markup=reply_markup)

def select_challenge(bot, update, cid):

    query = update.callback_query
    text = get_challenge_data(cid);

    menu = InlineKeyboardButton("Menu", callback_data ='challenge ' + str(cid) + " menu")
    custom_keyboard = [[menu]];
    reply_markup = InlineKeyboardMarkup(custom_keyboard)
    bot.edit_message_text(chat_id=query.message.chat_id,
                          parse_mode = ParseMode.MARKDOWN,
                          message_id=query.message.message_id,
                          text=text, reply_markup=reply_markup)

def challenge_options(bot, update):
    query = update.callback_query
    data = query.data.split();

    cid = int(data[1]);


    query = update.callback_query

    if data[2] == "menu":
        challenge_menu(bot, update, cid);
        return

    if data[2] == "hide":
        select_challenge(bot, update, cid);
        return
#        bot.edit_message_text(chat_id=query.message.chat_id,
#                              parse_mode = ParseMode.MARKDOWN,
#                              message_id=query.message.message_id,
#                              text=get_challenge_data(cid))

    members = db["members"];
    member = members.find(challenge_id = cid, member_id = query.from_user.id);
    member = list(member);
    text = ""

    if len(member) == 0:
        if data[2] == "participate" :
            add_member(cid, query.from_user.id, query.from_user.username);
#            bot.edit_message_text(chat_id=query.message.chat_id,
#                                  parse_mode = ParseMode.MARKDOWN,
#                              message_id=query.message.message_id,
#                              text=get_challenge_data(cid))
        else:
#            text = get_challenge_data(cid);
             text += "\n\n\nVocê ainda não está participando do desafio";
#            bot.edit_message_text(chat_id=query.message.chat_id,
#                                  parse_mode = ParseMode.MARKDOWN,
#                                  message_id=query.message.message_id,
#                                  text=text)
    elif data[2] == "participate":
        return
#        bot.edit_message_text(chat_id=query.message.chat_id,
#                              parse_mode = ParseMode.MARKDOWN,
#                              message_id=query.message.message_id,
#                              text=get_challenge_data(cid))
    else:
        member = member[0];

        if data[2] == "new_day":
            member['qnt'] = 0;
            member['day'] += 1;
        elif data[2] == "inc":
            increment(bot, update, cid);
        elif data[2] == "add":
            val = int(data[3]);
            member['qnt'] += val;
            member['tot'] += val;
        members.update(member, ['challenge_id', 'member_id']);

    #select_challenge(bot, update, cid);
    text = get_challenge_data(cid) + text;

    bot.edit_message_text(chat_id=query.message.chat_id,
                          parse_mode = ParseMode.MARKDOWN,
                          message_id=query.message.message_id,
                          text=text,
                          reply_markup=query.message.reply_markup)
    #bot.edit_message_text(chat_id=query.message.chat_id,
    #                      parse_mode = ParseMode.MARKDOWN,
    #                      message_id=query.message.message_id,
    #                      text=get_challenge_data(cid))

def main():
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('challenges', list_challenges))
    dispatcher.add_handler(CommandHandler('create_challenge', create_challenge, pass_args=True))
    dispatcher.add_handler(CommandHandler('delete_challenge', delete_challenge, pass_args=True))

    #dispatcher.add_handler(CommandHandler('challenge_members', challenge_members, pass_args=True))

    dispatcher.add_handler(CallbackQueryHandler(query_result))


    #list_members();
    #add_member(1, 1, "beca")
    #add_member(1, 2, "calazans")
    #add_member(1, 3, "dfa")

    #create_challenge("Desafio das 100 Flexões", "Fazer  100 flexões todos os dias por 30 dias");

    updater.start_polling()



if __name__ == "__main__":
    main()
