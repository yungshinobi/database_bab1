import npyscreen
import sys


class VisitorsList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(VisitorsList, self).__init__(*args, **keywords)
        self.name = "Visitors"
        self.add_handlers({
            "^A": self.when_add_record,
            "^D": self.when_delete_record,
            "^R": self.subscribe_to_artwork
        })

    def subscribe_to_artwork(self, *args, **keywords):
        cur_id = self.values[self.cursor_line]["id"]
        self.parent.parentApp.getForm('SUBSCRIBE_TO_ARTWORK').value = cur_id
        self.parent.parentApp.switchForm('SUBSCRIBE_TO_ARTWORK')

    def display_value(self, vl):
        return "{:^3}|{:^15}|{:^26}|{:^30}|".format(str(vl[0]),
                                             str(vl[1]),
                                             str(', '.join(vl[2])),
                                             str(', '.join(vl[4])))

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.getForm('VISITOREDIT').value = act_on_this["id"]
        self.parent.parentApp.switchForm('VISITOREDIT')

    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.getForm('VISITOREDIT').value = None
        self.parent.parentApp.switchForm('VISITOREDIT')

    def when_delete_record(self, *args, **keywords):
        try:
            cur_id = self.values[self.cursor_line]["id"]
            self.parent.parentApp.database.delete_visitor_by_id(cur_id)
        except Exception as e:
            raise(e)
            self.parent.wMain.values = []
            self.parent.wMain.display()
        self.parent.update_list()


class VisitorsListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = VisitorsList

    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)
        self.add_handlers({
            "^Q": self.exit
        })

    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        to_display = []
        visitors = self.parentApp.database.get_all_visitors()
        for visitor in visitors:
            artworks = []
            artworks_id = self.parentApp.database.get_artworks_id_by_visitor_id(visitor["id"])
            for artwork_id in artworks_id:
                artwork = self.parentApp.database.get_artwork_by_id(artwork_id[0])
                artworks.append(artwork["name"])
            visitor.append(artworks)
            to_display.append(visitor)
        self.wMain.values = to_display
        if len(to_display) == 0:
            self.parentApp.switchForm("MAIN")
        self.wMain.display()

    def exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()
