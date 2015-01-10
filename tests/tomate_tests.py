#!/usr/bin/env python2
import sys
import os
import unittest
sys.path.append(os.path.abspath(sys.path[0]) + "/../")
from tomate2 import Pomodoro
from tomate2 import States
from tomate2 import TomateConfig

class PomodoroTests(unittest.TestCase):
  def setUp(self):
    self.tomate = Pomodoro() 
    self.tomate.init_ui()
    pass

  def test_format_time_seconds(self):
    self.assertEqual(self.tomate.format_time(5), "5 seconds")

  def test_format_time_minute(self):
    self.assertEqual(self.tomate.format_time(60), "1 minute")

  def test_format_time_hour_minute(self):
    self.assertEqual(self.tomate.format_time( 60 * 60 + 60), "1 hour and 1 minute")

  def test_format_time_hour_minutes(self):
    self.assertEqual(self.tomate.format_time( 60 * 60 +120), "1 hour and 2 minutes")

  def test_format_time_hours_minute(self):
    self.assertEqual(self.tomate.format_time( 2 * 60 * 60 + 60), "2 hours and 1 minute")

  def test_format_time_day_hour_minute(self):
    self.assertEqual(self.tomate.format_time( 25 * 60 * 60 + 60), "1 day 1 hour and 1 minute")

  def test_format_time_days_minute(self):
    self.assertEqual(self.tomate.format_time( 2 * 24 * 60 * 60 + 60), "2 days and 1 minute")

  def test_format_time_days_hours_minutes(self):
    self.assertEqual(self.tomate.format_time( (3 * 24 * 60 * 60 )+ (5 * 60 * 60
      )+ 120), "3 days 5 hours and 2 minutes")

  def test_format_time_minutes(self):
    self.assertEqual(self.tomate.format_time(182), "3 minutes")

  def test_set_state_working_to_ok_on_tick(self):
    self.tomate.set_state(States.WORKING, 0)
    self.tomate.update(TomateConfig.MIN_WORK_TIME + 1)
    self.assertEqual(self.tomate.state, States.OK)

  def test_set_state_working_remains_the_same_on_tick(self):
    self.tomate.set_state(States.WORKING, 0)
    self.tomate.update(TomateConfig.MIN_WORK_TIME / 2)
    self.assertEqual(self.tomate.state, States.WORKING)

  def test_set_state_ok_to_idle_on_selection(self):
    self.tomate.set_state(States.OK, TomateConfig.MIN_WORK_TIME + 1)
    self.tomate.set_state(States.IDLE, 0)
    self.assertEqual(self.tomate.state, States.IDLE)

  def test_set_State_ok_to_done_on_tick(self):
    self.tomate.set_state(States.OK, TomateConfig.MIN_WORK_TIME + 1)
    self.tomate.update(TomateConfig.DONE_WORK_TIME + 1)
    self.assertEqual(self.tomate.state, States.DONE)

  def test_set_state_done_to_idle_on_selection(self):
    self.tomate.set_state(States.DONE, TomateConfig.DONE_WORK_TIME + 1)
    self.tomate.set_state(States.IDLE, 0)
    self.assertEqual(self.tomate.state, States.IDLE)

  def test_set_state_working_to_idle_on_selection(self):
    self.tomate.set_state(States.WORKING, 60)
    self.tomate.set_state(States.IDLE, 0)
    self.assertEqual(self.tomate.state, States.IDLE)

  def test_set_state_idle_remains_idle_on_tick(self):
    self.tomate.set_state(States.IDLE, 0)
    self.tomate.update(TomateConfig.DONE_WORK_TIME)
    self.assertEqual(self.tomate.state, States.IDLE)

if __name__ == '__main__':
  unittest.main()
