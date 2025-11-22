"""
Real-time Log File Watcher

Monitors log files for new entries and streams them in real-time.
Similar to 'tail -f' functionality.
"""

import time
from pathlib import Path
from typing import Generator, Callable, Optional
import threading


class LogWatcher:
    """Watch log files for new entries in real-time"""
    
    def __init__(self, filepath: str, poll_interval: float = 1.0):
        """
        Initialize log watcher
        
        Args:
            filepath: Path to log file to watch
            poll_interval: How often to check for new lines (seconds)
        """
        self.filepath = Path(filepath)
        self.poll_interval = poll_interval
        self._stop_flag = False
        self._file_position = 0
    
    def watch(self) -> Generator[str, None, None]:
        """
        Generator that yields new lines as they appear in the log file
        
        Yields:
            New log lines as strings
        """
        if not self.filepath.exists():
            raise FileNotFoundError(f"Log file not found: {self.filepath}")
        
        with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
            # Start from end of file for real-time monitoring
            f.seek(0, 2)
            self._file_position = f.tell()
            
            while not self._stop_flag:
                line = f.readline()
                if line:
                    self._file_position = f.tell()
                    yield line.strip()
                else:
                    # No new data, wait before checking again
                    time.sleep(self.poll_interval)
                    
                    # Check if file was truncated (log rotation)
                    current_size = self.filepath.stat().st_size
                    if current_size < self._file_position:
                        # File was truncated, start from beginning
                        f.seek(0)
                        self._file_position = 0
    
    def watch_from_beginning(self) -> Generator[str, None, None]:
        """
        Generator that yields all lines from the beginning, then continues watching
        
        Yields:
            All log lines (historical + new) as strings
        """
        if not self.filepath.exists():
            raise FileNotFoundError(f"Log file not found: {self.filepath}")
        
        with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
            # Read all existing lines first
            for line in f:
                if self._stop_flag:
                    return
                yield line.strip()
            
            self._file_position = f.tell()
            
            # Now watch for new lines
            while not self._stop_flag:
                line = f.readline()
                if line:
                    self._file_position = f.tell()
                    yield line.strip()
                else:
                    time.sleep(self.poll_interval)
                    
                    # Check for log rotation
                    current_size = self.filepath.stat().st_size
                    if current_size < self._file_position:
                        f.seek(0)
                        self._file_position = 0
    
    def stop(self):
        """Stop watching the file"""
        self._stop_flag = True
    
    def reset(self):
        """Reset the stop flag to allow restarting"""
        self._stop_flag = False
        self._file_position = 0


class AsyncLogWatcher:
    """Asynchronous log watcher that runs in a separate thread"""
    
    def __init__(self, filepath: str, callback: Callable[[str], None], 
                 poll_interval: float = 1.0, from_beginning: bool = False):
        """
        Initialize async log watcher
        
        Args:
            filepath: Path to log file
            callback: Function to call with each new line
            poll_interval: How often to check for new lines (seconds)
            from_beginning: If True, read entire file first
        """
        self.watcher = LogWatcher(filepath, poll_interval)
        self.callback = callback
        self.from_beginning = from_beginning
        self._thread: Optional[threading.Thread] = None
    
    def start(self):
        """Start watching in a background thread"""
        if self._thread and self._thread.is_alive():
            return  # Already running
        
        self.watcher.reset()
        self._thread = threading.Thread(target=self._watch_loop, daemon=True)
        self._thread.start()
    
    def _watch_loop(self):
        """Main watch loop (runs in thread)"""
        try:
            watch_gen = (self.watcher.watch_from_beginning() 
                        if self.from_beginning 
                        else self.watcher.watch())
            
            for line in watch_gen:
                self.callback(line)
        except Exception as e:
            print(f"Error in watch loop: {e}")
    
    def stop(self):
        """Stop watching"""
        self.watcher.stop()
        if self._thread:
            self._thread.join(timeout=2.0)
    
    def is_running(self) -> bool:
        """Check if watcher is currently running"""
        return self._thread is not None and self._thread.is_alive()


# Utility function for simple use cases
def tail_file(filepath: str, num_lines: int = 10) -> list[str]:
    """
    Get the last N lines from a file (like 'tail -n')
    
    Args:
        filepath: Path to file
        num_lines: Number of lines to return
    
    Returns:
        List of last N lines
    """
    path = Path(filepath)
    if not path.exists():
        return []
    
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        return [line.strip() for line in lines[-num_lines:]]
