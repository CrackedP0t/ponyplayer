from gi.repository import Gtk, GObject
import requests


class StationView(Gtk.TreeView):
    def __init__(self):
        Gtk.TreeView.__init__(self)

        self.store = StationStore()
        self.set_model(self.store)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Station", renderer, text=0)
        self.append_column(column)

        self.set_headers_visible(False)
        self.set_enable_search(False)


class StationStore(Gtk.ListStore):
    apiUrl = "http://ponyvillelive.com/api/nowplaying"
    columns = {"name": 0, "uri": 1, "artist": 2, "song": 3}

    def __init__(self):
        Gtk.ListStore.__init__(self)

        self.set_column_types([GObject.TYPE_STRING, GObject.TYPE_STRING,
                               GObject.TYPE_STRING, GObject.TYPE_STRING])

        self.reload()

    def reload(self):
        response = requests.get(self.apiUrl)
        data = response.json()
        result = data["result"]

        for k in result:
            v = result[k]
            found = False
            for row in self:
                if row[0] == v["station"]["name"]:
                    found = True
                    row[2] = v["current_song"]["artist"]
                    row[3] = v["current_song"]["title"]
                    # if v["status"] != "online" or v["station"]["category"] != "audio":
                    #     row.slice()

            if v["status"] == "online" and v["station"]["category"] == "audio" and not found:
                self.append([v["station"]["name"], v["station"]["stream_url"],
                    v["current_song"]["artist"], v["current_song"]["title"]])
