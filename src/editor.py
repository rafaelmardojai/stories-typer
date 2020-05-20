# editor.py
#
# Copyright 2020 Rafael Mardojai CM
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from fountain import fountain

from gi.repository import Gio, Gtk

from .sourceview import SourceView

from .objects import Scene, Character

@Gtk.Template(resource_path='/com/rafaelmardojai/StoriesTyper/ui/editor.ui')
class Editor(Gtk.Paned):
    __gtype_name__ = 'Editor'

    stack = Gtk.Template.Child()
    scrolled_text = Gtk.Template.Child()
    scrolled_src = Gtk.Template.Child()

    characters_list = Gtk.Template.Child()
    scenes_list = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)

        self.window = window

        self.text = Gtk.TextView()
        self.src = SourceView()

        self.scrolled_text.add_with_viewport(self.text)
        self.scrolled_src.add_with_viewport(self.src)
        self.stack.set_visible_child_name('src')

        self.src.buffer.connect('changed', self.load_objects)

    def load_file(self, file):
        self.src.buffer.set_text(file.read())
        self.set_title(file)

    def get_fountain(self):
        return fountain.Fountain(self.get_src_text())

    def set_title(self, filename):
        fount = self.get_fountain()

        if 'title' in fount.metadata:
            print(fount.metadata['title'])
            self.window.headerbar.set_title(fount.metadata['title'][0])

        self.window.headerbar.set_subtitle(filename)

    def load_objects(self, editor_buffer):
        scenes, characters = self.get_objects(self.get_fountain())

        smodel = Gio.ListStore.new(Scene)
        cmodel = Gio.ListStore.new(Character)

        self.scenes_list.bind_model(smodel, self.name_widget)
        self.characters_list.bind_model(cmodel, self.name_widget)

        for s in scenes:
            scene = Scene(s)
            smodel.append(scene)

        for c in characters:
            character = Character(c)
            cmodel.append(character)

        self.scenes_list.show_all()
        self.characters_list.show_all()

    def get_objects(self, fount):
        scenes = []
        characters = []

        # iterate through elements
        for f in fount.elements:
            if f.element_type == 'Scene Heading' and f.element_text.upper() not in scenes:
                scenes.append(f.element_text.upper())
            elif f.element_type == 'Character' and f.element_text.upper() not in characters:
                characters.append(f.element_text.upper())
        return scenes, characters

    def name_widget(self, scene):
        return Gtk.Label(scene.name)

    def get_src_text(self):
        startIter, endIter = self.src.buffer.get_bounds()
        return self.src.buffer.get_text(startIter, endIter, False)
