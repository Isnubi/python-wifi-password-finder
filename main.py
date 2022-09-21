import subprocess


def get_wlan_ssid():
    data = subprocess.check_output(
        ['netsh', 'wlan', 'show', 'profiles']
    ).decode('utf-8', errors="backslashreplace").split('\n')

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

            for a in profile_info:
                if "SSID name" in a:
                    ssid = a.split(':')[1][2:-2]
                    break
                ssid = "No SSID found" if ssid is None else ssid
            ssid_list.append(ssid)
    return ssid_list


def get_wlan_infos(ssid):
    key_content = None
    auth_type = None

    profile_info = subprocess.check_output(
        ['netsh', 'wlan', 'show', 'profile', 'name=' + ssid, 'key=clear']
    ).decode('utf-8', errors="backslashreplace").split('\n')

    for a in profile_info:
        if "Key Content" in a:
            key_content = a.split(':')[1][1:-1]
        key_content = "No password found" if key_content is None else key_content

        if "Authentication" in a:
            auth_type = a.split(':')[1][1:-1].split('\\xff')[0]
        auth_type = "No authentication type found" if auth_type is None else auth_type

    return key_content, auth_type


"""
put the UI process here
"""