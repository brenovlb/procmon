#!/usr/bin/env python3
import os
import time

def list_processes():
    processes = []
    for pid in os.listdir("/proc"):
        if pid.isdigit():
            try:
                with open(f"/proc/{pid}/comm", "r") as f:
                    name = f.read().strip()
                stat = open(f"/proc/{pid}/stat", "r").read().split()
                with open(f"/proc/{pid}/status", "r") as f:
                    status = f.readlines()

                utime = int(stat[13])
                stime = int(stat[14])
                mem_kb = 0
                for line in status: 
                    if line.startswith("VmRSS:"):
                        mem_kb = int(line.split()[1])
                        break
                processes.append({
                    "pid": pid,
                    "name": name,
                    "cpu_time": utime + stime,
                    "mem_kb": mem_kb
                })
            except Exception:
                continue
    return processes

def print_processes(processes):
    print(f"{'PID':>6} {'Name':<50} {'CPU Time':>10} {'Mem KB':>10}")
    print("-" * 80)
    for proc in processes:
        print(f"{proc['pid']:>6} {proc['name']:<50} {proc['cpu_time']:>10} {proc['mem_kb']:>10}")

if __name__ == "__main__":
    try:
        while True:
            os.system("clear")
            procs = list_processes()
            print(f"procmon - {len(procs)} processes running\n")
            procs.sort(key=lambda x: x['cpu_time'], reverse=True)
            print_processes(procs[:50])
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nExiting procmon")