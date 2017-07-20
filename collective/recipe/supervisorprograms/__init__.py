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
        confs.sort(key=self._program_conf_sort_key)
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

    def _program_conf_sort_key(self, conf):
        options_sort_order = ('priority', 'id', 'command', 'directory')
        return tuple(conf.get(o) for o in options_sort_order)

    update = install


class MultiplierRecipe(object):
    u"""Buildout recipe to create multiple program sections based on an existing one."""

    def __init__(self, buildout, name, options):
        program_section_name = options['program-section']
        count = int(options['count'])
        program_part = buildout[program_section_name]
        base_program_command = program_part['command']

        for new_program_number in xrange(1, count + 1):
            new_program_part = dict(program_part)
            new_program_part['command'] = '{}-{}'.format(base_program_command, new_program_number)
            new_program_section_name = '{}-{}-program'.format(
                program_section_name.replace('-program', ''),
                new_program_number
            )
            buildout[new_program_section_name] = new_program_part

    def install(self):
        return ()

    update = install


class PrinterRecipe(object):
    """Recipe to print its options.

    Useful for testing.
    """

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.options = options

    def install(self):
        print '\n'.join(
            '{} = {}'.format(k, v)
            for (k, v) in sorted(self.options.iteritems())
            if k != 'recipe'
        )
        return ()
