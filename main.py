import subprocess
import locale
import ctypes
import tkinter as tk
from tkinter import ttk


def get_system_language():
    """
    Get the language of the system
    :return:
    """
    windll = ctypes.windll.kernel32
    windll.GetUserDefaultUILanguage()
    language = locale.windows_locale[windll.GetUserDefaultUILanguage()]
    return language


def get_wlan_ssid(language):
    """
    Get the SSID of the available networks using the netsh command
    :param language: The language of the system
    :return:
    """
    data = subprocess.check_output(
        ['netsh', 'wlan', 'show', 'profiles']
    ).decode('utf-8', errors="backslashreplace").split('\n')

    if language == "fr_FR":
        profiles = [i.split(':')[1][1:-1] for i in data if "Profil Tous les utilisateurs" in i]
    if language == "en_US":
        profiles = [i.split(':')[1][1:-1] for i in data if "All User Profile" in i]

    ssid_list = []
    for i in profiles:
        if "\\" in i:
            continue
        else:
            ssid = None
            profile_info = subprocess.check_output(
                ['netsh', 'wlan', 'show', 'profile', 'name=' + i, 'key=clear']
            ).decode('utf-8', errors="backslashreplace").split('\n')

            if language == "fr_FR":
                for a in profile_info:
                    if "Nom du SSID" in a:
                        ssid = a.split(':')[1][2:-2]
                        break
                    ssid = "No SSID found" if ssid is None else ssid
                ssid_list.append(ssid)
            if language == "en_US":
                for a in profile_info:
                    if "SSID name" in a:
                        ssid = a.split(':')[1][2:-2]
                        break
                    ssid = "No SSID found" if ssid is None else ssid
                ssid_list.append(ssid)
    return ssid_list


def get_wlan_infos(ssid, language):
    """
    Get the password and the authentication type of the selected SSID
    :param ssid: The SSID of the network
    :param language: The language of the system
    """
    key_content = None
    auth_type = None

    profile_info = subprocess.check_output(
        ['netsh', 'wlan', 'show', 'profile', 'name=' + ssid, 'key=clear']
    ).decode('utf-8', errors="backslashreplace").split('\n')

    if language == "fr_FR":
        for a in profile_info:
            if "Contenu de la cl" in a:
                key_content = a.split(':')[1][1:-1]
            key_content = "No password found" if key_content is None else key_content

            if "Authentification" in a:
                auth_type = a.split(':')[1][1:-1].split('\\xff')[0]
            auth_type = "No authentication type found" if auth_type is None else auth_type
    if language == "en_US":
        for a in profile_info:
            if "Key content" in a:
                key_content = a.split(':')[1][1:-1]
            key_content = "No password found" if key_content is None else key_content

            if "Authentication" in a:
                auth_type = a.split(':')[1][1:-1].split('\\xff')[0]
            auth_type = "No authentication type found" if auth_type is None else auth_type

    return key_content, auth_type


def print_infos(infos, ssid_combo, language):
    """
    Print the password and the authentication type of the selected SSID
    :param infos: The text widget
    :param ssid_combo: The combobox widget
    """
    infos.delete('1.0', tk.END)
    infos.insert(tk.END, f"\nSSID: {ssid_combo.get()}\nPassword: {get_wlan_infos(ssid_combo.get(), language)[0]}\n"
                         f"Authentication type: {get_wlan_infos(ssid_combo.get(), language)[1]}", "center")


def script_ui():
    """
    Create the UI
    """
    root = tk.Tk()
    root.title("Wifi Password Viewer")
    root.geometry("500x200")
    root.resizable(False, False)

    supported_language_list = ["fr_FR", "en_US"]
    if get_system_language() not in supported_language_list:
        print("Your language is not supported yet")
        exit()

    ssid_list = get_wlan_ssid(get_system_language())
    ssid_list.sort()
    ssid_combo = ttk.Combobox(root, values=ssid_list, state="readonly")
    ssid_combo.pack(pady=10)

    infos = tk.Text(root, height=5, width=50)
    infos.tag_configure("center", justify='center')
    ssid_combo.bind("<<ComboboxSelected>>", lambda e: print_infos(infos, ssid_combo, get_system_language()))
    infos.pack()

    root.mainloop()


def main():
    """
    Main function
    """
    script_ui()


main()
