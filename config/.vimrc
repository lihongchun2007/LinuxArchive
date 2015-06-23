"Vim Options
"-----------
set ff=unix
set ffs=unix

set history=1000               "remember last n commands
"set mouse=a                    "enable full mouse support in the console
set autoindent                 "don't know
set smartindent                "don't know
set shiftwidth=4               "don't know
set softtabstop=4              "eh?
set expandtab                  "no clue what this does

colorscheme elflord

filetype plugin indent on

set number                     "turn line numbering on
syntax on                      "syntax highlighting on
set ignorecase                 "make searches case-insensitive
"
"
"
"
"Status Bar
"----------
"set ruler                      "turn on status bar
set showmode                   "display the current mode in the status line
set showcmd                    "show partially-typed commands in the status line
set laststatus=2               "always show status line 

"configuration for doxygentoolkit
let g:DoxygenToolkit_briefTag_pre="@Synopsis  "
let g:DoxygenToolkit_paramTag_pre="@Param "
let g:DoxygenToolkit_returnTag="@Returns   "
"let g:DoxygenToolkit_blockHeader="--------------------------------------------------------------------------"
"let g:DoxygenToolkit_blockFooter="----------------------------------------------------------------------------"
let g:DoxygenToolkit_authorName="Li Hongchun"
"let g:DoxygenToolkit_licenseTag="My own license" 


filetype plugin indent on
set grepprg=grep\ -nH\ $*
let g:tex_flavor="latex"
set runtimepath=~/.vim,$VIM/vimfiles,$VIMRUNTIME,$VIM/vimfiles/after,~/.vim/after

