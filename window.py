from gi.repository import Gtk, Gdk, GLib
from stationview import StationView
from player import Player


class MainWindow(Gtk.Window):

    playing = True

    def __init__(self):
        Gtk.Window.__init__(self, title="PonyPlayer")

        self.player = Player()

        self.infolabel = Gtk.Label("Pick a station!")
        self.infolabel.set_justify(Gtk.Justification.CENTER)

        self.playpausebutton = Gtk.ToggleButton()
        image = Gtk.Image.new_from_icon_name("media-playback-pause", Gtk.IconSize.LARGE_TOOLBAR)
        self.playpausebutton.set_image(image)
        self.playpausebutton.set_can_focus(False)
        self.playpausebutton.connect("clicked", self.playpause_clicked)
        self.playpausebutton.set_sensitive(False)

        self.volumebutton = Gtk.VolumeButton()
        self.volumebutton.set_value(1.0)
        self.volumebutton.set_can_focus(False)
        self.volumebutton.set_relief(Gtk.ReliefStyle.NORMAL)
        self.volumebutton.connect("value-changed", self.volumebutton_changed)

        self.controlbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.controlbox.pack_start(self.playpausebutton, True, True, 0)
        self.controlbox.pack_end(self.volumebutton, True, True, 0)

        self.topbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.topbox.pack_start(self.infolabel, True, True, 0)
        self.topbox.pack_end(self.controlbox, True, True, 0)

        self.tree = StationView()
        self.tree.get_selection().connect("changed", self.station_selected)
        self.tree.set_can_focus(False)

        self.mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.mainbox.pack_start(self.topbox, False, False, 0)
        self.mainbox.pack_end(self.tree, True, True, 0)
        self.add(self.mainbox)

        GLib.timeout_add_seconds(5, self.reload)

        self.set_icon_from_file("pvllogo.png")

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        Gtk.main()

    def playpause_clicked(self, button):
        self.playing = not self.playing
        if self.playing:
            image = Gtk.Image.new_from_icon_name("media-playback-pause", Gtk.IconSize.LARGE_TOOLBAR)
            self.playpausebutton.set_image(image)
            self.player.start()
        else:
            image = Gtk.Image.new_from_icon_name("media-playback-start", Gtk.IconSize.LARGE_TOOLBAR)
            self.playpausebutton.set_image(image)
            self.player.stop()

    def station_selected(self, selection):
        self.playpausebutton.set_sensitive(True)
        selected = selection.get_selected()

        if selected:
            self.player.change_uri(selected[0][selected[1]][1])

            self.infolabel.set_text(selected[0][selected[1]][2] + "\n" + selected[0][selected[1]][3])

    def volumebutton_changed(self, slider, value):
        self.player.set_volume(value)

    def reload(self):
        self.tree.get_model().reload()
        selected = self.tree.get_selection().get_selected()
        # if selected:
            # self.infolabel.set_text(selected[0][selected[1]][2] + "\n" + selected[0][selected[1]][3])
        return True