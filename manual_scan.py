import subprocess
import ctypes
import locale
import platform


def get_system():
    """
    Get the system name
    :return:
    """
    system = platform.system()
    return system


def get_system_language():
    """
    Get the language of the system
    :return:
    """
    windll = ctypes.windll.kernel32
    windll.GetUserDefaultUILanguage()
    system_language = locale.windows_locale[windll.GetUserDefaultUILanguage()]
    return system_language


match get_system():
    case "Windows":
        data = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'profiles']
        ).decode('utf-8', errors="backslashreplace").split('\n')

        match get_system_language():
            case "fr_FR":
                profiles = [i.split(':')[1][1:-1] for i in data if "Profil Tous les utilisateurs" in i]
            case "en_US":
                profiles = [i.split(':')[1][1:-1] for i in data if "All User Profile" in i]
            case _:
                print("Your language is not supported yet")

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
                    match get_system_language():
                        case "fr_FR":
                            if "Nom du SSID" in a:
                                ssid = a.split(':')[1][2:-2]
                            ssid = "No SSID found" if ssid is None else ssid
                            if "Contenu de la cl" in a:
                                key_content = a.split(':')[1][1:-1]
                            key_content = "No password found" if key_content is None else key_content
                            if "Authentification" in a:
                                auth_type = a.split(':')[1][1:-1].split('\\xff')[0]
                            auth_type = "No authentication type found" if auth_type is None else auth_type
                        case "en_US":
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

    case "Linux":
        print("Linux is not supported yet")

    case "Darwin":
        print("MacOS is not supported yet")

    case _:
        print("Your system is not supported yet")

input("")
