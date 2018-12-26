import npyscreen
from models.visitor import Visitor


class VisitorEdit(npyscreen.ActionForm):
    def create(self):
        self.value = None
        self.wgName = self.add(npyscreen.TitleText, name="Name:")
        self.wgServices = self.add(npyscreen.TitleText, name="Services:")
        self.add_handlers({
            "^Q": self.exit
        })

    def beforeEditing(self):
        if self.value:
            visitor = self.parentApp.database.get_visitor_by_id(self.value)
            self.name = "Edit"
            self.record_id = visitor["id"]
            self.wgName.value = visitor["name"]
            self.wgServices.value = ','.join(map(str, visitor["services"]))
            # f = open("log.txt", "w")
            # f.write(f'record : {record}')
        else:
            self.name = "New Visitor"
            self.record_id = ''
            self.wgName.value = ''
            self.wgServices.value = ''

    def on_ok(self):
        visitor = Visitor(self.wgName.value, self.wgServices.value.split(','))
        if self.record_id: # We are editing an existing record
            self.parentApp.database.update_visitor_by_id(self.record_id, visitor)
        else: # We are adding a new record.
            self.parentApp.database.create_new_visitor(visitor)
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()