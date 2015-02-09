from gi.repository import Gst


class Player():

    state = Gst.State.PLAYING

    def __init__(self):
        Gst.init(None)

        self.pipeline = Gst.ElementFactory.make("playbin", "player")
        self.pipeline.set_property("volume", 1.0)

        goom = Gst.ElementFactory.make("goom")
        flags = self.pipeline.get_property("flags")

        # print(flags)
        flags |= 0x00000008
        self.pipeline.set_property("flags", flags)

        self.pipeline.set_property("vis-plugin", goom)

        self.pipeline.set_state(Gst.State.NULL)

    def start(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        self.state = Gst.State.PLAYING

    def stop(self):
        self.state = Gst.State.NULL
        self.pipeline.set_state(Gst.State.NULL)

    def change_uri(self, uri):
        oldstate = self.state
        self.stop()
        self.pipeline.set_property("uri", uri)
        self.start()
        self.pipeline.set_state(oldstate)

    def set_volume(self, value):
        self.pipeline.set_property("volume", value)