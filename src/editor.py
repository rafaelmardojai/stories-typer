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

from gi.repository import Gtk

from .sourceview import SourceView

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

    def load_file(self, file):
        self.src.buffer.set_text(file.read())
        self.load_scenes()
        self.load_characters()
        self.set_title()

    def get_fountain(self):
        return fountain.Fountain(self.get_src_text())

    def set_title(self):
        fount = self.get_fountain()

        if 'title' in fount.metadata:
            print(fount.metadata['title'])
            self.window.headerbar.set_title(fount.metadata['title'][0])

    def load_scenes(self):
        scenes = self.get_scenes(self.get_fountain())

        for s in scenes:
            item = Gtk.ListBoxRow()
            label = Gtk.Label(s)
            item.add(label)
            self.scenes_list.add(item)

        self.scenes_list.show_all()

    def get_scenes(self, fount):
        scenes = []

        # iterate through elements
        for f in fount.elements:
            if f.element_type == 'Scene Heading' and f.element_text.upper() not in scenes:
                scenes.append(f.element_text.upper())
        return scenes

    def load_characters(self):
        characters = self.get_characters(self.get_fountain())

        for c in characters:
            item = Gtk.ListBoxRow()
            label = Gtk.Label(c)
            item.add(label)
            self.characters_list.add(item)

        self.characters_list.show_all()

    def get_characters(self, fount):
        chars = []

        # iterate through elements
        for f in fount.elements:
            if f.element_type == 'Character' and f.element_text.upper() not in chars:
                chars.append(f.element_text.upper())
        return chars

    def get_src_text(self):
        startIter, endIter = self.src.buffer.get_bounds()
        return self.src.buffer.get_text(startIter, endIter, False)
