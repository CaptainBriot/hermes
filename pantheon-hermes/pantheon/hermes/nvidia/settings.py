import logging

import pantheon.hermes

LOGGER = logging.getLogger(__name__)


def settings(args):
    cmd = pantheon.hermes.command.Command('nvidia-settings --display :{} {}'.format(pantheon.hermes.DISPLAY, args))
    cmd()

    for line in cmd.stdout.splitlines():
        line = line.decode("utf-8").strip()
        if line:
            LOGGER.debug(line)

    return cmd
