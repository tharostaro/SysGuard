
import platform
import psutil

from database import init_db, save_metric, get_history
from logger import setup_logger


logger = setup_logger()


# ==========================================
# SYSGUARD v3.0
# LINUX SYSTEM MONITORING TOOL
# ==========================================


def banner():
    print("=" * 45)
    print("             SYSGUARD v3.0")
    print("          LINUX SYSTEM MONITOR")
    print("=" * 45)


# SYSTEM INFORMATION

def system_info():
    print("\n[ SYSTEM INFORMATION ]")
    print("-" * 45)

    print(f"System: {platform.system()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Hostname: {platform.node()}")
    print(f"Python: {platform.python_version()}")

    logger.info("System information viewed")


# CPU MONITOR

def cpu_info():
    print("\n[ CPU MONITOR ]")
    print("-" * 45)

    usage = psutil.cpu_percent(interval=1)

    print(f"CPU Usage: {usage}%")

    save_metric("CPU", usage)
    logger.info(f"CPU usage recorded: {usage}%")


# RAM MONITOR

def ram_info():
    print("\n[ RAM MONITOR ]")
    print("-" * 45)

    memory = psutil.virtual_memory()

    total = memory.total / (1024 ** 3)
    used = memory.used / (1024 ** 3)

    print(f"Total RAM: {total:.2f} GB")
    print(f"Used RAM: {used:.2f} GB")
    print(f"Usage: {memory.percent}%")

    save_metric("RAM", memory.percent)
    logger.info(f"RAM usage recorded: {memory.percent}%")


# PROCESS MONITOR

def process_info():
    print("\n[ RUNNING PROCESSES ]")
    print("-" * 45)

    count = 0

    for process in psutil.process_iter(['pid', 'name']):

        if count >= 15:
            break

        try:
            pid = process.info['pid']
            name = process.info['name'] or "Unknown"

            print(f"PID: {pid:<10} NAME: {name}")
            count += 1

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    print("-" * 45)
    print(f"Displayed processes: {count}")

    logger.info("Process viewer opened")


# DISK MONITOR

def disk_info():
    print("\n[ DISK MONITOR ]")
    print("-" * 45)

    disk = psutil.disk_usage('/')

    total = disk.total / (1024 ** 3)
    used = disk.used / (1024 ** 3)
    free = disk.free / (1024 ** 3)

    print(f"Total Storage: {total:.2f} GB")
    print(f"Used Storage: {used:.2f} GB")
    print(f"Free Storage: {free:.2f} GB")
    print(f"Usage: {disk.percent}%")

    logger.info("Disk information viewed")


# METRICS HISTORY

def history_info():
    print("\n[ METRICS HISTORY ]")
    print("-" * 60)

    history = get_history()

    if not history:
        print("No measurements found.")
        return

    for name, value, timestamp in history:
        print(f"{timestamp} | {name}: {value}%")

    print("-" * 60)

    logger.info("Metrics history viewed")


# MAIN MENU

def main():

    init_db()
    logger.info("SysGuard started")

    while True:

        banner()

        print("\n[ MAIN MENU ]")
        print("1. System Information")
        print("2. CPU Monitor")
        print("3. RAM Monitor")
        print("4. Process Viewer")
        print("5. Disk Usage")
        print("6. Metrics History")
        print("0. Exit")

        choice = input("\nSysGuard > ").strip()

        if choice == "1":
            system_info()

        elif choice == "2":
            cpu_info()

        elif choice == "3":
            ram_info()

        elif choice == "4":
            process_info()

        elif choice == "5":
            disk_info()

        elif choice == "6":
            history_info()

        elif choice == "0":
            logger.info("SysGuard stopped")
            print("\n[+] SysGuard shutting down...")
            break

        else:
            print("\n[!] Invalid option!")

        input("\nPress ENTER to continue...")


# PROGRAM ENTRY POINT

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        logger.warning("SysGuard interrupted by user")
        print("\n\n[!] SysGuard interrupted.")

