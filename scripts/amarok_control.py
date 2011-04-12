#!/usr/bin/env python2

#  
#  Copyright (C) 2011 Joseph Henrich
# 
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import atexit
import gobject
import dbus
import dbus.glib
import glib
import os
import math

try:
  import gtk
  from dockmanager.dockmanager import DockManagerItem, DockManagerSink, DOCKITEM_IFACE
  from dockmanager.dockmanager import RESOURCESDIR
  from signal import signal, SIGTERM
  from sys import exit
except ImportError, e:
  print e
  exit()

amarokbus = "org.kde.amarok"
playerpath = "/Player"

class AmarokItem(DockManagerItem):
  def __init__(self, sink, path):
    DockManagerItem.__init__(self, sink, path)

    
    self.player = dbus.SessionBus().get_object(amarokbus, playerpath)
    self.add_menu_item("Play/Pause", "media-playback-start", "Controls")
    self.add_menu_item("Previous", "media-skip-backward", "Controls")
    self.add_menu_item("Next", "media-skip-forward", "Controls")

  def menu_pressed(self, menu_id):
    if not self.player:
      return False

    if self.id_map[menu_id] == "Play/Pause":
      self.player.PlayPause()
    elif self.id_map[menu_id] == "Next": 
      self.player.Next()
    elif self.id_map[menu_id] == "Previous": 
      self.player.Prev()

class AmarokSink(DockManagerSink):
  def item_path_found(self, pathtoitem, item):
    if item.Get(DOCKITEM_IFACE, "DesktopFile", dbus_interface="org.freedesktop.DBus.Properties").endswith("amarok.desktop"):
      self.items[pathtoitem] = AmarokItem(self, pathtoitem)

dockysink = AmarokSink()

def cleanup():
  dockysink.dispose()

if __name__ == "__main__":
  mainloop = gobject.MainLoop(is_running=True)

  atexit.register (cleanup)
  signal(SIGTERM, lambda signum, stack_frame: exit(1))

  mainloop.run()
