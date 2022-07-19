""" sets
set autoindent
set autoread
set cmdheight=1
set colorcolumn=80
set completeopt+=noinsert
set completeopt-=preview
set encoding=utf-8
set fileformats=unix,dos,mac
" set foldmethod=indent
set hidden
set history=500
set hlsearch
set ignorecase
set incsearch
set laststatus=2
set list
set listchars=tab:>-,trail:~,extends:>,precedes:<
set mouse=a
set nobackup
set nocompatible
set noexpandtab
set noswapfile
set nowrap
set nowritebackup
set number
set ruler
set scrolloff=5
set shiftwidth=4
set shortmess+=c
set showcmd
set showmatch
set showmode
set sidescroll=1
set sidescrolloff=15
set signcolumn=number
set smartindent
set splitbelow
set splitright
set tabstop=4
set termencoding=utf-8
set updatetime=300
set virtualedit=onemore

""" auto background
" let curtime = fmod(localtime()/3600+8, 24)
" if curtime >= 6 && curtime < 18
"     set background=light
" else
"     set background=dark
" endif

""" switchers
filetype on
filetype plugin on
filetype indent on
syntax on

""" maps
let g:mapleader="\<space>"
nnoremap <leader>q :q<CR>
nnoremap <leader>Q :q!<CR>
nnoremap <leader>w :w<CR>
vnoremap <C-c> "+y
vnoremap <C-x> "+d
vnoremap <C-v> "+p
nnoremap <C-v> "+P
inoremap <C-v> <C-r>+
inoremap <C-u> <C-v>u
nnoremap U <C-r>
noremap  gh ^
noremap  gl $
noremap  gj <C-d>
noremap  gk <C-u>
inoremap jj <ESC>
inoremap JJ <ESC>
nnoremap gp :bp<CR>
nnoremap gn :bn<CR>
nnoremap gx :bd<CR>
nnoremap g, <C-o>
nnoremap g. <C-i>

""" load plugins config
let nvim_dir = $HOME."/.local/share/nvim/site/pack/autostart/start"
for node in split(system("cd ".nvim_dir." && ls -d *"))
	let script_path = nvim_dir."/".node.".vim"
	if filereadable(script_path)
		exec "source ".script_path
	endif
endfor

function TurnOffCaps()  
	let capsState = matchstr(system('xset -q'), '00: Caps Lock:\s\+\zs\(on\|off\)\ze')
	if capsState == 'on'
		silent! execute ':!xdotool key Caps_Lock'
	endif
endfunction
autocmd InsertLeave * call TurnOffCaps()

