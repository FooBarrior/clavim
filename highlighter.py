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

class Highlighter:
    def __init__(self, filename):
        self.nodes = []
        self.filename = filename
        self.index = clang.cindex.Index.create()
        self.tu = self.index.parse(filename)

def cursorvisit_callback(node, parent, userdata):
    #if node.kind == clang.cindex.CursorKind.MEMBER_REF_EXPR:
    userdata['object'].nodes.append(node)
    return 2


def main():
    highlighter = Highlighter(sys.argv[1])

    userdata = dict()
    userdata['object'] = highlighter
    # visit children
    clang.cindex.Cursor_visit(
        highlighter.tu.cursor,
        clang.cindex.Cursor_visit_callback(cursorvisit_callback),
        userdata)

    print 'nodes (%s):' % (len(highlighter.nodes))
    for x in highlighter.nodes:
        if not x.extent.start.file is None:
            print 'name=%s kind=%s file=%s line=%s col=%s' % (clang.cindex.Cursor_displayname(x), x.kind.name, x.extent.start.file.name, x.location.line, x.location.column)

main()
