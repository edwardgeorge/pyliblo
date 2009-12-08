#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup, Extension
from distutils.command.build_scripts import build_scripts
from distutils import util, log
import os, sys


if '--with-pyrex' in sys.argv:
    from Pyrex.Distutils import build_ext
    sys.argv.remove('--with-pyrex')
    compile_source = 'pyrex'
elif '--with-cython' in sys.argv:
    from Cython.Distutils import build_ext
    sys.argv.remove('--with-cython')
    compile_source = 'cython'
else:
    compile_source = ''


class build_scripts_rename(build_scripts):
    def copy_scripts(self):
        build_scripts.copy_scripts(self)
        # remove the .py extension from scripts
        for s in self.scripts:
            f = util.convert_path(s)
            before = os.path.join(self.build_dir, os.path.basename(f))
            after = os.path.splitext(before)[0]
            log.info("renaming %s -> %s" % (before, after))
            os.rename(before, after)


cmdclass = {
    'build_scripts': build_scripts_rename
}

ext_modules = [
    Extension(
        'liblo',
        [compile_source and 'src/liblo.pyx' or 'src/liblo.c'],
        extra_compile_args = [
            '-fno-strict-aliasing',
            '-Werror-implicit-function-declaration',
        ],
        libraries = ['lo']
    )
]

if compile_source:
    cmdclass['build_ext'] = build_ext


setup (
    name = 'pyliblo',
    version = '0.8.1',
    author = 'Dominic Sacre',
    author_email = 'dominic.sacre@gmx.de',
    url = 'http://das.nasophon.de/pyliblo/',
    description = 'Python bindings for the liblo OSC library',
    license = 'LGPL',
    scripts = [
        'scripts/send_osc.py',
        'scripts/dump_osc.py',
    ],
    data_files = [
        ('share/man/man1', [
            'scripts/send_osc.1',
            'scripts/dump_osc.1',
        ]),
    ],
    cmdclass = cmdclass,
    ext_modules = ext_modules
)
