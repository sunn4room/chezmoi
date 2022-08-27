import os
import subprocess
import threading
from ulauncher.api import AdvancedExtension, ExtensionResult
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.utils.desktop.notification import show_notification

class MainExtension(AdvancedExtension):

    def on_input(self, input_text, trigger_id):
        if input_text:
            stdout = self.run_command(['pgrep', '-u', os.getlogin(), '-a', input_text])
            if stdout:
                output = stdout.read().decode('utf-8')
                for line in output.split('\n'):
                    if line:
                        index = line.index(' ')
                        pid = line[:index]
                        cmd = line[index+1:]
                        yield ExtensionResult(
                            name=pid,
                            description=cmd,
                            on_enter=RunScriptAction(f'kill -9 {pid}')
                        )

if __name__ == '__main__':
    MainExtension().run()
