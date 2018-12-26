import psycopg2
import psycopg2.extras
import sys
import random
import string
import datetime
from models.artist import Artist, Material
from models.artwork import Artwork
from models.visitor import Visitor


class Database:
    def __init__(self, host, name):
        self.conn = None
        self.cur = None
        self.host = host
        self.name = name

    def connect(self, user, password):
        try:
            self.conn = psycopg2.connect(host=self.host, dbname=self.name, user=user, password=password)
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except Exception as e:
            print('Error %s' % e)
            sys.exit(1)

    def close(self):
        self.cur.close()
        self.conn.close()

    #  region create table
    def create_artists_table(self):
        materiales = Material.get_all()
        self.cur.execute(f"""DROP TYPE IF EXISTS material CASCADE""")
        self.cur.execute(f"""CREATE TYPE material AS 
                             ENUM ('{materiales[0]}', '{materiales[1]}');""")
        self.cur.execute("DROP TABLE IF EXISTS artists CASCADE")
        self.cur.execute("""CREATE TABLE artists(
                            id SERIAL PRIMARY KEY NOT NULL, 
                            name VARCHAR NOT NULL, 
                            material MATERIAL NOT NULL,
                            country VARCHAR NOT NULL)""")
        self.conn.commit()

    def create_artworks_table(self):
        self.cur.execute("DROP TABLE IF EXISTS artworks CASCADE")
        self.cur.execute("""CREATE TABLE artworks(
                            id SERIAL PRIMARY KEY, 
                            name VARCHAR NOT NULL, 
                            date DATE NOT NULL,
                            style VARCHAR NOT NULL,
                            artistId SERIAL NOT NULL,
                            FOREIGN KEY (artistId) references artists(id) 
                            ON DELETE CASCADE 
                            ON UPDATE CASCADE)""")
        self.conn.commit()

    def create_visitors_table(self):
        self.cur.execute("DROP TABLE IF EXISTS visitors CASCADE")
        self.cur.execute("""CREATE TABLE visitors(
                            id SERIAL PRIMARY KEY, 
                            name VARCHAR NOT NULL, 
                            services VARCHAR[] NOT NULL,
                            artworkId SERIAL NOT NULL)""")
        self.conn.commit()

    def create_visitors_artworks_table(self):
        self.cur.execute("DROP TABLE IF EXISTS visitors_artworks")
        self.cur.execute("""CREATE TABLE visitors_artworks(
                                    visitorId INTEGER,
                                    artworkId INTEGER,
                                    FOREIGN KEY (visitorId) references visitors(id) 
                                    ON DELETE CASCADE
                                    ON UPDATE CASCADE,
                                    FOREIGN KEY (artworkId) references artworks(id)
                                    ON DELETE CASCADE
                                    ON UPDATE CASCADE)""")
        self.conn.commit()
    #  endregion

    #  region create
    def create_new_artist(self, art):
        self.cur.execute(f"""INSERT INTO artists (name, country, material) 
                             VALUES ('{art.name}', '{art.country}', '{art.material}')""")
        self.conn.commit()

    def create_new_artwork(self, artwork):
        self.cur.execute(f"""INSERT INTO artworks (name, date, style, artistId) 
                             VALUES ('{artwork.name}', 
                                     '{artwork.date}', 
                                     '{artwork.style}',
                                     '{artwork.artist_id}')""")
        self.conn.commit()

    def create_new_visitor(self, visitor):
        self.cur.execute(f"""INSERT INTO visitors (name, services) 
                             VALUES ('{visitor.name}', ARRAY{visitor.services})""")
        self.conn.commit()

    #  endregion

    #  region get all
    def get_all_artists(self):
        self.cur.execute("SELECT * FROM artists ORDER BY id")
        return self.cur.fetchall()

    def get_all_artworks(self):
        self.cur.execute("SELECT * FROM artworks ORDER BY id")
        return self.cur.fetchall()

    def get_all_visitors(self):
        self.cur.execute("SELECT * FROM visitors ORDER BY id")
        return self.cur.fetchall()

    #  endregion

    #  region get by name
    def get_artist_by_name(self, name):
        self.cur.execute(f"SELECT * FROM artists WHERE name = '{name}'")
        try:
            return self.cur.fetchall()[0]
        except Exception as e:
            return False

    def get_artwork_by_name(self, name):
        self.cur.execute(f"SELECT * FROM artworks WHERE name = '{name}'")
        return self.cur.fetchall()[0]

    def get_visitor_by_name(self, name):
        self.cur.execute(f"SELECT * FROM visitors WHERE name = '{name}'")
        return self.cur.fetchall()[0]

    #  endregion

    #  region get by id
    def get_artist_by_id(self, id):
        self.cur.execute(f"SELECT * FROM artists WHERE id = '{id}'")
        return self.cur.fetchone()

    def get_artwork_by_id(self, id):
        self.cur.execute(f"SELECT * FROM artworks WHERE id = '{id}'")
        return self.cur.fetchone()

    def get_visitor_by_id(self, id):
        self.cur.execute(f"SELECT * FROM visitors WHERE id = '{id}'")
        return self.cur.fetchone()

    #  endregion

    #  region update by id
    def update_artist_by_id(self, id, new_artist):
        self.cur.execute(f"""UPDATE artists 
                             SET (name, material, country) = ('{new_artist.name}', 
                                                              '{new_artist.material}',
                                                              '{new_artist.country}')
                             WHERE id = {id};""")
        self.conn.commit()

    def update_artwork_by_id(self, id, new_artwork):
        self.cur.execute(f"""UPDATE artworks 
                             SET (name, date, style, artistId) = 
                             ('{new_artwork.name}', 
                              '{new_artwork.date}', 
                              '{new_artwork.style}', 
                              '{new_artwork.artist_id}')
                             WHERE id = {id};""")
        self.conn.commit()

    def update_visitor_by_id(self, id, new_visitor):
        self.cur.execute(f"""UPDATE visitors 
                             SET (name, services) = ('{new_visitor.name}', '{new_visitor.services}')
                             WHERE id = {id};""")
        self.conn.commit()

    #  endregion

    #  region delete by id
    def delete_artist_by_id(self, id):
        self.cur.execute(f"DELETE FROM artists WHERE id = '{id}';")
        self.conn.commit()

    def delete_artwork_by_id(self, id):
        self.cur.execute(f"DELETE FROM visitors_artworks WHERE artworkId = '{id}'")
        self.cur.execute(f"DELETE FROM artworks WHERE id = '{id}';")
        self.conn.commit()

    def delete_visitor_by_id(self, id):
        self.cur.execute(f"DELETE FROM visitors_artworks WHERE visitorId = '{id}'")
        self.cur.execute(f"DELETE FROM visitors WHERE id = '{id}';")
        self.conn.commit()

    #  endregion

    #   region get id by name
    def get_artist_id_by_name(self, name):
        self.cur.execute(f"SELECT id FROM artists WHERE name = '{name}';")
        return self.cur.fetchone()[0]

    def get_artwork_id_by_name(self, name):
        self.cur.execute(f"SELECT id FROM artworks WHERE name = '{name}';")
        return self.cur.fetchone()[0]

    def get_visitor_id_by_name(self, name):
        self.cur.execute(f"SELECT id FROM visitors WHERE name = '{name}';")
        return self.cur.fetchone()[0]
    #   endregion

    #   region generate random data
    def generate_random_artists(self, num: int):
        for i in range(num):
            name = self.__generate_random_string(3, 12)
            material = random.choice(Material.get_all())
            country = self.__generate_random_string(3, 12)
            artist = Artist(name=name, material=material, country=country)
            self.create_new_artist(artist)

    def generate_random_artworks(self, num: int):
        for i in range(num):
            name = self.__generate_random_string(3, 12)
            date = self.__generate_random_date()
            style = self.__generate_random_string(3, 12)
            artist_count = self.get_artists_count()
            artist_id = random.randint(1, artist_count)
            artwork = Artwork(name, date, style, artist_id)
            self.create_new_artwork(artwork)

    def generate_random_visitors(self, num: int):
        for i in range(num):
            name = self.__generate_random_string(3, 12)
            number_of_services = random.randint(1, 4)
            services = []
            for j in range(number_of_services):
                band_name = self.__generate_random_string(3, 12)
                services.append(band_name)
            visitor = Visitor(name, services)
            artworks_count = self.get_artworks_count()
            artwork_id = random.randint(1, artworks_count)
            self.create_new_visitor(visitor, artwork_id)

    #   endregion

    def add_visitor_artwork(self, visitor_id, artwork_id):
        self.cur.execute(f"""INSERT INTO visitors_artworks (visitorId, artworkId) 
                             VALUES ('{visitor_id}', '{artwork_id}')""")
        self.conn.commit()

    def get_visitors_id_by_artwork_id(self, artwork_id):
        self.cur.execute(f"SELECT visitorid FROM visitors_artworks WHERE artworkId = '{artwork_id}'")
        return self.cur.fetchall()

    def get_artworks_id_by_visitor_id(self, visitor_id):
        self.cur.execute(f"SELECT artworkid FROM visitors_artworks WHERE visitorId = '{visitor_id}'")
        return self.cur.fetchall()

    def get_artworks_by_visitor_id(self, visitor_id):
        artworks_id = self.get_artworks_id_by_visitor_id(visitor_id)
        data = []
        for i in artworks_id:
            data.append(self.get_artwork_by_id(i[0]))
        return data

    def update_all_subscriptions_by_visitor_id(self, visitor_id, artworks_id):
        self.cur.execute(f"DELETE FROM visitors_artworks WHERE visitorId = '{visitor_id}'")
        for artwork_id in artworks_id:
            self.cur.execute(f"""INSERT INTO visitors_artworks (visitorId, artworkId) 
                                         VALUES ('{visitor_id}', '{artwork_id}')""")
        self.conn.commit()

    def get_artists_count(self):
        self.cur.execute(f"SELECT COUNT (*) FROM artists;")
        return self.cur.fetchone()

    def get_artworks_count(self):
        self.cur.execute(f"SELECT COUNT (*) FROM artworks;")
        return self.cur.fetchone()[0]

    def get_visitors_count(self):
        self.cur.execute(f"SELECT COUNT (*) FROM visitors;")
        return self.cur.fetchone()[0]

    def get_count_of_an_entity(self, entity):
        entity = entity.lower()
        if entity == "artists":
            return self.get_artists_count()
        elif entity == "artworks":
            return self.get_artworks_count()
        elif entity == "visitors":
            return self.get_visitors_count()
        else:
            return 0

    @staticmethod
    def __generate_random_string(min: int, max: int):
        s = string.ascii_letters
        return ''.join(random.sample(s, random.randint(min, max)))

    @staticmethod
    def __generate_random_date():
        year = random.randint(1950, 2018)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return datetime.datetime(year, month, day)

    def full_text_artist_search(self, word):
        self.cur.execute(f"""SELECT * FROM artists 
                             WHERE to_tsvector(name) @@ plainto_tsquery('{word}')""")
        return self.cur.fetchall()

    def search_material(self, material: Material):
        self.cur.execute(f"""SELECT * FROM artists WHERE material = '{material}'""")
        return self.cur.fetchall()

    def full_text_style_search(self, word):
        self.cur.execute(f"""SELECT * FROM artworks 
                             WHERE id NOT IN (
                                SELECT id FROM artworks 
                                WHERE to_tsvector(style) @@ plainto_tsquery('{word}')
                             )""")
        return self.cur.fetchall()

    def delete_all_artworks_by_artist_id(self, artist_id):
        # self.cur.execute(f"""DELETE FROM artworks_visitors WHERE artworkId in (
        #                         SELECT id FROM artworks WHERE artistId = '{artist_id}'
        #                      );""")
        self.cur.execute(f"DELETE FROM artworks CASCADE WHERE artistId = '{artist_id}';")

        self.conn.commit()

    def delete_all_artist_visitors(self, visitor_id):
        self.cur.execute(f"DELETE FROM visitors CASCADE WHERE artistId = '{artist_id}';")
        self.conn.commit()