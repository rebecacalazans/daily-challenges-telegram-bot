#!/usr/bin/env bash

sqlite3 bot.db "create table challenges (id integer primary key, name text, description text)"
sqlite3 bot.db "create table members (id integer primary key, challenge_id integer, member_id integer, member_username text, qnt integer, day integer)"
