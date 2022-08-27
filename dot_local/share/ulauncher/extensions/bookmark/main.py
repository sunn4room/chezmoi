import os
import json
from ulauncher.api import AdvancedExtension, ExtensionResult
from ulauncher.api.shared.action.ActionList import ActionList
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenAction import OpenAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction

class Bookmark():
    def __init__(self, name: str, url: str):
        self.name: str = name
        self.url: str = url

class MainExtension(AdvancedExtension):

    def __init__(self):
        super(MainExtension, self).__init__()
        self.timestamp: int = 0
        self.bookmarks: list[Bookmark] = []

    def find_bookmark(self, data):
        if data['type'] == 'folder':
            for child in data['children']:
                self.find_bookmark(child)
        else:
            self.bookmarks.append(Bookmark(data['name'], data['url']))

    def need_load(self, sth):
        bookmark_path = os.path.expanduser(self.preferences['bookmark_path'])
        if not os.path.isfile(bookmark_path):
            return True
        timestamp = os.stat(bookmark_path).st_mtime_ns
        return timestamp != self.timestamp

    def do_load(self, sth):
        try:
            bookmark_path = os.path.expanduser(self.preferences['bookmark_path'])
            self.bookmarks = []
            with open(bookmark_path, 'r') as data_file:
                data = json.load(data_file)
                self.find_bookmark(data['roots']['bookmark_bar'])
            self.timestamp = os.stat(bookmark_path).st_mtime_ns
            self.info('update %s bookmarks', len(self.bookmarks))
            self.notify('Bookmarks changed', f'update {len(self.bookmarks)} bookmarks')
        except:
            return False
        else:
            return True

    @AdvancedExtension.load('bookmarks')
    def on_input(self, input_text: str, trigger_id):
        input_text = input_text.lower()
        counter = 0
        for bookmark in self.bookmarks:
            if input_text in bookmark.name.lower() or input_text in bookmark.url.lower():
                yield ExtensionResult(
                    name=bookmark.name,
                    description=bookmark.url,
                    on_enter=OpenUrlAction(bookmark.url)
                )
                counter += 1
                if counter == 10:
                    break

if __name__ == '__main__':
    MainExtension().run()
