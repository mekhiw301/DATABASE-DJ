from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, Optional
from flask_wtf.file import FileAllowed, FileRequired # For file uploads


# from flask import current_app
# ALLOWED_EXTENSIONS = current_app.config['ALLOWED_EXTENSIONS']


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce widgets variants of
    them within a container element, typically a <ul> or <ol>.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SongForm(FlaskForm):
    """Form for adding/editing songs."""
    title = StringField('Song Title', validators=[DataRequired(), Length(max=150)])
    artist = StringField('Artist', validators=[DataRequired(), Length(max=150)])
    album = StringField('Album (Optional)', validators=[Optional(), Length(max=150)])
    # Ensure you configure ALLOWED_EXTENSIONS in your app config
    song_file = FileField('Audio File', validators=[
        FileRequired(),
        FileAllowed(['mp3', 'wav', 'ogg', 'flac', 'm4a'], 'Audio files only!') # Match ALLOWED_EXTENSIONS in config
    ])
    submit = SubmitField('Upload Song')


class PlaylistForm(FlaskForm):
    """Form for adding playlists."""
    name = StringField('Playlist Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description (Optional)')
    submit = SubmitField('Create Playlist')


class AddSongToPlaylistForm(FlaskForm):
    """
    Form for adding existing songs to an existing playlist.
    Uses a multi-checkbox field.
    """
    # This field will be populated dynamically in the route
    songs = MultiCheckboxField('Select Songs', coerce=int)
    submit = SubmitField('Add Selected Songs')

