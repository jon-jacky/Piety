"""
line.py - Edit line of text on video display with cursor addressing.
                  Does not work on printing terminals.
"""

import string

# For vt100-style terminal controlled by ansi escape sequences.
# Replace these imports to use a different keyboard and display.
import ansi_display as display
import vt_keyboard as keyboard

# Command functions all require a display terminal with cursor addressing.

# Each function takes an argument, l (for 'line'), an object,
#  which must have attributes point (int), chars  and prompt (strings)
# For example an instance of console.Console has these attributes.
# Prompt attribute is only used to define the left margin,
#  only move_beginning_of_line and move_end_of_line use it.
#  (couldn't we have prompt default to '' if there is no such attribute?)

def self_insert_command(l, key):
    l.chars = (l.chars[:l.point] + key + l.chars[l.point:])
    l.point += 1
    display.self_insert_char(key)

def backward_delete_char(l):
    if l.point > 0:
        l.chars = (l.chars[:l.point-1] + l.chars[l.point:])
        l.point -= 1
        display.backward_delete_char()

def move_beginning_of_line(l):
    l.point = 0
    start = len(l.prompt)+1 # allow for space after prompt
    display.move_to_column(start) # move to character after prompt

def backward_char(l):
    if l.point > 0:
        l.point -= 1
        display.backward_char()

def delete_char(l):
    l.chars = (l.chars[:l.point] + l.chars[l.point+1:])
    display.delete_char()

def move_end_of_line(l):
    l.point = len(l.chars)
    eol = len(l.prompt) + 1 + len(l.chars)
    display.move_to_column(eol)

def forward_char(l):
    if l.point < len(l.chars):
        l.point += 1
        display.forward_char()

def kill_line(l):
     l.chars = l.chars[:l.point] # point doesn't change
     display.kill_line()


keymap =  {
    # command functions here all take just one argument, the l object.
    keyboard.bs: backward_delete_char,
    keyboard.delete: backward_delete_char,
    keyboard.C_a: move_beginning_of_line,
    keyboard.C_b: backward_char,
    keyboard.left: backward_char,
    keyboard.C_d: delete_char,
    keyboard.C_e: move_end_of_line,
    keyboard.C_f: forward_char,
    keyboard.right: forward_char,
    keyboard.C_k: kill_line,
    # command function here takes two arguments: the l object, and key
    string.printable: self_insert_command
    }
