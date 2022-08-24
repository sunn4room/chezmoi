from ulauncher.api import Extension, ExtensionResult, StoppableThread
from ulauncher.utils.desktop.notification import show_notification
from ulauncher.api.shared.action.ActionList import ActionList
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenAction import OpenAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction

class MainExtension(Extension):

    def on_input(self, input_text, trigger_id):
        for key, value in self.preferences.items():
            yield ExtensionResult(
                name=f'{key}: {value}',
                description=f'input: {input_text}',
                on_enter=HideWindowAction()
            )

    def on_item_enter(self, data):
        pass

    def on_output(self, cmd, output):
        pass

    def on_preferences_update(self, id, value, previous_value):
        pass

if __name__ == '__main__':
    MainExtension().run()
