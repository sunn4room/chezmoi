import os
from ulauncher.api import AdvancedExtension, ExtensionResult
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenAction import OpenAction

class MainExtension(AdvancedExtension):

    def on_input(self, input_text, trigger_id):
        if input_text.startswith(os.path.sep):
            cut = input_text.split(' ', 1)
            directory = cut[0]
            pattern = cut[1].strip() if len(cut) == 2 else ''
        else:
            directory = os.path.expanduser('~')
            pattern = input_text.strip()

        if len(pattern) == 0:
            return

        if pattern.startswith("*"):
            pattern = pattern[1:]
        else:
            pattern = "*" + pattern

        if len(pattern) == 0:
            return

        if pattern.endswith("*"):
            pattern = pattern[:-1]
        else:
            pattern = pattern + "*"

        if len(pattern) == 0:
            return

        stdout = self.run_command(['fd', '-g', '-H', '-L', '--max-results=10', '--', pattern, directory])
        if stdout:
            output = stdout.read().decode('utf-8')
            for full_name in output.split('\n'):
                if full_name:
                    if full_name.endswith(os.path.sep):
                        base_name = os.path.basename(full_name[:-1])
                        icon = "images/folder.png"
                    else:
                        base_name = os.path.basename(full_name)
                        icon = "images/file.png"
                    yield ExtensionResult(
                        name=base_name,
                        description=full_name,
                        icon=icon,
                        on_enter=OpenAction(full_name)
                    )

if __name__ == '__main__':
    MainExtension().run()
