import npyscreen
from models.artist import Artist, Material


class ArtistEdit(npyscreen.ActionForm):
    def create(self):
        self.value = None
        self.wgName = self.add(npyscreen.TitleText, name="Name:")
        self.wgCountry = self.add(npyscreen.TitleText, name="Country:")
        self.wgMaterial = self.add(npyscreen.TitleSelectOne,
                                 name="Material:",
                                 values=Material.get_all())
        self.add_handlers({
            "^Q": self.exit
        })

    def beforeEditing(self):
        self.materiales = Material.get_all()
        if self.value:
            artist = self.parentApp.database.get_artist_by_id(self.value)
            self.name = "Edit"
            self.record_id = artist["id"]
            self.wgName.value = artist["name"]
            self.wgCountry.value = artist["country"]
            self.wgMaterial.value = self.materiales.index(artist["material"])
            # f = open("log.txt", "w")
            # f.write(f'record : {record}')
        else:
            self.name = "New Artsit"
            self.record_id = ''
            self.wgName.value = ''
            self.wgCountry.value = ''
            self.wgMaterial.value = ''

    def on_ok(self):
        material = self.wgMaterial.values[self.wgMaterial.value[0]]
        artist = Artist(self.wgName.value, material, self.wgCountry.value)
        if self.record_id: # We are editing an existing record
            self.parentApp.database.update_artist_by_id(self.record_id, artist)
        else: # We are adding a new record.
            self.parentApp.database.create_new_artist(artist)
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()
