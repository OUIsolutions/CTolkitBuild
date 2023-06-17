from CToolKit.Errors.ExecutionError import ExecutionError
import subprocess


class ComandLineExecution:

    def __init__(self, command: str):
        self.status_code, self.output = subprocess.getstatusoutput(command)

        if self.status_code != 0:
            raise ExecutionError(self.output, self.status_code)
