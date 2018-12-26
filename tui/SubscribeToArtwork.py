import npyscreen
from models.visitor import Visitor


class SubscribeToArtwork(npyscreen.ActionForm):
    def create(self):
        self.value = None
        # self.wgText = self.add(npyscreen.TitleText)
        self.wgArtworks = self.add(npyscreen.TitleMultiSelect, name="Artwork:", max_height=4)
        self.add_handlers({
            "^Q": self.exit
        })

    def beforeEditing(self):
        self.wgArtworks.add_handlers({
            "^D": self.unset_select
        })
        self.wgArtworks.values = self.parentApp.database.get_all_artworks()
        subscribed = self.parentApp.database.get_artworks_by_visitor_id(self.value)

        values = []
        for artwork in subscribed:
            index = subscribed.index(artwork)
            if index != -1:
                values.append(index)

        self.wgArtworks.value = values


    def on_ok(self):
        if len(self.wgArtworks.value) != 0:
            artworks = self.wgArtworks.value
            artworks_id = []
            for artwork in artworks:
                artworks_id.append(self.wgArtworks.values[artwork][0])

            self.parentApp.database.update_all_subscriptions_by_visitor_id(self.value, artworks_id)
        else:
            self.parentApp.database.update_all_subscriptions_by_visitor_id(self.value, [])
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()

    def unset_select(self, *args, **keywords):
        self.wgArtworks.value = []

