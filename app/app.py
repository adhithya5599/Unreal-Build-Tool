import subprocess
import time
import random
from os.path import abspath, dirname, join
import os
import datetime
import configparser
import json

from discord_webhooks import DiscordWebhooks

last_build_path = join(dirname(abspath(__file__)), "last_build.ini")
unreal_build_path = join(dirname(abspath(__file__)), "../../../UnrealTestBuilds")
config_path = join(dirname(abspath(__file__)), "config.ini")

if __name__ == "__main__":
    folderTimestamp = os.path.getmtime(unreal_build_path)
    last_build_data = datetime.datetime.fromtimestamp(folderTimestamp).isoformat()
    config = configparser.ConfigParser()
    config.read(config_path)
    DISCORD_WEBHOOK_URL = config['Discord']['webhook']
    
    with open(last_build_path, 'r') as f:
        datetimeValue = f.read().strip()
    print(datetimeValue)
    print(last_build_data)
    if(datetimeValue == last_build_data):
       print("Values are same")
    else:
        print("Latest Build Detected")
        with open(last_build_path, 'w') as f:
            f.write("%s" % str(last_build_data))
        message = DiscordWebhooks(DISCORD_WEBHOOK_URL)
        message.set_author(name="Unreal Build Tool : New Build successful" )
        message.set_content(color=0x009900, description= "Farm Hands game was built sucessfully and uploaded to the [Google Drive Folder](https://drive.google.com/drive/folders/1ZivDW9GnbjTnDhitT9ynq0SpxBAkg3Qy)")
        message.send()
        print("Payload Sent")
        time.sleep(15)