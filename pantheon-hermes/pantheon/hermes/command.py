import subprocess
import shlex
import logging

LOGGER = logging.getLogger(__name__)


class Command:
    def __init__(self, command):
        try:
            self.args = shlex.split(command)
        except AttributeError:
            self.args = command

        self.command = shlex.quote(' '.join(self.args))
        self.process = None
        self.stdout = None
        self.stderr = None

    @property
    def returncode(self):
        try:
            return self.process.returncode
        except AttributeError:
            return None

    def log_lines(self):
        if self.stdout is not None:
            for line in self.stdout.splitlines():
                line = line.decode("utf-8").strip()
                if line:
                    LOGGER.debug(line)

        if self.stderr is not None:
            for line in self.stderr.splitlines():
                line = line.decode("utf-8").strip()
                if line:
                    LOGGER.error(line)

    def __bool__(self):
        return self.returncode == 0

    def __call__(self, *args, **kwargs):
        LOGGER.info('Executing %s', self.command)
        kwargs['stdout'] = kwargs.get('stdout', subprocess.PIPE)
        kwargs['stderr'] = kwargs.get('stderr', subprocess.STDOUT)
        self.process = subprocess.Popen(self.args, *args, **kwargs)
        self.stdout, self.stderr = self.process.communicate()
        LOGGER.info('Command %s is done with return code %s', self.command, self.returncode)
        return bool(self)
