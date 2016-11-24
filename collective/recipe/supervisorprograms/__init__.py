# -*- coding: utf-8 -*-
"""Recipe environment."""

PROGRAM_OPTIONS = (
    'priority',
    'id',
    'process_opts',
    'command',
    'args',
    'directory',
    'redirect-stderr',
    'user',
)


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.options = options

        # Do not iterate over self.buildout.iteritems() or we'll initialize every part
        # on the buildout unnecessarily.
        section_names = [k for k in self.buildout if k.endswith('-program')]
        sections = [(k, self.buildout[k]) for k in section_names]

        confs = [self._program_conf_from_section(k, v) for (k, v) in sections]
        self.options['programs'] = '\n'.join(self._program_conf_as_str(c) for c in confs)

    def install(self):
        """Installer"""
        return ()

    def _program_conf_from_section(self, section_name, section_dict):
        conf = {'id': section_name.replace('-program', '')}
        conf.update(section_dict)
        args = conf.get('args') or ''
        args = args.strip()
        if args and (not args.startswith('[')):
            conf['args'] = '[{}]'.format(args)

        process_opts = [(k, v) for (k, v) in conf.iteritems() if k not in PROGRAM_OPTIONS]
        if process_opts:
            conf['process_opts'] = '({})'.format(
                ' '.join('{}={}'.format(k, v) for (k, v) in process_opts)
            )

        return conf

    def _program_conf_as_str(self, conf):
        parts = [(conf.get(k) or '') for k in PROGRAM_OPTIONS]
        parts = [p.strip() for p in parts]
        parts = [p for p in parts if p]
        return ' '.join(parts)

    update = install
