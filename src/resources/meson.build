pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
gnome = import('gnome')

gnome.compile_resources('storiestyper',
  'resources.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

install_data('gtksourceview/fountain.lang',
  install_dir: join_paths(get_option('datadir'), 'gtksourceview-4/language-specs')
)

install_data('gtksourceview/storiestyper-light.xml',
  install_dir: join_paths(get_option('datadir'), 'gtksourceview-4/styles')
)
