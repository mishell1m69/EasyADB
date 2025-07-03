"""

-- By MICHEL Clément, student at IUT Réseaux et Télécommunications, Université Côte d'Azur, Valbonne, France
-- Started : 02/07/2025 on HP ProBook 450 G9
-- Phones used for ADB testing: Redmi Note 8 Pro (mainly), Redmi Note 13 Pro+ 5G (comparison)
-- Objectives : A few days ago, i dicovered ADB and wanted to dive deeper into it. I started learning some commands and quickly thought that creating
an interractive interface would be pretty useful, as i could be used to start commands into Powershell, but also store all of my favourite commands.
This interface should now be considered as a tool, that can be used differently, wether you choose to use "Logcat" or "Network" commands, for example.
-- Was AI used in this project? : Yes, i required the use of AI to help me build the basic structure of this interface as i was not familiar 
at all with Tkinter and ADB-to-Python linking. It did work pretty well and i do not regret using it, as it allowed me to build this GUI, just like
imagined it.
-- Suitable for commercial use? : Not for commercial use, just for personal use and to help others.
-- Websites used: 
-> https://developer.android.com/tools/releases/platform-tools?hl=fr
-> https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20
-> https://developer.android.com/tools/adb?hl=fr
-> https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://gist.github.com/Pulimet/5013acf2cd5b28e55036c82c91bd56d8&ved=2ahUKEwiR-oup_J6OAxWLcKQEHePBLbIQFnoECAoQAQ&usg=AOvVaw0QtLJ20OqCl3S4BR0S4BVe

""" 

# _____ __  __ _____   ____  _____ _______ _____ 
 #|_   _|  \/  |  __ \ / __ \|  __ \__   __/ ____|
 #  | | | \  / | |__) | |  | | |__) | | | | (___  
 #  | | | |\/| |  ___/| |  | |  _  /  | |  \___ \ 
 # _| |_| |  | | |    | |__| | | \ \  | |  ____) |
 #|_____|_|  |_|_|     \____/|_|  \_\ |_| |_____/ 

                                                                                       
import subprocess
import os
import tkinter as tk


# __      __     _____  _____          ____  _      ______  _____ 
# \ \    / /\   |  __ \|_   _|   /\   |  _ \| |    |  ____|/ ____|
#  \ \  / /  \  | |__) | | |    /  \  | |_) | |    | |__  | (___  
#   \ \/ / /\ \ |  _  /  | |   / /\ \ |  _ <| |    |  __|  \___ \ 
#    \  / ____ \| | \ \ _| |_ / ____ \| |_) | |____| |____ ____) |
#     \/_/    \_\_|  \_\_____/_/    \_\____/|______|______|_____/  
                                                               

# Path to adb (not sure if its .exe or the whole folder that matters)
ADB_PATH = os.path.abspath("platform-tools")
ADB_EXE = os.path.join(ADB_PATH, "adb")

# Global process (so it can be stopped)
current_process = None


#  ______ _    _ _   _  _____ _______ _____ ____  _   _  _____ 
# |  ____| |  | | \ | |/ ____|__   __|_   _/ __ \| \ | |/ ____|
# | |__  | |  | |  \| | |       | |    | || |  | |  \| | (___  
# |  __| | |  | | . ` | |       | |    | || |  | | . ` |\___ \ 
# | |    | |__| | |\  | |____   | |   _| || |__| | |\  |____) |
# |_|     \____/|_| \_|\_____|  |_|  |_____\____/|_| \_|_____/ 
                                                              
                                                              
# To execute an ADB command in Powershell
def run_adb_command(command):
    global current_process
    try:
        args = command.strip().split()

        # Special case to logcat to a .txt file
        if args[0] == "logcat" and ">" in args:
            out_file = args[args.index(">") + 1]
            logcat_command = args[:args.index(">")]
            with open(out_file, "w", encoding="utf-8") as f:
                print(f"[INFO] Export de logcat vers {out_file}")
                current_process = subprocess.Popen([ADB_EXE] + logcat_command, stdout=f, stderr=subprocess.STDOUT)
        else:
            full_command = [ADB_EXE] + args
            print(f"Exécution : {' '.join(full_command)}")
            current_process = subprocess.Popen(full_command)

    except Exception as e:
        print(f"[ERREUR] {e}")


# Open an URL on the device
def open_url_prompt():
    # New popup window
    url_window = tk.Toplevel(root)
    url_window.title("Ouvrir une URL")
    url_window.geometry("400x120")

    tk.Label(url_window, text="Entrez l'URL à ouvrir sur l'appareil :").pack(pady=5)
    
    url_entry = tk.Entry(url_window, width=50)
    url_entry.pack(pady=5)

    def launch_url():
        url = url_entry.get().strip()
        if url:
            command = f"shell am start -a android.intent.action.VIEW -d {url}"
            run_adb_command(command)
            url_window.destroy()

    launch_btn = tk.Button(url_window, text="Lancer", command=launch_url)
    launch_btn.pack(pady=5)

# Ping an URL
def ping_url_prompt():
    # New popup window
    url_window = tk.Toplevel(root)
    url_window.title("Ping une URL")
    url_window.geometry("400x120")

    tk.Label(url_window, text="Entrez l'URL à Ping :").pack(pady=5)
    
    url_entry = tk.Entry(url_window, width=50)
    url_entry.pack(pady=5)

    def launch_url():
        url = url_entry.get().strip()
        if url:
            command = f"shell ping {url}"
            run_adb_command(command)
            url_window.destroy()

    launch_btn = tk.Button(url_window, text="Ping", command=launch_url)
    launch_btn.pack(pady=5)


def launch_scrcpy():
    scrcpy_path = r"C:\\ADB\scrcpy-win64-v3.3.1\scrcpy.exe""
    subprocess.Popen(scrcpy_path)


# Stop the current process (equivalent to Ctrl+C)
def stop_command():
    global current_process
    if current_process and current_process.poll() is None:
        current_process.terminate()
        print("[INFO] Commande interrompue (équivalent Ctrl+C)")
        current_process = None


# Close the interface
def quit_gui():
    stop_command()  # We ensure no process stays active
    root.destroy()


 # __  __          _____ _   _   _      ____   ____  _____  
 #|  \/  |   /\   |_   _| \ | | | |    / __ \ / __ \|  __ \ 
 #| \  / |  /  \    | | |  \| | | |   | |  | | |  | | |__) |
 #| |\/| | / /\ \   | | | . ` | | |   | |  | | |  | |  ___/ 
 #| |  | |/ ____ \ _| |_| |\  | | |___| |__| | |__| | |     
 #|_|  |_/_/    \_\_____|_| \_| |______\____/ \____/|_|     
                                                                                                                     

# Interface
root = tk.Tk()
root.title("ADB command pannel")
root.geometry("512x512")


# SERVER --------------------------------------------------------------------------------------------------------
# Menu for Server 
server_menu = tk.Menu(root, tearoff=0)
server_menu.add_command(label="Start", command=lambda: run_adb_command("start-server"))
server_menu.add_command(label="Kill", command=lambda: run_adb_command("kill-server"))
server_menu.add_command(label="Reconnect (Host side)", command=lambda: run_adb_command("reconnect"))
server_menu.add_command(label="Reconnect (Device side)", command=lambda: run_adb_command("reconnect device"))
server_menu.add_command(label="Attach device", command=lambda: run_adb_command("attach"))
server_menu.add_command(label="Detach device", command=lambda: run_adb_command("detach"))

def show_server_menu(event):
    server_menu.tk_popup(event.x_root, event.y_root)

btn_server = tk.Button(root, text="Server", width=25, fg="green")
btn_server.pack(pady=10)
btn_server.bind("<Button-1>", show_server_menu)


# DEVICE --------------------------------------------------------------------------------------------------------
# Menu for Device
device_menu = tk.Menu(root, tearoff=0)
device_menu.add_command(label="Devices", command=lambda: run_adb_command("devices -l"))
device_menu.add_command(label="Serial number", command=lambda: run_adb_command("get-serialno"))
device_menu.add_command(label="State", command=lambda: run_adb_command("get-state"))
device_menu.add_command(label="Android version", command=lambda: run_adb_command("shell getprop ro.build.version.release"))
device_menu.add_command(label="Devpath", command=lambda: run_adb_command("get-devpath"))
device_menu.add_command(label="IMEI", command=lambda: run_adb_command("shell dumpsys iphonesybinfo"))
device_menu.add_command(label="Battery", command=lambda: run_adb_command("shell dumpsys battery"))
device_menu.add_command(label="Screen resolution", command=lambda: run_adb_command("shell wm size"))
device_menu.add_command(label="Features", command=lambda: run_adb_command("shell pm list features"))
device_menu.add_command(label="Services", command=lambda: run_adb_command("shell service list"))
device_menu.add_command(label="Bugreport", command=lambda: run_adb_command("bugreport"))

def show_device_menu(event):
    device_menu.tk_popup(event.x_root, event.y_root)

btn_device = tk.Button(root, text="Device", width=25, fg="green")
btn_device.pack(pady=10)
btn_device.bind("<Button-1>", show_device_menu)


# LOGCAT --------------------------------------------------------------------------------------------------------
# Menu for Logcat
logcat_menu = tk.Menu(root, tearoff=0)
logcat_menu.add_command(label="Logcat", command=lambda: run_adb_command("logcat"))
logcat_menu.add_command(label="Logcat to file (txt)", command=lambda: run_adb_command("logcat > logcat_report.txt"))
logcat_menu.add_command(label="Logcat dump", command=lambda: run_adb_command("logcat -d"))
logcat_menu.add_command(label="Logcat dump to file (txt)", command=lambda: run_adb_command("logcat -d> logcat_report.txt"))
logcat_menu.add_command(label="Logcat clear", command=lambda: run_adb_command("logcat -c"))
logcat_menu.add_command(label="Detect Logcat E (Error)", command=lambda: run_adb_command("logcat *:E"))
logcat_menu.add_command(label="Detect Logcat F (Fatal)", command=lambda: run_adb_command("logcat *:F"))
logcat_menu.add_command(label="Detect Logcat S (Silent)", command=lambda: run_adb_command("logcat *:S"))
logcat_menu.add_command(label="Logcat help", command=lambda: run_adb_command("logcat --help"))

def show_logcat_menu(event):
    logcat_menu.tk_popup(event.x_root, event.y_root)

btn_logcat = tk.Button(root, text="Logcat", width=25, fg="green")
btn_logcat.pack(pady=10)
btn_logcat.bind("<Button-1>", show_logcat_menu)


# NETWORK --------------------------------------------------------------------------------------------------------
# Menu forr Network
network_menu = tk.Menu(root, tearoff=0)
network_menu.add_command(label="Show IpV4-6/Interfaces", command=lambda: run_adb_command("shell ip a"))
network_menu.add_command(label="Netstat", command=lambda: run_adb_command("shell netstat"))
network_menu.add_command(label="Ip route", command=lambda: run_adb_command("shell ip route  "))
network_menu.add_command(label="Dumpsys Wi-Fi", command=lambda: run_adb_command("shell dumpsys wifi"))
network_menu.add_command(label="Wi-Fi ON", command=lambda: run_adb_command("shell svc wifi enable"))
network_menu.add_command(label="Wi-Fi OFF", command=lambda: run_adb_command("shell svc wifi disable"))
network_menu.add_command(label="Data ON", command=lambda: run_adb_command("shell svc data enable"))
network_menu.add_command(label="Data OFF", command=lambda: run_adb_command("shell svc data disable"))
network_menu.add_command(label="Show primary DNS", command=lambda: run_adb_command("shell getprop net.dns1"))
network_menu.add_command(label="Ping URL", command=ping_url_prompt)

def show_network_menu(event):
    network_menu.tk_popup(event.x_root, event.y_root)

btn_network = tk.Button(root, text="Network", width=25, fg="green")
btn_network.pack(pady=10)
btn_network.bind("<Button-1>", show_network_menu)


# OTHER--------------------------------------------------------------------------------------------------------
# Menu for Other 
other_menu = tk.Menu(root, tearoff=0)
other_menu.add_command(label="Screenshot", command=lambda: run_adb_command("shell screencap -p /sdcard/screenshot.png"))
other_menu.add_command(label="Home", command=lambda: run_adb_command("shell am start -W -c android.intent.category.HOME -a android.intent.action.MAIN"))
other_menu.add_command(label="URL", command=open_url_prompt)
other_menu.add_command(label="ADB version", command=lambda: run_adb_command("version"))

def show_other_menu(event):
    other_menu.tk_popup(event.x_root, event.y_root)

btn_other = tk.Button(root, text="Other", width=25, fg="green")
btn_other.pack(pady=10)
btn_other.bind("<Button-1>", show_other_menu)


# Other commands/buttons
# SHIZUKU --------------------------------------------------------------------------------------------------------
btn_help = tk.Button(root, text="Start Shizuku", width=25, command=lambda: run_adb_command("shell sh /sdcard/Android/data/moe.shizuku.privileged.api/start.sh"), fg="purple")
btn_help.pack(pady=10)

# SCRCPY --------------------------------------------------------------------------------------------------------
btn_scrcpy = tk.Button(root, text="Lancer scrcpy", width=25, command=launch_scrcpy)
btn_scrcpy.grid(row=x, column=y, padx=5, pady=5)

# HELP --------------------------------------------------------------------------------------------------------
btn_help = tk.Button(root, text="Help", width=25, command=lambda: run_adb_command("help"), fg="blue")
btn_help.pack(pady=10)


# STOP --------------------------------------------------------------------------------------------------------
btn_stop = tk.Button(root, text="Stop current command (Ctrl+C)", width=25, command=stop_command, fg="red")
btn_stop.pack(pady=10)


# QUIT --------------------------------------------------------------------------------------------------------
btn_quit = tk.Button(root, text="Quit", width=25, command=quit_gui, fg="red")
btn_quit.pack(pady=10)


root.mainloop()
