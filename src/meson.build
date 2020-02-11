pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'storiestyper')
gnome = import('gnome')

subdir('resources')

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'storiestyper.in',
  output: 'storiestyper',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

storiestyper_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'editor.py',
  'sourceview.py',
  'about.py',
]

install_data(storiestyper_sources, install_dir: moduledir)
