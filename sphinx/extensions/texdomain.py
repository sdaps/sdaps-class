# -*- coding: utf-8 -*-
"""

    The TeX domain.

    :copyright: Copyright 2007-2016 by the Sphinx team, see AUTHORS.
                Copyright 2016 by Benjamin Berg <benjamin@sipsolutions.net>
    :license: BSD, see LICENSE for details.
"""

import re
from sphinx import addnodes
from sphinx.domains import Domain, ObjType
from sphinx.locale import l_, _
from sphinx.directives import ObjectDescription
from sphinx.roles import XRefRole
from sphinx.util.nodes import make_refnode
from sphinx.util.docfields import Field, GroupedField, TypedField
from docutils import nodes


class desc_texenvcontent(nodes.Part, nodes.TextElement):
    """Node for a general parameter list."""

    def astext(self):
        return nodes.TextElement.astext(self)

class desc_texparameterlist(nodes.Part, nodes.Inline, nodes.TextElement):
    """Node for a general parameter list."""
    child_text_separator = ' '

    def astext(self):
        return nodes.TextElement.astext(self)

class desc_texparameter(nodes.Part, nodes.Inline, nodes.TextElement):
    """Node for a single parameter."""

    braces='{}'

    def astext(self):
        if self.braces:
            return self.braces[0] + nodes.TextElement.astext(self) + self.braces[1]
        else:
            return nodes.TextElement.astext(self)


class desc_texoptionalparameter(desc_texparameter):
    """Node for a single optional paramter."""

    braces='[]'

class desc_texfreeparameter(desc_texparameter):
    """Node for a stared command."""

    braces=None


def _pseudo_parse_arglist(signode, arglist):
    """"Parse" a list of TeX arguments.

    Arguments surrounded by brackets instead of braces are considered
    "optional".
    """
    paramlist = desc_texparameterlist()
    have_optional = False
    arguments = arglist
    try:
        while arguments.strip():
            arguments = arguments.strip()

            if arguments[0] == '[':
                closing = ']'
                nodetype = desc_texoptionalparameter
            elif arguments[0] == '{':
                closing = '}'
                nodetype = desc_texparameter
            elif arguments[0] == '*':
                paramlist += desc_texfreeparameter('*', '*')
                arguments = arguments[1:].strip()
                continue
            else:
                raise AssertionError

            # Find closing bracket
            end = arguments.find(closing)
            if end == -1:
                raise AssertionError

            argument = arguments[1:end]
            arguments = arguments[end+1:].strip()

            argument = argument.strip()
            paramlist += nodetype(argument, argument)

    except AssertionError:
        # if there are too few or too many elements on the stack, just give up
        # and treat the whole argument list as one argument, discarding the
        # already partially populated paramlist node
        signode += desc_texparameterlist()
        # Use an addnodes desc_paramter as that won't wrap it into {}
        signode[-1] += addnodes.desc_parameter(arglist, arglist)
    else:
        signode += paramlist


class TeXObject(ObjectDescription):
    """
    Description of a TeX object.
    """
    #: If set to ``True`` this object is callable and a `desc_texparameterlist`
    #: is added
    has_arguments = False

    #: If set to ``True`` this object is an environment
    environment = False

    #: what is displayed right before the documentation entry
    display_prefix = None

    def get_signatures(self):
        # Either a single signature per line, or one starting with \begin
        # and ending with \end again.
        sigs = []

        tmp = self.arguments[0]
        while tmp:
            if tmp.startswith(r'\begin'):
                end = tmp.find(r'\end')
                if end > 0:
                    end = tmp[end:].find('\n')
                    if end > 0:
                        sig = tmp[:end].strip()
                        tmp = tmp[end+1:].strip()
                    else:
                        sig = tmp
                        tmp = None
                else:
                    # Just take the rest
                    sig = tmp
                    tmp = None
            else:
                s = tmp.split('\n', 1)
                if len(s) > 1:
                    tmp = s[1]
                else:
                    tmp = None
                sig = s[0]

            sigs.append(sig)

        # remove backslashes to support (dummy) escapes; helps Vim highlighting
        # [strip_backslash_re.sub(r'\1', sig.strip()) for sig in sigs]
        return sigs

    env_re = r'''
        ^\\begin{(?P<name>[a-zA-Z_@:]+)}
            (?P<args>[^\n]*)\n
            (?P<content>.*)
        \\end{(?P<ename>[a-zA-Z_@:]+)}$'''
    env_re = re.compile(env_re, flags = re.MULTILINE | re.VERBOSE | re.DOTALL)

    macro_re = r'''
        ^(?P<name>\\[a-zA-Z_@:]+)'''
    macro_re = re.compile(macro_re, flags = re.MULTILINE | re.VERBOSE | re.DOTALL)

    def handle_signature(self, sig, signode):
        sig = sig.strip()

        name = None

        if self.environment:
            match = self.env_re.match(sig)

            name = match.group('name')
            assert name == match.group('ename')
            arglist = match.group('args')
            content = match.group('content')

            self.environment = True
        else:
            match = re.match(r'^\\[a-zA-Z_@:]+', sig)
            if match:
                name = match.group()
                arglist = sig[len(name):].strip()
            else:
                name = sig
                arglist = None

        signode['fullname'] = name

        if self.display_prefix:
            signode += addnodes.desc_annotation(self.display_prefix,
                                                self.display_prefix)

        if self.environment:
            signode += addnodes.desc_annotation('\\begin{', '\\begin{')
        signode += addnodes.desc_name(name, name)
        if self.environment:
            signode += addnodes.desc_annotation('}', '}')

        if self.has_arguments:
            if arglist:
                _pseudo_parse_arglist(signode, arglist)

        if self.environment:
            signode += desc_texenvcontent(content, content)

            signode += addnodes.desc_annotation('\\end{', '\\end{')
            signode += addnodes.desc_name(name, name)
            signode += addnodes.desc_annotation('}', '}')

        return name, None

    def add_target_and_index(self, name_obj, sig, signode):
        objectname = self.options.get(
            'object', self.env.ref_context.get('tex:object'))
        fullname = name_obj[0]
        if fullname not in self.state.document.ids:
            signode['names'].append(fullname)
            signode['ids'].append(fullname)
            signode['first'] = not self.names
            self.state.document.note_explicit_target(signode)
            objects = self.env.domaindata['tex']['objects']
            if fullname in objects:
                self.state_machine.reporter.warning(
                    'duplicate object description of %s, ' % fullname +
                    'other instance in ' +
                    self.env.doc2path(objects[fullname][0]),
                    line=self.lineno)
            objects[fullname] = self.env.docname, self.objtype

        indextext = self.get_index_text(objectname, name_obj)
        if indextext:
            indexstr = fullname
            if indexstr.startswith('\\'):
                indexstr = indexstr[1:]
            if indexstr.startswith('sdaps_'):
                indexstr = indexstr[6:]
            if indexstr.startswith('sdaps'):
                indexstr = indexstr[5:]
            self.indexnode['entries'].append(('single', indextext,
                                              fullname, '',
                                              indexstr[0]))

    def get_index_text(self, objectname, name_obj):
        name, obj = name_obj

        if self.objtype == 'macro':
            return _('%s (macro)') % name
        elif self.objtype == 'environ':
            return _('%s (environment)') % name
        elif self.objtype == 'data':
            return _('%s (global variable or constant)') % name
        elif self.objtype == 'attribute':
            return _('%s (%s attribute)') % (name, obj)
        return ''


class TeXMacro(TeXObject):
    """Description of a TeX macro or environment."""
    has_arguments = True

    # Field types: GroupedField, TypedField, Field
    doc_field_types = [
        GroupedField('arguments', label=l_('Arguments'),
                     names=('argument', 'arg', 'parameter', 'param'),
                     can_collapse=True),

        GroupedField('keywordarguments', label=l_('Keyword Arguments'),
                     names=('karg', 'kwarg', 'kparam', 'kwparam'),
                     can_collapse=True),
    ]


class TeXEnvironment(TeXMacro):
    """Like a callable but with a different prefix."""
    has_arguments = True
    environment = True

class TeXXRefRole(XRefRole):
    pass

class TeXDomain(Domain):
    """TeX language domain."""
    name = 'tex'
    label = 'TeX'
    # if you add a new object type make sure to edit TeXObject.get_index_text
    object_types = {
        'macro':     ObjType(l_('macro'),     'macro'),
        'environ':   ObjType(l_('environ'), 'environ'),
        'data':      ObjType(l_('data'),      'data'),
        'attribute': ObjType(l_('attribute'), 'attr'),
    }
    directives = {
        'macro':     TeXMacro,
        'environ':   TeXEnvironment,
        'data':      TeXObject,
        'attribute': TeXObject,
    }
    roles = {
        'macro':   TeXXRefRole(),
        'environ': TeXXRefRole(),
        'data':    TeXXRefRole(),
        'attr':    TeXXRefRole(),
    }
    initial_data = {
        'objects': {},  # fullname -> docname, objtype
    }

    def clear_doc(self, docname):
        for fullname, (fn, _l) in list(self.data['objects'].items()):
            if fn == docname:
                del self.data['objects'][fullname]

    def merge_domaindata(self, docnames, otherdata):
        # XXX check duplicates
        for fullname, (fn, objtype) in otherdata['objects'].items():
            if fn in docnames:
                self.data['objects'][fullname] = (fn, objtype)

    def find_obj(self, env, obj, name, typ, searchorder=0):
        if name[-2:] == '()':
            name = name[:-2]
        objects = self.data['objects']
        newname = None
        if searchorder == 1:
            if obj and obj + '.' + name in objects:
                newname = obj + '.' + name
            else:
                newname = name
        else:
            if name in objects:
                newname = name
            elif obj and obj + '.' + name in objects:
                newname = obj + '.' + name
        return newname, objects.get(newname)

    def resolve_xref(self, env, fromdocname, builder, typ, target, node,
                     contnode):
        objectname = node.get('tex:object')
        searchorder = node.hasattr('refspecific') and 1 or 0
        name, obj = self.find_obj(env, objectname, target, typ, searchorder)
        if not obj:
            return None
        return make_refnode(builder, fromdocname, obj[0],
                            name.replace('$', '_S_'), contnode, name)

    def resolve_any_xref(self, env, fromdocname, builder, target, node,
                         contnode):
        objectname = node.get('tex:object')
        name, obj = self.find_obj(env, objectname, target, None, 1)
        if not obj:
            return []
        return [('tex:' + self.role_for_objtype(obj[1]),
                 make_refnode(builder, fromdocname, obj[0],
                              name.replace('$', '_S_'), contnode, name))]

    def get_objects(self):
        for refname, (docname, type) in list(self.data['objects'].items()):
            yield refname, refname, type, docname, \
                refname.replace('$', '_S_'), 1


def html_visit_desc_texenvcontent(self, node):
    self.body.append('<br/><span class="sig">')

def html_depart_desc_texenvcontent(self, node):
    self.body.append('</span><br/>')

def html_visit_desc_texparameterlist(self, node):
    self.body.append('<span class="sig">')
    self.first_param = 1
    self.optional_param_level = 0
    # How many required parameters are left.
    self.required_params_left = sum([isinstance(c, desc_texparameter)
                                     for c in node.children])
    self.param_separator = node.child_text_separator
    self.body.append(self.param_separator)

def html_depart_desc_texparameterlist(self, node):
    self.body.append('</span>')

def html_visit_desc_texparameter(self, node):
    if node.braces:
        self.body.append('<span class="sig-paren">%s</span>' % node.braces[0])
    if self.first_param:
        self.first_param = 0
    elif not self.required_params_left:
        self.body.append(self.param_separator)
    if self.optional_param_level == 0:
        self.required_params_left -= 1
    if not node.hasattr('noemph'):
        self.body.append('<em>')

def html_depart_desc_texparameter(self, node):
    if not node.hasattr('noemph'):
        self.body.append('</em>')
    if node.braces:
        self.body.append('<span class="sig-paren">%s</span>' % node.braces[1])
    if self.required_params_left:
        self.body.append(self.param_separator)


def setup(app):
    app.domains['tex'] = TeXDomain

    app.add_node(desc_texenvcontent,
                 html=(html_visit_desc_texenvcontent, html_depart_desc_texenvcontent),
                 )

    app.add_node(desc_texparameterlist,
                 html=(html_visit_desc_texparameterlist, html_depart_desc_texparameterlist),
                 )

    app.add_node(desc_texparameter,
                 html=(html_visit_desc_texparameter, html_depart_desc_texparameter),
                 )

    app.add_node(desc_texoptionalparameter,
                 html=(html_visit_desc_texparameter, html_depart_desc_texparameter),
                 )

    app.add_node(desc_texfreeparameter,
                 html=(html_visit_desc_texparameter, html_depart_desc_texparameter),
                 )

