# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Playlist(db.Model):
    """Playlist Model"""
    __tablename__ = 'playlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # Assuming max 100 chars, adjust if needed
    description = db.Column(db.Text, nullable=True) # Text for potentially longer descriptions

    # Relationship to the association object PlaylistSong
    # This defines the 'playlist' side of the one-to-many relationship
    # with the PlaylistSong association table.
    # cascade="all, delete-orphan" ensures that when a Playlist is deleted,
    # its corresponding entries in PlaylistSong are also deleted.
    song_associations = db.relationship('PlaylistSong',
                                        back_populates='playlist',
                                        cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Playlist id={self.id} name={self.name}>'

class Song(db.Model):
    """Song Model"""
    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False) # Assuming max 150 chars
    artist = db.Column(db.String(150), nullable=False) # Assuming max 150 chars

    # Relationship to the association object PlaylistSong
    # This defines the 'song' side of the one-to-many relationship
    # with the PlaylistSong association table.
    playlist_associations = db.relationship('PlaylistSong',
                                            back_populates='song',
                                            cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Song id={self.id} title={self.title} artist={self.artist}>'


class PlaylistSong(db.Model):
    """Association Object Pattern Model for Playlist <-> Song"""
    __tablename__ = 'playlists_songs'

    # Primary key for the association table itself, as per the diagram
    id = db.Column(db.Integer, primary_key=True)

    # Foreign key linking to the playlists table
    # nullable=False ensures every association record links to a playlist
    # ondelete='CASCADE' ensures if a playlist is deleted, these links are removed
    playlist_id = db.Column(db.Integer,
                            db.ForeignKey('playlists.id', ondelete='CASCADE'),
                            nullable=False)

    # Foreign key linking to the songs table
    # nullable=False ensures every association record links to a song
    # ondelete='CASCADE' ensures if a song is deleted, these links are removed
    song_id = db.Column(db.Integer,
                        db.ForeignKey('songs.id', ondelete='CASCADE'),
                        nullable=False)

    # Define relationships back to Playlist and Song models
    # This allows easy navigation, e.g., playlist_song_instance.playlist
    playlist = db.relationship('Playlist', back_populates='song_associations')
    song = db.relationship('Song', back_populates='playlist_associations')

    def __repr__(self):
        return f'<PlaylistSong id={self.id} playlist_id={self.playlist_id} song_id={self.song_id}>'


# Helper function to connect database (optional, often in app.py)
def connect_db(app):
    """Connect the database to the Flask app."""
    db.app = app
    db.init_app(app)