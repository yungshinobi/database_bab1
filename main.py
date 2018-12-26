import datetime
import npyscreen

from database.database import Database

from models.artist import Artist, Material
from models.artwork import Artwork
from models.visitor import Visitor

from tui import MainList
from tui import ArtistsList
from tui import ArtistEdit
from tui import ArtworksList
from tui import ArtworkEdit
from tui import VisitorsList
from tui import VisitorEdit
from tui import SubscribeToArtwork
from tui import SearchMaterial
from tui import SearchVideo
from tui import FulltextSearch


class ArtistsDBApp(npyscreen.NPSAppManaged):
    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)
        self.database = Database('127.0.0.1', 'postgres')

    def onStart(self):
        self.database.connect('ulyana', 'volchok')
        self.fill_database()

        self.addForm("MAIN", MainList.MainListDisplay, title='Main menu')
        self.addForm("ARTISTSLIST", ArtistsList.ArtistsListDisplay, title='Artists')
        self.addForm("ARTISTEDIT", ArtistEdit.ArtistEdit)
        self.addForm("ARTWORKSLIST", ArtworksList.ArtworksListDisplay)
        self.addForm("ARTWORKEDIT", ArtworkEdit.ArtworkEdit)
        self.addForm("VISITORSLIST", VisitorsList.VisitorsListDisplay)
        self.addForm("VISITOREDIT", VisitorEdit.VisitorEdit)
        self.addForm("SUBSCRIBE_TO_ARTWORK", SubscribeToArtwork.SubscribeToArtwork)
        self.addForm("SEARCH_MATERIAL", SearchMaterial.SearchMaterial)
        self.addForm("SEARCH_VIDEO", SearchVideo.SearchVideo)
        self.addForm("FULLTEXT_SEARCH", FulltextSearch.FulltextSearch)

    def onCleanExit(self):
        self.database.close()

    def fill_database(self):
        self.database.create_artists_table()
        self.database.create_artworks_table()
        self.database.create_visitors_table()
        self.database.create_visitors_artworks_table()

        artist1 = Artist(name='Vincent van Gogh',
                            material=Material.TRADITIONAL.value,
                            country='Netherlands')
        artist2 = Artist(name='Claude Monet',
                           material=Material.TRADITIONAL.value,
                           country='France')
        artist3 = Artist(name='Ulyanka Khrusch',
                            material=Material.DIGITAL.value,
                            country='Ukraine')
        artist4 = Artist(name='SIMART',
                                 material=Material.DIGITAL.value,
                                 country='Russia')
        artwork1 = Artwork(name='Little boy with lil goats',
                          date=datetime.datetime(year=2017, month=1, day=7),
                          style="paysage",
                          artist_id=4)
        artwork2 = Artwork(name='KVWVI WVRR0R',
                           date=datetime.datetime(year=2018, month=9, day=24),
                           style="portrait",
                           artist_id=3)
        artwork3 = Artwork(name='Starry night',
                           date=datetime.datetime(year=1889, month=6, day=15),
                           style="paysage",
                           artist_id=1)
        visitor1 = Visitor(name='Naruto Uzumaki', services=["vk", "narutowiki"])
        visitor2 = Visitor(name='Sasuke Uchiha', services=["insragram" , "telegram", "vk"])
        visitor3 = Visitor(name='Griz the Bear', services=["insragram" , "telegram"])

        self.database.create_new_artist(artist1)
        self.database.create_new_artist(artist2)
        self.database.create_new_artist(artist3)
        self.database.create_new_artist(artist4)
        # self.database.generate_random_artists(100)

        self.database.create_new_artwork(artwork1)
        self.database.create_new_artwork(artwork2)
        self.database.create_new_artwork(artwork3)

        self.database.create_new_visitor(visitor1)
        self.database.create_new_visitor(visitor2)
        self.database.create_new_visitor(visitor3)

        self.database.add_visitor_artwork(1, 1)
        self.database.add_visitor_artwork(2, 1)
        self.database.add_visitor_artwork(1, 2)

if __name__ == '__main__':

    MyApp = ArtistsDBApp()
    MyApp.run()

