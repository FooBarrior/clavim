#!/usr/bin/env python

# steps
# 1. load file and contents into a tuple
# 2. pass file contents to libclang to parse an AST
# 3. search for member functions and variables
# 4. return a list of them to vim
# 5. highlight them sons of bitches!
# 6. ???
# 7. profit!!1

import sys
import clang.cindex
import vim


def clavim_init():
    sys.argv[0] = ''
    sys.path.append(vim.eval('s:plugin_path'))
    global index
    index = clang.cindex.Index.create()
    global translationUnits
    translationUnits = {}

def get_current_file():
    file = "\n".join(vim.eval("getline(1, '$')"))
    return (vim.current.buffer.name, file)

def get_current_translation_unit(current_file):
    filename = vim.current.buffer.name
    if filename in translationUnits:
        tu = translationUnits[filename]
        tu.reparse([current_file])
        return tu

    tu = index.parse(filename)

    if tu is None:
        print 'Error: tu is None'
        return None

    translationUnits[filename] = tu
    return tu

def cursorvisit_callback(node, parent, data):
    f = node.extent.start.file
    lib = clang.cindex.conf.lib
    if node.kind != data['kind']:
        return 2
    if f is None:
        return 2

    converted_node = {
        'name': lib.clang_getCursorDisplayName(node),
        'kind': node.kind.name,
        'file': f.name,
        'line': node.location.line,
        'start': node.extent.start.column,
        'end': node.extent.end.column,
    }
    data['nodes'].append(converted_node)
    return 2


def find_cursors(tu, kind):
    callback_data = {
        'nodes': [],
        'kind': kind,
    }

    # visit children
    clang.cindex.conf.lib.clang_visitChildren(
        tu.cursor,
        clang.cindex.callbacks['cursor_visit'](cursorvisit_callback),
        callback_data
    )

    return callback_data['nodes']

def highlight_expressions():
    global cursors
    # find all clang cursors
    tu = get_current_translation_unit(get_current_file)
    MEMBER_REF_EXPR = clang.cindex.CursorKind.MEMBER_REF_EXPR
    cursors = find_cursors(tu, MEMBER_REF_EXPR)

    keys = 'line start end'.split()
    syn_match = r"syn match clavimMember /\%%%sl\%%%sc.*\%%%sc/"
    for x in cursors:
        if x['file'] == vim.current.buffer.name:
            t = tuple(str(x[k]) for k in keys)
            vim.command(syn_match % t)


def main():
    index = clang.cindex.Index.create()
    fname = sys.argv[1]
    tu    = index.parse(fname)
    kind  = clang.cindex.CursorKind.MEMBER_REF_EXPR
    nodes = find_cursors(tu, kind)

    print 'nodes (%s):' % (len(nodes))
    keys = 'name kind file line start end'.split()
    template = ' '.join(['%1s = %%(%1s)s' % k for k in keys])
    for x in nodes:
        print template % x

