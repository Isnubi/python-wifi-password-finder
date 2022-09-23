import subprocess
import ctypes
import locale


def get_system_language():
    """
    Get the language of the system
    :return:
    """
    windll = ctypes.windll.kernel32
    windll.GetUserDefaultUILanguage()
    language = locale.windows_locale[windll.GetUserDefaultUILanguage()]
    return language


language = get_system_language()
supported_language_list = ["fr_FR", "en_US"]
if get_system_language() not in supported_language_list:
    print("Your language is not supported yet")
    exit()

data = subprocess.check_output(
    ['netsh', 'wlan', 'show', 'profiles']
).decode('utf-8', errors="backslashreplace").split('\n')

if language == "fr_FR":
    profiles = [i.split(':')[1][1:-1] for i in data if "Profil Tous les utilisateurs" in i]
if language == "en_US":
    profiles = [i.split(':')[1][1:-1] for i in data if "All User Profile" in i]

for i in profiles:
    if "\\" in i:
        print(i + "-> unable to process this network because of the special characters")
        continue
    else:

        ssid = None
        key_content = None
        auth_type = None

        profile_info = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'profile', 'name=' + i, 'key=clear']
        ).decode('utf-8', errors="backslashreplace").split('\n')

        for a in profile_info:
            if language == "fr_FR":
                if "Nom du SSID" in a:
                    ssid = a.split(':')[1][2:-2]
                ssid = "No SSID found" if ssid is None else ssid
                if "Contenu de la cl" in a:
                    key_content = a.split(':')[1][1:-1]
                key_content = "No password found" if key_content is None else key_content
                if "Authentification" in a:
                    auth_type = a.split(':')[1][1:-1].split('\\xff')[0]
                auth_type = "No authentication type found" if auth_type is None else auth_type

            if language == "en_US":
                if "SSID name" in a:
                    ssid = a.split(':')[1][2:-2]
                ssid = "No SSID found" if ssid is None else ssid
                if "Key Content" in a:
                    key_content = a.split(':')[1][1:-1]
                key_content = "No password found" if key_content is None else key_content
                if "Authentication" in a:
                    auth_type = a.split(':')[1][1:-1].split('\\xff')[0]
                auth_type = "No authentication type found" if auth_type is None else auth_type

        print(ssid + ": " + key_content + " (" + auth_type + ")")
input("")
