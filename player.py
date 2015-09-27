from gi.repository import Gst, GdkX11, GstVideo

class Player():

    state = Gst.State.PLAYING

    def __init__(self, drawingarea):
        Gst.init(None)

        self.drawingarea = drawingarea

        self.pipeline = Gst.ElementFactory.make("playbin", "player")
        self.pipeline.set_property("volume", 1.0)

        # Enables visualization
        flags = self.pipeline.get_property("flags")
        flags |= 0x00000008
        self.pipeline.set_property("flags", flags)

        goom = Gst.ElementFactory.make("goom")
        self.pipeline.set_property("vis-plugin", goom)

        self.sink = Gst.ElementFactory.make("ximagesink")
        self.pipeline.set_property('video-sink', self.sink)

        self.drawingarea.connect('realize', self.on_drawingarea_realized)

        self.pipeline.set_state(Gst.State.NULL)

    def start(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        self.sink.set_window_handle(self.drawingarea.get_property('window').get_xid())

    def stop(self):
        self.pipeline.set_state(Gst.State.NULL)

    def change_uri(self, uri):
        self.stop()
        self.pipeline.set_property("uri", uri)
        self.start()

    def set_volume(self, value):
        self.pipeline.set_property("volume", value)

    def on_drawingarea_realized(self, sender):
        allocation = self.drawingarea.get_allocation()
        self.drawingarea.set_size_request(allocation.width, allocation.width)

        self.sink.set_window_handle(self.drawingarea.get_property('window').get_xid())
