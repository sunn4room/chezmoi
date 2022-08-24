import os
import re
from ulauncher.api import Extension, ExtensionResult, StoppableThread
from ulauncher.utils.desktop.notification import show_notification
from ulauncher.api.shared.action.ActionList import ActionList
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenAction import OpenAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction

class VMachine():
    def __init__(self, id: str, name: str, state: bool):
        self.id = id
        self.name = name
        self.state = state

class MainExtension(Extension):

    def __init__(self):
        super(MainExtension, self).__init__()
        self.regex = '^\"(.*)\" {(.*)}$'

    def get_vms(self):
        vms_raw = os.popen('vboxmanage list vms').read().split('\n')[:-1]
        running_vms_raw = os.popen('vboxmanage list runningvms').read().split('\n')[:-1]

        vms: list[VMachine] = []
        for vm_raw in vms_raw:
            match = re.match(self.regex, vm_raw)
            name = match.group(1)
            id = match.group(2)
            state = vm_raw in running_vms_raw
            vms.append(VMachine(id, name, state))
        
        return vms

    def on_input(self, input_text, trigger_id):
        for vm in self.get_vms():
            if input_text in vm.name:
                if vm.state:
                    script = f'vboxmanage controlvm {vm.id} poweroff'
                else:
                    script = f'vboxmanage startvm {vm.id}'
                yield ExtensionResult(
                    name=f'{vm.name} [{"running" if vm.state else "stopped"}]',
                    description=vm.id,
                    on_enter=RunScriptAction(script)
                )

if __name__ == '__main__':
    MainExtension().run()
