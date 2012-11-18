au FileType c,cpp,h,hpp call <SID>ClavimInit()

let s:plugin_path = escape(expand('<sfile>:p:h'), '\')

hi clavimMember  ctermbg=Cyan     ctermfg=Black  guibg=#8CCBEA    guifg=Black
hi clavimError   ctermbg=Red      ctermfg=Black  guibg=Red        guifg=Black

function! s:ClavimInit()
    exe 'pyfile ' . s:plugin_path . '/clavim.py'
    set ut=100 " the time in milliseconds after a keystroke when you want to reparse the AST
    python clavim_init()
    call s:ClavimHighlightMemberExpressions()
    "au CursorHold,CursorHoldI <buffer> call <SID>ClavimHighlightMemberExpressions()
    au InsertChange,InsertEnter,InsertLeave <buffer> call <SID>ClavimHighlightMemberExpressions()
endfunction

function! s:ClavimHighlightMemberExpressions()
    call <SID>ClavimClearHighlights()
    python highlight_expressions()
endfunction

function! s:ClavimClearHighlights()
    syn clear clavimMember
endfunction
