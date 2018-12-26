import npyscreen
from models.artist import Artist, Material


class SearchMaterial(npyscreen.ActionForm):
    def create(self):
        self.value = None
        self.wgMaterial = self.add(npyscreen.TitleSelectOne,
                                 name="Material:",
                                 values=Material.get_all(),
                                 max_height=5,
                                 value=None)
        self.wgResult = self.add(npyscreen.TitleMultiLine,
                                 name="Result:",
                                 values=[],
                                 max_height=4)
        self.add_handlers({
            "^Q": self.exit
        })

    def beforeEditing(self):
        self.name = "Search material"

    def on_ok(self):
        if len(self.wgMaterial.value) == 0:
            ...
        else:
            material = self.wgMaterial.values[self.wgMaterial.value[0]]
            self.wgResult.values = self.parentApp.database.search_material(material)
        #
        # if self.wgRelease.value:
        #
        #     self.parentApp.switchFormPrevious()
        # else:
        #     # TODO make popup
        #     self.is_error = True


    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()