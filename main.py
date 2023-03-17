import argparse
import datetime
import os
import platform
import subprocess
import sys
import time
from multiprocessing import Process

import GPUtil
import psutil
import pyautogui
from tabulate import tabulate

TEST_TIME = 5  # Время проведения теста

FRAPS_BENCHMARKING_HOTKEY = "f11"


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("src", help="Source location")
parser.add_argument("-o", "--output", help="Output location")
args = parser.parse_args()


def get_size(bytes, suffix="B"):
    """
    Метод для форматирования значений оперативной памяти.
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def print_hw_info(file):
    """
    Метод для записи системной информации в файл.
    """
    print(f"System information\n", file=file)
    uname = platform.uname()
    sys_info_list = []
    system = uname.system
    node = uname.node
    version = uname.version
    machine = uname.machine
    sys_info_list.append((system, node, version, machine))
    print(
        tabulate(sys_info_list, headers=("system", "node", "version", "machine")),
        "\n",
        file=file,
    )

    print(f"CPU information\n", file=file)
    cpufreq = psutil.cpu_freq()
    cpu_info_list = []
    processor = uname.processor
    physical_cores = psutil.cpu_count(logical=False)
    total_cores = psutil.cpu_count(logical=True)
    max_freq = f"{cpufreq.max:.2f}Mhz"
    min_freq = f"{cpufreq.min:.2f}Mhz"
    current_freq = f"{cpufreq.current:.2f}Mhz"
    cpu_info_list.append(
        (processor, physical_cores, total_cores, max_freq, min_freq, current_freq)
    )
    print(
        tabulate(
            cpu_info_list,
            headers=(
                "processor",
                "physical cores",
                "total cores",
                "max frequency",
                "min frequency",
                "current frequency",
            ),
        ),
        "\n",
        file=file,
    )

    print(f"Memory information\n", file=file)
    svmem = psutil.virtual_memory()
    ram_list = []
    total = get_size(svmem.total)
    available = get_size(svmem.available)
    used = get_size(svmem.used)
    percentage = f"{svmem.percent}%"
    ram_list.append((total, available, used, percentage))
    print(
        tabulate(
            ram_list,
            headers=(
                "total memory",
                "available memory",
                "used memory",
                "usage percentage",
            ),
        ),
        "\n",
        file=file,
    )

    print(f"GPU information\n", file=file)
    gpus = GPUtil.getGPUs()
    list_gpus = []
    for gpu in gpus:
        gpu_id = gpu.id
        gpu_name = gpu.name
        gpu_total_memory = f"{gpu.memoryTotal}MB"
        gpu_uuid = gpu.uuid
        list_gpus.append((gpu_id, gpu_name, gpu_total_memory, gpu_uuid))
    print(
        tabulate(list_gpus, headers=("id", "name", "total memory", "uuid")),
        "\n",
        file=file,
    )

    print(
        f"{'='*50} Test log {datetime.date.today().strftime('%d/%m/%Y')} {'='*50}",
        "\n",
        file=file,
    )


def monitoring(file):
    """
    Метод для записи статистики использования ресурсов ПК в файл.
    """
    gpu = GPUtil.getGPUs()[0]
    print(
        f"{datetime.datetime.now().strftime('%H:%M:%S')} "
        f"CPU utilization: {psutil.cpu_percent()}% "
        f"Memory usage: {get_size(psutil.virtual_memory().used)} "
        f"GPU usage: {gpu.load*100:.2f}% "
        f"GPU memory usage: {gpu.memoryUsed} MB "
        f"GPU temperature: {gpu.temperature}",
        file=file,
    )


def exit_game():
    """
    Метод для осуществления выхода из игры.
    """
    press_button("esc")
    double_press_button("down")
    press_button("enter")
    double_press_button("down")
    press_button("enter")


def move_forward(interval):
    """
    Метод для эмуляции движения вперед.
    """
    pyautogui.keyDown("w")
    time.sleep(interval)
    pyautogui.keyUp("w")


def take_screenshot(name, path):
    """
    Метод для сохранения скриншота.
    """
    pyautogui.screenshot(f"{path}/test_{name}.png")
    time.sleep(0.25)


def double_press_button(button):
    """
    Метод для эмуляции двойного нажатия клавиши на клавиатуре.
    """
    for _ in range(2):
        press_button(button)


def press_button(button):
    """
    Метод для эмуляции нажатия клавиши на клавиатуре.
    """
    pyautogui.keyDown(button)
    time.sleep(0.25)
    pyautogui.keyUp(button)


def start_fps_benchmark():
    """
    Метод для запуска бенчмарка Fraps.
    """
    press_button(FRAPS_BENCHMARKING_HOTKEY)


def parse_fps_log(output):
    """
    Метод для парсинга среднего FPS за сессию из лог-файла Fraps и записи значения в отдельный файл.
    """
    log_file = r"C:\Fraps\Benchmarks\FRAPSLOG.TXT"
    with open(log_file, "r") as f:
        log_text = f.readlines()
        split_list = log_text[1].split()
        fps = split_list[split_list.index("Avg:") + 1]
    os.unlink(log_file)
    file = open(f"{output}/avg_fps.txt", "w")
    print(f"Average FPS: {fps}", file=file)


def main(exe, output):
    """
    Основная логика работы программы, которая управляет процессом тестирования игры.
    """
    with subprocess.Popen([exe]):
        file = open(f"{output}/stats.txt", "w")
        print_hw_info(file)
        time.sleep(10)
        double_press_button("enter")
        start_fps_benchmark()
        take_screenshot("start", output)
        test = Process(target=move_forward, args=(TEST_TIME,))
        test.start()
        while test.is_alive():
            monitoring(file)
            time.sleep(1)
        take_screenshot("end", output)
        exit_game()
        parse_fps_log(output)


if __name__ == "__main__":
    exe_path = sys.argv[1]
    output_path = args.output
    main(exe_path, output_path)
