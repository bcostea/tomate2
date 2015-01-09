#!/usr/bin/env python2
from __future__ import division
import os
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GObject as gobject
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Notify
from gi.repository import AppIndicator3 as appindicator
from time import time
from math import floor

Gdk.threads_init()

class TomateConfig(object):
  #Parameters
  MIN_WORK_TIME = 60 * 10   # min work time in seconds
  DONE_WORK_TIME = 60 * 25  # finished work time in seconds
  POLL_INTERVAL = 5         # polling interval in seconds

class States(object):
  IDLE = 1
  WORKING = 2
  OK = 3
  DONE = 4

STATE_MESSAGES = {
    States.IDLE : 'Idle',
    States.WORKING : 'Working',
    States.OK : 'Ok',
    States.DONE : 'Done'
    }

STATE_ICONS = {
    States.IDLE : 'idle',
    States.WORKING : 'working',
    States.OK : 'ok',
    States.DONE : 'done'
    }


class Pomodoro:
  def __init__(self):
    # we start with an idle state
    self.state = States.IDLE
    self.tick_interval = TomateConfig.POLL_INTERVAL
    self.start_working_time = 0

  def init_ui(self):
    Notify.init("Tomate")
    self.ind = self.build_indicator()
    menu = self.build_menu()
    self.ind.set_menu(menu)

  def build_indicator(self):
    ind = appindicator.Indicator.new(
      "Tomate",
      self.get_icon(self.state),
      appindicator.IndicatorCategory.APPLICATION_STATUS)
    ind.set_status(appindicator.IndicatorStatus.ACTIVE)
    return ind

  def build_menu(self):
    menu = Gtk.Menu()
    self.st_menu = Gtk.MenuItem("Start")
    self.st_menu.connect('activate',self.icon_click)
    menu.append(self.st_menu)
    mi = Gtk.ImageMenuItem("Quit")
    img = Gtk.Image.new_from_stock(Gtk.STOCK_QUIT, Gtk.IconSize.MENU)
    mi.set_image(img)
    mi.connect('activate',Gtk.main_quit)
    menu.append(mi)
    menu.show_all()
    return menu

  def get_icon(self, state):
    return self.icon_directory() + "/img/" + STATE_ICONS[state] + ".png"

  def format_time(self,seconds):
    if seconds < 60:
      return "%d seconds" % seconds
    minutes = floor(seconds / 60)
    if minutes > 1:
      return "%d minutes" % minutes
    else:
      return "%d minute" % minutes

  def set_state(self, state, time):
    old_state=self.state

    if self.state == state:
      return

    if state == States.IDLE:
      delta = time - self.start_working_time
      if old_state == States.OK:
        self.tooltip = "Good, you worked for " + self.format_time(delta) + "!"
      elif old_state == States.WORKING:
        self.tooltip = "Not good: worked for only "  + self.format_time(delta)
      elif old_state == States.DONE:
        self.tooltip = "Good, you worked for " + self.format_time(delta) + "! \
          Time for a break!"
    elif state == States.WORKING:
      self.start_working_time = time
      delta = time - self.start_working_time
      self.tooltip = "Working for " + self.format_time(delta) + "..."
    elif state == States.OK:
      delta = time - self.start_working_time
      self.tooltip = "Good, you worked for " + self.format_time(delta) + "!"
    elif state == States.DONE:
      self.tooltip = "Worked enough, take a break!"

    self.state=state
    self.ind.set_icon(self.get_icon(state))
    self.show_notification(self.state, self.tooltip)

  def show_notification(self, state, notification):
    try:
      nw = Notify.Notification.new("Tomate state changed to " +
        STATE_MESSAGES[state],
        notification, self.get_icon(state))
      nw.show()
    except:
      pass

  def icon_directory(self):
    return os.path.dirname(os.path.realpath(__file__)) + os.path.sep

  def icon_click(self, dummy):
    if self.state == States.IDLE:
      self.set_state(States.WORKING, time())
    else:
      self.set_state(States.IDLE, time())

  def update(self, time):
    """This method is called everytime a tick interval occurs"""
    delta = time - self.start_working_time
    if self.state == States.IDLE:
      pass
    else:
      self.st_menu.set_label("Working for %s... stop" % self.format_time(delta))
      if self.state == States.WORKING:
        if delta > TomateConfig.MIN_WORK_TIME:
            self.set_state(States.OK, time)
      elif self.state == States.OK:
        if delta > TomateConfig.DONE_WORK_TIME:
          self.set_state(States.DONE, time)

  def tick(self):
    self.update(time())
    source_id = gobject.timeout_add(self.tick_interval*1000, self.tick)

  def main(self):
    # All PyGTK applications must have a gtk.main(). Control ends here
    # and waits for an event to occur (like a key press or mouse event).
    source_id = gobject.timeout_add(self.tick_interval, self.tick)
    self.init_ui()
    Gtk.main()

# If the program is run directly or passed as an argument to the python
# interpreter then create a Pomodoro instance and show it
if __name__ == "__main__":
  app = Pomodoro()
  app.main()
