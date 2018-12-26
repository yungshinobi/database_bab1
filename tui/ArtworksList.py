import npyscreen


class ArtworksList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(ArtworksList, self).__init__(*args, **keywords)
        self.name = "Artworks"
        self.add_handlers({
            "^A": self.when_add_record,
            "^D": self.when_delete_record
        })

    def display_value(self, vl):
        return "{:^3}|{:^18}|{:^12}|{:^14}|{:^5}|{:^20}|".format(str(vl[0]),
                                                                 str(vl[1]),
                                                                 str(vl[2]),
                                                                 str(vl[3]),
                                                                 str(vl[4]),
                                                                 str(vl[5]))

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.getForm('ARTWORKEDIT').value = act_on_this["id"]
        self.parent.parentApp.switchForm('ARTWORKEDIT')

    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.getForm('ARTWORKEDIT').value = None
        self.parent.parentApp.switchForm('ARTWORKEDIT')

    def when_delete_record(self, *args, **keywords):
        try:
            cur_id = self.values[self.cursor_line]["id"]
            self.parent.parentApp.database.delete_artwork_by_id(cur_id)
        except Exception as e:
            self.parent.wMain.values = []
            self.parent.wMain.display()
        self.parent.update_list()


class ArtworksListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = ArtworksList

    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)
        self.add_handlers({
            "^Q": self.exit
        })

    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        artworks = self.parentApp.database.get_all_artworks()
        # raise(Exception(artworks))
        to_display = []
        for artwork in artworks:
            author = self.parentApp.database.get_artist_by_id(artwork["artistid"])
            artwork.append(author["name"])
            to_display.append(artwork)
        self.wMain.values = to_display
        if len(to_display) == 0:
            self.parentApp.switchForm("MAIN")
        self.wMain.display()

    def exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()
