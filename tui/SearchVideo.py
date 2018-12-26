import npyscreen
from models.artist import Artist, Material


class SearchVideo(npyscreen.ActionForm):
    def create(self):
        self.value = None
        self.wgIsVideo = self.add(npyscreen.RoundCheckBox, name="Have video:", value=False)
        self.wgResult = self.add(npyscreen.TitleMultiLine,
                                 name="Result:",
                                 values=[])
        self.add_handlers({
            "^Q": self.exit
        })

    def beforeEditing(self):
        self.name = "Search video"
        self.wgIsVideo.add_handlers({
            "^V": self.unset_video
        })

    def on_ok(self):
            self.wgResult.values = self.parentApp.database.search_videos(self.wgIsVideo.value)

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()

    def unset_video(self, *args, **keywords):
        self.wgIsVideo.value = False

