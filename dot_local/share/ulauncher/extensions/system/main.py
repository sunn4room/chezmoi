import os
from ulauncher.api import Extension, ExtensionResult
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

class MainExtension(Extension):

    def __init__(self):
        super(MainExtension, self).__init__()
        self.make_candidates()

    def make_candidates(self):
        self.candidates: list[ExtensionResult] = []
        for action in ["poweroff", "reboot", "suspend", "hibernate", "logout", "lock"]:
            self.candidates.append(ExtensionResult(
                name=action,
                description=self.preferences[action],
                icon=f"images/{action}.png",
                on_enter=ExtensionCustomAction(self.preferences[action])
            ))

    def on_input(self, input_text, trigger_id):
        for candidate in self.candidates:
            if input_text in candidate.get_name():
                yield candidate

    def on_item_enter(self, cmd):
        self.logger.info('run: %s', cmd)
        os.system(cmd)

    def on_preferences_update(self, id, value, previous_value):
        self.make_candidates()

if __name__ == '__main__':
    MainExtension().run()
