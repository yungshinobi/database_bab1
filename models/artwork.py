class Artwork:
    def __init__(self, name, date, style, artist_id):
        self.name = name
        self.date = date
        self.style = style
        self.artist_id = artist_id

    def print(self):
        print(f'Artwork name : {self.name}')
        print(f'Artwork date : {self.date}')
        print(f'Artwork style : {self.style}')
        print(f'Artwork artist_id : {self.artist_id}')
