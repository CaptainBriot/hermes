import pantheon.hermes


def settings(args):
    args = args.strip()
    cmd = pantheon.hermes.command.Command('nvidia-settings --display :{} {}'.format(pantheon.hermes.DISPLAY, args))
    cmd()
    cmd.log_lines()
    return cmd
