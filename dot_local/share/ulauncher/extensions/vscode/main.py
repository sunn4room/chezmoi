import os
import glob
import json
import datetime
from ulauncher.api import AdvancedExtension, ExtensionResult
from ulauncher.api.shared.action.ActionList import ActionList
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenAction import OpenAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction

class MainExtension(AdvancedExtension):

    def on_input(self, input_text, trigger_id):
        abs_path = os.path.expanduser('~/.config/Code')
        file_list = glob.glob(abs_path +
                              "/User/workspaceStorage/*/workspace.json")

        recent_workspaces = []
        for workspace_file in file_list:
            f = open(workspace_file, 'r')
            data = json.load(f)

            f.close()

            if 'folder' not in data:
                continue

            pointer = data['folder'].find('file://')
            if (pointer >= 0):
                path = data['folder'][7:]
                # get workspace name
                namePointer = path.rfind('/')
                name = path[namePointer + 1:]
                currentData = {'name': name, 'path': path}

                # make sure to include only folders that still exist
                if os.path.isdir(path) and path != "/tmp":
                    currentData['mtime'] = datetime.datetime.fromtimestamp(
                        os.stat(path).st_mtime)
                    recent_workspaces.append(currentData)

        for workspace_file in file_list:
            with open(workspace_file, 'r') as f:
                data = json.load(f)

            if 'folder' not in data:
                continue

            pointer = data['folder'].find('file://')
            if (pointer >= 0):
                path = data['folder'][7:]
                namePointer = path.rfind('/')
                name = path[namePointer + 1:]

                if input_text in name and os.path.isdir(path) and path != "/tmp":
                    mtime = datetime.datetime.fromtimestamp(
                        os.stat(path).st_mtime)
                    yield ExtensionResult(
                        name=name,
                        description=f'[{mtime}] {path}',
                        on_enter=RunScriptAction(f'code "{path}"')
                    )

if __name__ == '__main__':
    MainExtension().run()
