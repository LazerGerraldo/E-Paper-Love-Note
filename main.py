#!/usr/bin/env python3
#Main driver handles mode of operation morning and evening routines, displaying a randomly 
# picked message from MessagesTo.txt file, and overrideing other options with a email 
# triggered message to be displayed for a given amount ot time. Zachary revision of main.py

from enum import Enum
import datetime as dt
import time
import random
import emailPull
import os
import textHandler
import logging
from logging.handlers import RotatingFileHandler

notedir =  '/home/pi/MessagesTo.txt' #finding MessagesTo.txt file location
mornnotedir = '/home/pi/MorningMessagesTo.txt' #morning message directory
evenotedir = '/home/pi/EveningMessagesTo.txt'  #evening message directory
log_formatter = logging.Formatter('%(asctime)s %(message)s')
my_handler = RotatingFileHandler('/home/pi/E-Paper-Love-Note/log/lovenote.trace',
                                 mode='a+', maxBytes=5*1024*1024, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)

app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)
app_log.addHandler(my_handler)


MAX_DISPLAY_CYCLES = 60           # 60 cycles, 1 hour. Determines time message is displayed
CLOCK_CYCLE_SECONDS = 60          # 60 seconds, 1 minute. Constant refresh cycle to check time of day
MAX_OVERRIDE_CYCLES = 180         # 180 minutes for screen display override from email

# various modes of operation
class Mode(Enum):
   MORNING = 1
   DISPLAY_FROM_FILE = 2
   EVENING = 3
   EMAIL_OVERRIDE = 4
   NONE = 5

class DisplayState:
   def __init__(self):
      self.override_cycle = 0
      self.override_message = '' # message to be overridden to screen
      self.mode = None
      self.current_cycle = 0

   def update_current_mode(self):
      hour = dt.datetime.now().hour

      if self.mode == Mode.EMAIL_OVERRIDE:
          return

      if hour < 9:
         if not self.mode == Mode.MORNING:
            self.mode = Mode.MORNING
            textHandler.display_on_screen('Good morning! Have such a wonderful day!')
            app_log.info("Mode set to morning, displaying morning message")
      elif hour < 22:
         if not self.mode == Mode.DISPLAY_FROM_FILE:
            self.mode = Mode.DISPLAY_FROM_FILE
            self.current_cycle = 0
            app_log.info("Mode set to display from file, displaying random message")
      else:
         if not self.mode == Mode.EVENING:
            self.mode = Mode.EVENING
            textHandler.display_on_screen('Good night! Have a wonderful sleep!')
            app_log.info("Mode set to evening, displaying evening message")

   def set_email_override_mode(self, message):
      self.mode = Mode.EMAIL_OVERRIDE
      self.override_message = message
      self.override_cycle = 0

   def in_mode(self, mode):
      return self.mode == mode

   def override_cycle_done(self):
      if self.override_cycle == MAX_OVERRIDE_CYCLES:
         self.override_message = ''
         self.mode = Mode.NONE
         self.override_cycle = 0
         return True

      elif self.override_cycle == 0:
         app_log.info("Displaying override message to screen: %s" % self.override_message)
         textHandler.display_on_screen(self.override_message) #display overridden message to screen

      self.override_cycle += 1
      return False

   def display_from_file_cycle(self):

      if self.current_cycle % MAX_DISPLAY_CYCLES == 0:
         self.current_cycle = 1
         return True

      self.current_cycle += 1
      return False

# updates the stored MessagesTo.txt file using email data.
def handle_email(state, f, subject, content):
   if subject.lower() == 'add':
      f.write(content)
      f.write('\n')
      app_log.info('Adding new message to file: %s' % content)
   elif subject.lower() == 'push':
      state.set_email_override_mode(content)
      app_log.info("setting override message: %s" % state.override_message)
   elif subject.lower() == 'clear':
      state.set_email_override_mode('') #sends blank message to email override
      app_log.info("clearing display, nothing should be on the screen for the override time duration")
   elif subject.lower() == 'all':
      f.write(content)
      f.write('\n')
      state.set_email_override_mode(content)
   else:
      app_log.info('Not a valid Email Subject')

def check_new_emails(state):
   with open(notedir, 'a') as f:
      try:
         emails = emailPull.ReadEmail()
         for y in emails:
            handle_email(state, f, y[0], y[1]) #tuple of email handle_email(file, subject, content)
      except:
         app_log.info('Exception: error in reading new emails')

def display_random_message():
   with open(notedir, 'r') as f:
      lines = []
      for line in f:
         lines += [line]

      message = random.choice(lines)
      textHandler.display_on_screen(message)
      app_log.info('Random message: %s' % message)

#displays random message from given note directory MorningMessagesTo.txt or EveningMessagesTo.txt
def display_morn_eve_message(notedirs):
   with open(notedirs, 'r') as f:
      lines = []
      for line in f:
         lines += [line]

      message = random.choice(lines)
      textHandler.display_on_screen(message)
      app_log.info('Random morning or evening message: %s' % message)

def main():
   textHandler.initscreen() # clears and initializes screen
   state = DisplayState()

   app_log.info('Booting app up! *****************************************')

   while True:
      state.update_current_mode()
      check_new_emails(state)

      if state.in_mode(Mode.EMAIL_OVERRIDE):
         if state.override_cycle_done():
            continue

      elif state.in_mode(Mode.DISPLAY_FROM_FILE):
         new_display_cycle = state.display_from_file_cycle()
         if new_display_cycle:
            display_random_message()

      time.sleep(CLOCK_CYCLE_SECONDS)

main()
