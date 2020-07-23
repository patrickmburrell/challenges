from datetime import datetime
import threading
import click

DEFAULT_TASK_DURATION_MIN = 20
DEFAULT_REST_DURATION_MIN = 5

_tasklen = 20
_breaklen = 5
_remaining_loops = 2
_loop = 0


def start_task_timer():
    print("start your task")
    task_timer = threading.Timer(_tasklen, task_over)
    task_timer.start()


def start_break_timer():
    print("start your break")
    break_timer = threading.Timer(_breaklen, break_over)
    break_timer.start()


def task_over():
    # global _loop
    # print(f"task period {_loop+1} is over")
    print(f"task period is complete")
    start_break_timer()


def break_over():
    # global _loop
    # print(f"break period {_loop+1} is over")
    print(f"break period is complete")
    loop_over()


def loop_over():
    global _loop
    global _remaining_loops

    print(f"loop {_loop+1} is complete\n")

    _loop += 1
    _remaining_loops += -1

    if _remaining_loops > 0:
        start_task_timer()
    else:
        print("\nPomodoro session is complete\n")


@click.command()
@click.option("--tasklen", default=20, help="length of a task timer in minutes")
@click.option("--breaklen", default=5, help="length of a break timer in minutes")
@click.option("--loops", default=2, help="number of task+break timers to run")
def main(tasklen, breaklen, loops):
    print(f"\ntasklen: {tasklen}")
    print(f"breaklen: {breaklen}")
    print(f"loops: {loops}\n")

    global _tasklen
    global _breaklen
    global _remaining_loops

    _tasklen = tasklen
    _breaklen = breaklen
    _remaining_loops = loops

    start_task_timer()


if __name__ == "__main__":
    main()
