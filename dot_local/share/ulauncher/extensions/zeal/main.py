import os
import plistlib
import urllib.request as request
import json
import threading
import shutil
import tarfile
from ulauncher.api import AdvancedExtension, ExtensionResult
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction

class MainExtension(AdvancedExtension):

    def __init__(self):
        super(MainExtension, self).__init__()
        self.docsets_path = os.path.expanduser('~/.local/share/Zeal/Zeal/docsets')
        self.timestamp: int = 0
        self.docsets: list[str] = []
        self.data = None

    def need_load(self, sth):
        if sth == 'data':
            return self.data is None
        elif sth == 'docsets':
            if not os.path.isdir(self.docsets_path):
                return False
            timestamp = os.stat(self.docsets_path).st_mtime_ns
            return timestamp != self.timestamp

    def do_load(self, sth):
        if sth == 'data':
            try:
                with request.urlopen('http://api.zealdocs.org/v1/docsets') as f:
                    raw_data = json.loads(f.read())
                    self.data = {}
                    for docset in raw_data:
                        self.data[docset['name']] = docset['versions']
                self.logger.info('update %s data', len(self.data.keys()))
            except:
                return False
            else:
                return True
        elif sth == 'docsets':
            try:
                self.docsets = []
                for name in os.listdir(self.docsets_path):
                    p_list = os.path.join(self.docsets_path, name, 'Contents', 'Info.plist')
                    with open(p_list, "rb") as plist_file:
                        plist_data = plistlib.load(plist_file)
                    self.docsets.append(plist_data.get("CFBundleIdentifier"))
                self.timestamp = os.stat(self.docsets_path).st_mtime_ns
                self.info('update %s docsets', len(self.docsets))
            except Exception as e:
                self.error(e)
                return False
            else:
                return True

    def on_input(self, input_text: str, trigger_id: str):
        if trigger_id == "search":
            return self.on_input_search(input_text)
        else:
            return self.on_input_download(input_text)

    @AdvancedExtension.load('docsets')
    def on_input_search(self, input_text):
        if ':' in input_text:
            cut = input_text.split(':', 1)
            id = cut[0]
            query = cut[1]
            if len(query) != 0 and id in self.docsets:
                url = f'dash-plugin://query={input_text}'
                yield ExtensionResult(
                    name=f"Search in {id}",
                    description=url,
                    on_enter=OpenUrlAction(url)
                )
        else:
            for id in self.docsets:
                if input_text in id:
                    yield ExtensionResult(
                        name=f'Select in "{id}"',
                        description=f"enter to search in {id}",
                        on_enter=SetUserQueryAction(f'{self.preferences["search"]} {id}:')
                    )
 
    @AdvancedExtension.load('data')
    def on_input_download(self, input_text):
        cut = input_text.split(' ', 1)
        if len(cut) == 1:
            for name in self.data.keys():
                if cut[0].lower() in name.lower():
                    yield ExtensionResult(
                        name=name,
                        description=str(self.data[name]),
                        on_enter=SetUserQueryAction(f'{self.preferences["download"]} {name} ')
                    )
        else:
            if cut[0] in self.data.keys():
                name = cut[0]
                if len(self.data[name]) == 0:
                    if len(cut[1]) == 0:
                        yield ExtensionResult(
                            name=name,
                            description=name,
                            on_enter=ExtensionCustomAction({
                                'name': name,
                                'version': None
                            })
                        )
                else:
                    for version in self.data[name]:
                        if cut[1] in version:
                            yield ExtensionResult(
                                name=name,
                                description=version,
                                on_enter=ExtensionCustomAction({
                                    'name': name,
                                    'version': version
                                })
                            )

    def on_item_enter(self, docset):
        name: str = docset['name']
        version: str | None = docset['version']
        tempfile = f'/tmp/{name}.tgz'
        if os.path.isfile(tempfile):
            os.remove(tempfile)
        if version == None:
            url = f'http://{self.preferences["server"]}.kapeli.com/feeds/{name}.tgz'
        else:
            url = f'http://{self.preferences["server"]}.kapeli.com/feeds/zzz/versions/{name}/{version}/{name}.tgz'
        try:
            self.logger.info("download: %s", url)
            def _callback(block_num, block_size, total_size):
                percent = int(float(block_num * block_size) / float(total_size) * 100.0)
                self.notify(f'{name}.tgz', percent)
            request.urlretrieve(url, tempfile, _callback)
        except:
            self.logger.warning("download error: %s", url)
        else:
            if not os.path.isdir(self.docsets_path):
                os.makedirs(self.docsets_path)
            with tarfile.open(tempfile, 'r') as f:
                target_name = f.getmembers()[0].name
                target_dir = os.path.join(self.docsets_path, target_name)
                if os.path.isdir(target_dir):
                    shutil.rmtree(target_dir)
                def is_within_directory(directory, target):
                    
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)
                
                    prefix = os.path.commonprefix([abs_directory, abs_target])
                    
                    return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                    for member in tar.getmembers():
                        member_path = os.path.join(path, member.name)
                        if not is_within_directory(path, member_path):
                            raise Exception("Attempted Path Traversal in Tar File")
                
                    tar.extractall(path, members, numeric_owner=numeric_owner) 
                    
                
                safe_extract(f, self.docsets_path)
            os.system('pkill zeal')

if __name__ == '__main__':
    MainExtension().run()
