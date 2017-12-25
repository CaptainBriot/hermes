import pantheon.hermes


def _run(command):
    command()
    command.log_lines()
    return command


def settings(args):
    args = args.strip()
    cmd = pantheon.hermes.command.Command('nvidia-settings --display :{} {}'.format(pantheon.hermes.DISPLAY, args))
    return _run(cmd)


def smi(*args):
    query = ','.join([str(arg) for arg in args])
    cmd = pantheon.hermes.command.Command('nvidia-smi --query-gpu={} --format=csv,noheader'.format(query))
    return _run(cmd)
