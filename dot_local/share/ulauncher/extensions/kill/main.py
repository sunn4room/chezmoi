import os
import subprocess
import threading
from ulauncher.api import Extension, ExtensionResult
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.utils.desktop.notification import show_notification

class MainExtension(Extension):

    def on_input(self, input_text, trigger_id):
        if input_text:
            return ['pgrep', '-u', os.getlogin(), '-a', input_text]
        else:
            return [ExtensionResult(
                name='please type something',
                description='your query string is empty',
                on_enter=HideWindowAction()
            )]
    
    def on_output(self, cmd, output):
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
