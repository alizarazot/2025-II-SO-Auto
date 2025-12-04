from sys import argv

from psutil import process_iter, AccessDenied


def main(args=argv):
    assert len(args) > 0  # A full command line is expected.

    target_letter = None
    if len(args) == 2:
        target_letter = args[1]

    if target_letter is None:
        print("Available Processes:")

    offending = []
    for proc in process_iter(["pid", "name", "exe"]):
        name, pid, exe = proc.info["name"], proc.info["pid"], proc.info["exe"]

        if target_letter is None:
            print(f" - {pid:>5}: {name}")
            continue

        if exe is None:
            print(f"Couldn't check process executable: {name} ({pid}).")

        if exe is not None and exe.lower().startswith(target_letter.lower()):
            print(f"{name} ({pid}) -> {exe}")
            offending.append(proc)

        files: list[str]
        try:
            files = proc.open_files()
        except AccessDenied:
            print(f"Couldn't check process files: {name} ({pid}).")
            continue

        for file in files:
            path = file.path
            if path.lower().startswith(target_letter.lower()):
                print(f"{name} ({pid}) -> {file}")
                offending.append(proc)

    if len(offending) != 0:
        print("Do you want to kill this process? [y/n]")
    for proc in offending:
        name, pid = proc.info["name"], proc.info["pid"]
        print(f" - {name} ({pid})", end=" ")
        if prompt_ask_agree():
            proc.kill()


def prompt_ask_agree() -> bool:
    answer = input("[y/n]: ").lower()
    if answer != "y" and answer != "n":
        print("You can only answer with 'y' or 'n', for 'yes' and 'no' respectively!")
        print("    ", end="")
        return prompt_ask_agree()
    return answer == "y"


if __name__ == "__main__":
    main()
