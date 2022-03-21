# -*- coding: utf-8 -*-

# Copyright (c) 2012-2013 by Christoph Reller. All rights reserved.
#           (c) 2016 by Benjamin Berg

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.

#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY CHRISTOPH RELLER ''AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL CHRISTOPH RELLER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of Christoph Reller.

# Modified for use with SDAPS custom template. Based on sphinxcontrib.sdaps

"""
    sdapstex
    ~~~~~~~~


    Author: Christoph Reller <christoph.reller@gmail.com>
            Benjamin Berg <benjamin.berg@sipsolutions.net>
    Version: 0.0.1
"""

import tempfile
import posixpath
import shutil
import sys
import os
import subprocess
import sphinx
import sphinx.addnodes
import warnings
try:
    from hashlib import sha1 as sha
except ImportError:
    from sha import sha

from docutils import nodes, utils
from docutils.parsers.rst import directives

from sphinx.errors import SphinxError
try:
    from sphinx.util.osutil import ensuredir
except:
    from sphinx.util import ensuredir

try:
    from docutils.parsers.rst import Directive
except:
    from sphinx.util.compat import Directive

class SDAPSExtError(SphinxError):
    category = 'SDAPS extension error'

class sdaps(nodes.Part, nodes.Element):
    pass

sdapstex_block = 0

class SDAPSDirective(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'sdapsclassic'  : directives.flag,
        'metadata'      : directives.flag,
        'preamble'      : directives.unchanged,
    }

    def run(self):
        node = sdaps()
        if not self.content:
            node['caption'] = ''
            node['sdaps'] = '\n'.join(self.arguments)
        else:
            node['sdaps'] = '\n'.join(self.content)
            node['caption'] = '\n'.join(self.arguments)
        node['libs'] = self.options.get('libs', '')
        if 'sdapsclassic' in self.options:
            node['sdapsclassic'] = True
        else:
            node['sdapsclassic'] = False

        if 'metadata' in self.options:
            node['metadata'] = True
        else:
            node['metadata'] = False

        if 'preamble' in self.options:
            node['preamble'] = self.options['preamble']
        else:
            node['preamble'] = ''

        return [node]




def run_engine(texfile, cwd, inputs=None, jobname=None, prexec_hook=None):
    def _preexec_fn():
        if prexec_hook is not None:
            prexec_hook()

        if inputs:
            os.environ['TEXINPUTS'] = ':'.join(['.'] + inputs + [''])

    args = ['pdflatex',]
    if jobname:
        args.append('-jobname=' + jobname)
    args += ['-halt-on-error', '-interaction', 'batchmode', texfile]

    return subprocess.call(args,
                           cwd=cwd,
                           preexec_fn=_preexec_fn)


def compile_target(texfile, cwd, inputs=None):
    run_engine(texfile, cwd, inputs=inputs)
    run_engine(texfile, cwd, inputs=inputs)
    return run_engine(texfile, cwd, inputs=inputs)




TEMPLATE = r'''
\documentclass[english]{scrartcl}

\usepackage{sdapslayout}

\title{Title}
\author{Author}

%(preamble)s

\makeatletter
\ExplSyntaxOn

\def\sdaps_page_end:{}

\def\exampletargettopcmd{
  \pgfsys@markposition{targettop}
}

\def\exampletargetbottomcmd{
  \vbox{\hfill\pgfsys@markposition{targetbottom}}

  \iow_new:N \g_targetinfo
  \iow_open:Nn \g_targetinfo { \c_sys_jobname_str . targetinfo }

  \pgfsys@getposition{pgfpageorigin}{\pageorigin}
  \pgfsys@getposition{targettop}{\tmp}
  \pgfpointadd{\pageorigin}{\tmp}
  \pgfgetlastxy{\tmpx}{\tmpy}

  \iow_shipout_x:Nx \g_targetinfo {\tmpx, \tmpy}

  \pgfsys@getposition{targetbottom}{\tmp}
  \pgfpointadd{\pageorigin}{\tmp}
  \pgfgetlastxy{\tmpx}{\tmpy}

  \iow_shipout_x:Nx \g_targetinfo {\tmpx, \tmpy}
  \iow_shipout_x:Nx \g_targetinfo {\the\paperwidth, \the\paperheight}
}
\ExplSyntaxOff
\makeatother


\begin{document}

\exampletargettopcmd

%(target)s

\exampletargetbottomcmd

\end{document}'''

TEMPLATE_SDAPSCLASSIC = r'''
\documentclass[english]{sdapsclassic}

\title{Title}
\author{Author}

%(preamble)s

\makeatletter
\ExplSyntaxOn

\def\sdaps_page_end:{}

\def\exampletargettopcmd{
  \pgfsys@markposition{targettop}
}

\def\exampletargetbottomcmd{
  \vbox{\hfill\pgfsys@markposition{targetbottom}}

  \iow_new:N \g_targetinfo
  \iow_open:Nn \g_targetinfo { \c_sys_jobname_str . targetinfo }

  \pgfsys@getposition{pgfpageorigin}{\pageorigin}
  \pgfsys@getposition{targettop}{\tmp}
  \pgfpointadd{\pageorigin}{\tmp}
  \pgfgetlastxy{\tmpx}{\tmpy}

  \iow_shipout_x:Nx \g_targetinfo {\tmpx, \tmpy}

  \pgfsys@getposition{targetbottom}{\tmp}
  \pgfpointadd{\pageorigin}{\tmp}
  \pgfgetlastxy{\tmpx}{\tmpy}

  \iow_shipout_x:Nx \g_targetinfo {\tmpx, \tmpy}
  \iow_shipout_x:Nx \g_targetinfo {\the\paperwidth, \the\paperheight}
}

\ExplSyntaxOff
\makeatother


\begin{document}
\begin{questionnaire}

\beginpgfgraphicnamed{target}

\exampletargettopcmd

%(target)s

\exampletargetbottomcmd

\end{questionnaire}
\end{document}'''



def render_sdaps(self, node):
    code = node['sdaps']
    hashkey = code.encode('utf-8')
    hashkey += node['preamble'].encode('utf-8')
    if node['sdapsclassic']:
        hashkey += b'sdapsclassic'
    if node['metadata']:
        hashkey += b'metadata'

    fname = 'sdaps-%s.svg' % (sha(hashkey).hexdigest())
    relfn = posixpath.join(self.builder.imgpath, fname)
    outfn = os.path.join(self.builder.outdir, '_images', fname)

    if os.path.isfile(outfn):
        return relfn, 'Compile was not started as output exists'

#    if hasattr(self.builder, '_sdaps_warned'):
#        return None, 'Compile was not started due to prior warnings'

    ensuredir(os.path.dirname(outfn))
    curdir = os.getcwd()

    replacements = {
        'target' : code,
        'preamble' : node['preamble'] if 'preamble' in node else ''
    }

    if not node['sdapsclassic']:
        latex = TEMPLATE % replacements
    else:
        latex = TEMPLATE_SDAPSCLASSIC % replacements
    latex = latex.encode('utf-8')

    tempdir = self.builder._sdaps_tempdir = tempfile.mkdtemp(prefix="sphinx-sdapstex-")

    try:
        fd = open(os.path.join(tempdir, 'tmp.tex'), 'wb')
        fd.write(latex)
        fd.close()

        inputs = [ self.builder.config.sdaps_latex_dir, self.builder.config.sdaps_image_dir ]

        res = compile_target('tmp.tex', cwd=tempdir, inputs=inputs)
        if res != 0:
            warnings.warn('An error occurred while compiling the LaTeX document')
            self.builder._sdaps_warned = True
            relfn = None
        else:
            if node['metadata']:
                shutil.copy(os.path.join(tempdir, 'tmp.sdaps'), outfn + '.meta')

            topinfo, bottominfo, paper = open(os.path.join(tempdir, 'tmp.targetinfo')).read().split('\n')[0:3]
            x1, y1 = [float(i[:-2]) * 72.27 / 72 for i in topinfo.split(',')]
            x2, y2 = [float(i[:-2]) * 72.27 / 72 for i in bottominfo.split(',')]
            pw, ph = [float(i[:-2]) * 72.27 / 72 for i in paper.split(',')]
            x = int(x1)
            y = int(ph - y1)
            w = int(x2 - x1 + 1)
            h = int(y1 - y2 + 1)
            assert h > 0, "Maybe the LaTeX document has multiple pages?"

            res = subprocess.call(
                    ['pdftocairo',
                     '-x', str(x), '-y', str(y),
                     '-W', str(w), '-H', str(h),
                     '-paperw', str(w), '-paperh', str(h),
                     '-svg', os.path.join(tempdir, 'tmp.pdf'), outfn])
            if res:
                warnings.warn('SVG conversion failed')
                self.builder._sdaps_warned = True
                return None, 'SVG conversion failed', ''
    finally:
        errlog = open(os.path.join(tempdir, 'tmp.log')).read()
        shutil.rmtree(tempdir)

    return relfn, errlog

def html_visit_sdaps(self,node):
    libs = node['libs']
    libs = libs.replace(' ', '').replace('\t', '').strip(', ')

    try:
        fname, errlog = render_sdaps(self, node)
    except SDAPSExtError as exc:
        info = str(exc)[str(exc).find('!'):-1]
        sm = nodes.system_message(info, type='WARNING', level=2,
                                  backrefs=[], source=node['sdaps'])
        sm.walkabout(self)
        warnings.warn('display latex %r: \n' % node['sdaps'] + str(exc))
        raise nodes.SkipNode

    self.body.append(self.starttag(node, 'div', CLASS='figure'))
    self.body.append(self.starttag(node, 'div', CLASS='tabs'))

    global sdapstex_block
    sdapstex_block += 1
    checked = 'checked' if fname is None else ''
    self.body.append('<input type="radio" id="tab-code-%i" class="tab-code" name="tab-group-%i" %s>' % (sdapstex_block, sdapstex_block, checked))
    self.body.append('<label for="tab-code-%i" class="label-code">Example LaTeX code</label>' % sdapstex_block)

    checked = 'checked' if fname is not None else ''
    self.body.append('<input type="radio" id="tab-rendering-%i" class="tab-rendering" name="tab-group-%i" %s>' % (sdapstex_block, sdapstex_block, checked))
    if fname is not None:
        self.body.append('<label for="tab-rendering-%i" class="label-rendering">Result</label>' % sdapstex_block)
    else:
        self.body.append('<label for="tab-rendering-%i" class="label-rendering">Compile Log</label>' % sdapstex_block)

    if fname:
        metadata = os.path.join(self.builder.outdir, fname + '.meta')
        if os.path.exists(metadata):
            metadata = open(metadata).read()
        else:
            metadata = False
    else:
        metadata = False

    if metadata:
        self.body.append('<input type="radio" id="tab-metadata-%i" class="tab-metadata" name="tab-group-%i">' % (sdapstex_block, sdapstex_block))
        self.body.append('<label for="tab-metadata-%i" class="label-metadata">Metadata</label>' % sdapstex_block)

    self.body.append(self.starttag(node, 'div', CLASS='content-code'))

    highlighted = self.highlighter.highlight_block(
            node['sdaps'], 'latex')

    self.body.append(highlighted)

    if node['preamble']:
        self.body.append('Required code in preamble:')

        highlighted = self.highlighter.highlight_block(
                node['preamble'], 'latex')

        self.body.append(highlighted)

    self.body.append('</div>')


    self.body.append(self.starttag(node, 'div', CLASS='content-rendering'))
    if fname is not None:
        self.body.append('<p>')
        self.body.append('<img src="%s" alt="%s" /></p>\n' %
                         (fname, self.encode(node['sdaps']).strip()))
    else:
        self.body.append(self.starttag(node, 'pre'))
        self.body.append(self.encode(errlog))
        self.body.append('</pre>')
    self.body.append('</div>')

    if metadata:
        self.body.append(self.starttag(node, 'div', CLASS='content-metadata'))
        self.body.append(self.starttag(node, 'pre'))
        self.body.append(self.encode(metadata))
        self.body.append('</pre>')
        self.body.append('</div>')




    self.body.append('</div>')

    if node['caption']:
        self.body.append('<p class="caption">%s</p>' %
                         self.encode(node['caption']).strip())

    self.body.append('</div>')
    raise nodes.SkipNode

#def latex_visit_sdaps(self, node):
#    if node['caption']:
#        latex = '\\begin{figure}[htp]\\centering\\begin{sdapspicture}' + \
#                node['sdaps'] + '\\end{sdapspicture}' + '\\caption{' + \
#                self.encode(node['caption']).strip() + '}\\end{figure}'
#    else:
#        latex = '\\begin{center}\\begin{sdapspicture}' + node['sdaps'] + \
#            '\\end{sdapspicture}\\end{center}'
#    self.body.append(latex)

def depart_sdaps(self,node):
    pass

def setup(app):
    app.add_config_value('sdaps_latex_dir', os.path.abspath('../build/local'), ['html'])
    app.add_config_value('sdaps_image_dir', os.path.abspath('.'), ['html'])

    app.add_node(sdaps,
                 html=(html_visit_sdaps, depart_sdaps),
                 #latex=(latex_visit_sdaps, depart_sdaps)
                 )
    app.add_directive('sdaps', SDAPSDirective)
    app.add_css_file('css/sdapstex.css')
