#!/usr/bin/env texlua

-- Build script for LaTeX3 "sdaps" files

-- Identify the bundle and module: the module may be empty in the case where
-- there is no subdivision
bundle = ""
module = "sdaps"

-- Location of main directory: use Unix-style path separators
maindir = "."

-- Non-standard settings
cleanfiles   = {"*.pdf", "*.tex", "*.zip"}
packtdszip   = true
unpackdeps   = { }

uploadconfig = {
  author      = "Benjamin Berg",
  email       = "benjamin@sipsolutions.net",
  uploader    = "Benjamin Berg",
  license     = "lppl1.3c",
  summary     = "SDAPS package for questionnaire creation",
  topic       = {"class", "macro-supp", "package-devel", "exam", "pdf-forms", "table-long" },
  ctanPath    = "/macros/latex/contrib/sdaps",
  home        = "https://sdaps.org",
  repository  = "https://github.com/sdaps/sdaps-class/",
  bugtracker  = "https://github.com/sdaps/sdaps-class/issues",
  update      = true,
  version     = "1.9.8",
  description = [[
This module contains LaTeX classes and packages to create machine readable
questionnaires. Metadata is generated for the whole document and it is
possible to process created forms fully automatically using the SDAPS main
program.

Features include:
 * PDF Form generation
 * Advanced array like layouting
   - Can flow over multiple pages and repeats the header automatically
   - Optional document wide alignment of array environments
   - Has complex layout features like rotating the headers to safe space
   - Ability to exchange rows and columns on the fly
 * Different question types:
   - Freeform text
   - Single/multiple choice questions
   - Range questions
 * Layouting questions in rows or columns
 * Possibility to pre-fill questinnaires from LaTeX

Documentation can be found online at https://sdaps.org/class-doc
]]
}

-- Should we set any of the deps variables?
-- typesetdeps = { }
-- checkdeps   = { }
-- unpackdeps  = { }

checkruns = 3

-- No luatex support currently
checkengines = { "pdftex", "xetex" }

demofiles       = { "arraydemo.tex", "testclassic.tex", "test.tex"}
sourcefiles     = { "README", "*.ins", "*.dtx", "sdapscode128.tex", "dict/*.dict" }
installfiles    = { "*.sty", "*.cls", "*.tex", "*.dict" }

kpse.set_program_name ("kpsewhich")
if not release_date then
  l3build = kpse.lookup ("l3build.lua")
  assert (l3build, "l3build is not installed!")
  dofile (kpse.lookup ("l3build.lua"))
end
