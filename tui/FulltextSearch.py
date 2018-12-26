import npyscreen
from models.artist import Artist, Material


class FulltextSearch(npyscreen.ActionForm):
    def create(self):
        self.value = None
        self.wgText = self.add(npyscreen.TitleText,
                                 name="Input word:",
                                 value='')
        self.wgResult = self.add(npyscreen.TitleMultiLine,
                                 name="Result:",
                                 values=[],
                                 max_height=4)
        self.add_handlers({
            "^Q": self.exit
        })

    def beforeEditing(self):
        self.name = "Fulltext search"
        self.wgText.value = ''

    def on_ok(self):
        if self.wgText.value == '':
            ...
        else:
            self.wgResult.values = self.parentApp.database.full_text_artist_search(self.wgText.value)


    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()