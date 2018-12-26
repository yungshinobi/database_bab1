import npyscreen


class MainList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(MainList, self).__init__(*args, **keywords)
        self.name = "Main List"

    def display_value(self, vl):
        return "|{:^76}|".format(str(vl))


    def actionHighlighted(self, act_on_this, keypress):
        if self.parent.parentApp.database.get_count_of_an_entity(act_on_this) == 0:
            self.spawn_notify_popup(act_on_this)
        else:
            self.parent.parentApp.switchForm(f"{act_on_this.upper()}LIST")

    def spawn_notify_popup(self, entity):
        message_to_display = f'{entity} is empty. \n\t Do you wanna create some?'
        notify_result = npyscreen.notify_yes_no(message_to_display, title='Info box')
        if notify_result:
            self.parent.parentApp.getForm('ATRISTEDIT').value = None
            self.parent.parentApp.switchForm(f"{entity.upper()[:-1]}EDIT")
        else:
            self.parent.parentApp.switchForm("MAIN")


class MainListDisplay(npyscreen.FormMutt):

    MAIN_WIDGET_CLASS = MainList

    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)
        self.add_handlers({
            "^Q": self.exit
        })

    def beforeEditing(self):
        self.wMain.values = ['Artists', 'Artworks', 'Visitors']
        self.wMain.display()

    def exit(self, *args, **keywords):
        self.parentApp.switchForm(None)
