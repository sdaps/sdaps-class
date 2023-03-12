#!/usr/bin/env texlua

-- Build script for LaTeX3 "sdaps" files

-- Identify the bundle and module: the module may be empty in the case where
-- there is no subdivision
bundle = ""
module = "sdaps"

-- Location of main directory: use Unix-style path separators
maindir = maindir or "."

-- Non-standard settings
cleanfiles   = {"*.pdf", "*.zip"}
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
  version     = "1.9.10",
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

-- Don't typeset anything (in particular documentation)
typesetfiles    = { }
docfiles        = { "README", "sdaps.html", "sphinx/_build/html/" }
demofiles       = { "arraydemo.tex", "testclassic.tex", "test.tex"}
sourcefiles     = { "README", "*.ins", "*.dtx", "sdapscode128.tex", "dict/*.ini" }
installfiles    = { "*.sty", "*.cls", "*.tex", "*.dict" }

kpse.set_program_name ("kpsewhich")
if not release_date then
  l3build = kpse.lookup ("l3build.lua")
  assert (l3build, "l3build is not installed!")
  dofile (l3build)
end

-- I would love to override target_list['unpack'].func, or .post, but that
-- does not work as "install" will call the original unpack
orig_unpack = unpack
unpack = function (names)
  -- first run orignal unpack (as it cleans the directory)
  errorlevel = orig_unpack(names)
  if errorlevel ~=0 then
    return errorlevel
  end

  -- Really, a weblate .dict plugin would make more sense than this
  errorlevel = run('.', './generate-dictionaries.py')
  if errorlevel ~=0 then
    print("Failed to generate dictonaries from translation sources")
  end

  return errorlevel
end
target_list['unpack'].func = unpack

target_list['ctan'].pre = function (names)
  errorlevel = run('.', 'grep -q "Version: ' .. uploadconfig['version']:gsub('%.', '\\.') .. '" README')
  if errorlevel ~=0 then
    print("Version mismatch between README file and build.lua configuration")
    return errorlevel
  end

  -- Seems like the ctan command does not ensure "doc" has been run
  errorlevel = call({ '.' }, "doc")
  if errorlevel ~=0 then
     print("Failed to build documentation (required to build ctan package)")
    return errorlevel
  end

  return errorlevel
end

target_list['doc'].pre = function (names)
  -- Building the sphinx documentation requires having unpacked everything
  errorlevel = call({ '.' }, "unpack")
  if errorlevel ~=0 then
     print("Failed to unpack (required to build documentation)")
    return errorlevel
  end

  -- Only build sphinx documentation, then return
  -- Note that we build the "classic" theme, because matrial generates a huge tarball
  -- And we force a clean rebuild, just to make sure things are correct
  errorlevel = run('.', 'make -C sphinx clean')
  if errorlevel ~=0 then
    return errorlevel
  end
  errorlevel = run('.', 'make -C sphinx html SPHINXOPTS="-D html_theme=classic"')
  -- And remove some unwanted files
  os.remove('sphinx/_build/html/.buildinfo')
  os.remove('sphinx/_build/html/objects.inv')

  return errorlevel
end

target_list['clean'].pre = function (names)
  run('sphinx', 'make clean')
end
