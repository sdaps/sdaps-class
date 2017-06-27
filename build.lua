#!/usr/bin/env texlua

-- Build script for LaTeX3 "sdaps" files

-- Identify the bundle and module: the module may be empty in the case where
-- there is no subdivision
bundle = "sdaps"
module = "sdaps"

-- Location of main directory: use Unix-style path separators
maindir = "."

-- Need xparse
--checkdeps = {}

checkruns = 3

-- No luatex support currently
checkengines = { "pdftex", "xetex" }

demofiles       = { "arraydemo.tex", "testclassic.tex", "test.tex"}
sourcefiles     = { "*.ins", "*.dtx", "code128.tex" }
installfiles    = { "*.sty", "*.cls", "*.tex" }

kpse.set_program_name ("kpsewhich")
dofile (kpse.lookup ("l3build.lua"))
