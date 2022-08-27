import os
from ulauncher.api import AdvancedExtension, ExtensionResult
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction

class MainExtension(AdvancedExtension):

    def __init__(self):
        super(MainExtension, self).__init__()
        self.actions = ["poweroff", "reboot", "suspend", "hibernate", "logout", "lock"]

    def on_input(self, input_text, trigger_id):
        for action in self.actions:
            if input_text in action:
                yield ExtensionResult(
                    name=action,
                    description=self.preferences[action],
                    icon=f"images/{action}.png",
                    on_enter=RunScriptAction(self.preferences[action])
                )

if __name__ == '__main__':
    MainExtension().run()
