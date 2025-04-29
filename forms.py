"""Forms for playlist app."""

from wtforms import SelectField
from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory
from models import db, Playlist, Song, PlaylistSong

BaseModelForm = model_form_factory(FlaskForm)
class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

class PlaylistForm(ModelForm):
    """Form for adding playlists."""
    song = SelectField('Add Song', coerce=int)
    class Meta:
        model=Playlist

class SongForm(ModelForm):
    """Form for adding playlists."""
    class Meta:
        model=Song

class NewSongForPlaylistForm(ModelForm):
    class Meta:
        model = PlaylistSong
        include = ['song_id']  # Include only the 'song_id' field

    song_id = SelectField('Song')