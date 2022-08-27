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
        for key, value in self.preferences.items():
            yield ExtensionResult(
                name=f'{key}: {value}',
                description=f'input: {input_text}',
                on_enter=HideWindowAction()
            )

if __name__ == '__main__':
    MainExtension().run()
