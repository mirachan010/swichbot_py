import sys
from switchbot import SwitchBot
import switchbottoken

# 別ファイルで定義できないかなぁって顔してる
action_list = {"0": "turnOff", "1": "turnOn"}
device_list = {"1": {"name": "しんしつ",
                     "id": "01-202304231514-36472826"},
               "2": {"name":  "めいんへや",
                     "id": "01-202304231516-65133257"},
               "3": {"name":  "きっちん",
                     "id": "01-202304231522-72989138"},
               "4": {"name":  "えあこん",
                     "id": "01-202401110022-38574048"}}


def main(args):
    action = action_list[args[2]]
    device = device_list[args[1]]
    bots = SwitchBot(switchbottoken.token, switchbottoken.secret)
    bots.use_device_command(device['id'], action)
    print(device)


if __name__ == '__main__':
    args = sys.argv
    if 3 != len(args):
        print("need 2 args")
        print("python actionfordevice.py (device) (action)")
    else:
        main(args)
