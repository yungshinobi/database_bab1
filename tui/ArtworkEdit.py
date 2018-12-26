import npyscreen
import numpy as np
from models.artwork import Artwork


class ArtworkEdit(npyscreen.ActionForm):
    # TODO create quit handlers
    def create(self):
        self.value = None
        self.wgName = self.add(npyscreen.TitleText, name="Name:", value="")
        self.wgStyle = self.add(npyscreen.TitleText, name="Style:", value="")
        self.wgDate = self.add(npyscreen.TitleDateCombo, name="Date:", value="")
        self.wgArtistName = self.add(npyscreen.TitleSelectOne, name="Author:", max_height=4)
        self.is_error = False
        self.add_handlers({
            "^Q": self.exit
        })

    def beforeEditing(self):
        artists = self.parentApp.database.get_all_artists()
        names = list(map(lambda x: x['name'], artists))
        self.wgArtistName.values = names

        if self.value:
            artwork = self.parentApp.database.get_artwork_by_id(self.value)
            art_id = artwork["artistid"]
            artist = self.parentApp.database.get_artist_by_id(art_id)
            self.name = "Edit"
            self.record_id = artwork["id"]
            self.wgName.value = artwork["name"]
            self.wgStyle.value = artwork["style"]
            self.wgDate.value = artwork["date"]
            self.wgArtistName.value = names.index(artist["name"])
        elif self.is_error is True:
            self.is_error = False
            # Try again
        else:
            self.name = "New Artwork"
            self.record_id = None
            self.wgArtistName.value = None
            self.wgName.value = ''
            self.wgStyle.value = ''
            self.wgDate.value = ''

    def on_ok(self):
        if self.wgArtistName.value:
            artist_name = self.wgArtistName.values[self.wgArtistName.value[0]]
            artist = self.parentApp.database.get_artist_by_name(artist_name)
            artwork = Artwork(self.wgName.value,
                              self.wgDate.value,
                              self.wgStyle.value,
                              artist["id"])

            # We are editing an existing record
            if self.record_id is not None:
                self.parentApp.database.update_artwork_by_id(self.record_id, artwork)
            # We are adding a new record
            else:
                self.parentApp.database.create_new_artwork(artwork)
            self.parentApp.switchFormPrevious()
        else:
            # TODO make popup
            self.is_error = True
            self.spawn_notify_popup(self.wgArtistName.value)

    def on_cancel(self):
        self.is_error = False
        self.parentApp.switchFormPrevious()

    def exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()

    def spawn_notify_popup(self, entity):
        message_to_display = f'Please select author'
        notify_result = npyscreen.notify_confirm(message_to_display, title='Error')