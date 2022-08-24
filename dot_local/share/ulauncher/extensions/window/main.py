import hashlib
import os
import time
import gi
from gi.repository import Gtk
from gi.repository import Wnck
from ulauncher.api import Extension, ExtensionResult, StoppableThread
from ulauncher.utils.desktop.notification import show_notification
from ulauncher.api.shared.action.ActionList import ActionList
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenAction import OpenAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction

gi.require_version('Gdk', '3.0')
gi.require_version("Gtk", "3.0")
gi.require_version("Wnck", "3.0")

class MainExtension(Extension):

    def __init__(self):
        super(MainExtension, self).__init__()
        self.screen = Wnck.Screen.get_default()

    def on_input(self, input_text, trigger_id):
        self.screen.force_update()
        while Gtk.events_pending():
            Gtk.main_iteration()
        for window in self.screen.get_windows():
            name = window.get_application().get_name()
            title = window.get_name()
            if input_text in name or input_text in title:
                yield ExtensionResult(
                    name=name,
                    description=title,
                    on_enter=ExtensionCustomAction(window.get_xid())
                )

    def on_item_enter(self, wid):
        for window in self.screen.get_windows():
            if window.get_xid() == wid:
                workspace = window.get_workspace()
                timestamp = int(time.time())
                if workspace:
                    workspace.activate(timestamp)
                window.activate(timestamp)

if __name__ == '__main__':
    MainExtension().run()
