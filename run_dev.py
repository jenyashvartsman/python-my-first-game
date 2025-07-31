import subprocess
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class GameReloader(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.process = subprocess.Popen([sys.executable, self.script])

    def on_any_event(self, event):
        if event.src_path.endswith(".py"):
            print("🔁 Restarting game...")
            self.process.kill()
            self.process = subprocess.Popen([sys.executable, self.script])

if __name__ == "__main__":
    script_name = "game.py"
    event_handler = GameReloader(script_name)
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        event_handler.process.kill()

    observer.join()
