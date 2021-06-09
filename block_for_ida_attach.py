import sys
import tkinter
from time import sleep

import frida

class FridaManager:

    def __init__(self,script_path):
        with open(script_path, "r", encoding="utf8") as fp:
            self.jscode = fp.read()
        self.script=None

    def on_message(self,message, data):
        if message['type'] == 'send':
            print("[*] {0}".format(message['payload'].encode("utf8")))

            if message['payload']=="block":
                # 子线程中接收不到命令行的输入，采用tkinter来控制程序何时继续
                root=tkinter.Tk()
                root.mainloop()
                self.script.post({'type': 'input', 'payload': "z"})
        else:
            # error type or others
            print(message["type"])
            for key,value in message.items():
                print(key+":"+str(value))


    def spawn_package(self,package_name):
        # device = my_frida.get_device(device,1)
        try:
            frida.kill(package_name)
        except Exception as e:
            pass
        device=frida.get_usb_device(1)
        pid = device.spawn([package_name])
        sleep(1)
        process = device.attach(package_name)
        # process.enable_child_gating()
        sleep(1)
        self.script = process.create_script(self.jscode)
        self.script.on('message', self.on_message)

        print('[*] start hooking')
        self.script.load()

        # print("sleep 3s")
        device.resume(pid)
        sys.stdin.read()

    def attach_package(self,package_name):
        device=frida.get_usb_device(1)
        process = device.attach(package_name)
        process.enable_child_gating()
        self.script = process.create_script(self.jscode)
        self.script.on('message', self.on_message)
        print('[*] start hooking')
        self.script.load()
        sys.stdin.read()

if __name__=='__main__':
    manager=FridaManager("hook_load_library.js")
    manager.spawn_package("com.intel")