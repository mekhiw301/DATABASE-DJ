import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename

from config import Config
from models import db, connect_db, Playlist, Song
from forms import SongForm, PlaylistForm, AddSongToPlaylistForm

app = Flask(__name__)
app.config.from_object(Config)

csrf = CSRFProtect(app) # Enable CSRF protection
connect_db(app) # Connect SQLAlchemy

# --- Helper Function ---
def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# --- Routes ---

@app.route('/')
def homepage():
    """Show homepage: Lists playlists."""
    playlists = Playlist.query.order_by(Playlist.name).all()
    return render_template('index.html', playlists=playlists)

# === Playlist Routes ===

@app.route('/playlists')
def list_playlists():
    """Show list of all playlists."""
    playlists = Playlist.query.order_by(Playlist.name).all()
    return render_template('playlists.html', playlists=playlists)

@app.route('/playlists/new', methods=["GET", "POST"])
def add_playlist():
    """Handle add playlist form."""
    form = PlaylistForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data

        # Check if playlist name already exists
        existing_playlist = Playlist.query.filter_by(name=name).first()
        if existing_playlist:
            flash(f"Playlist '{name}' already exists.", "warning")
            return render_template('playlist_form.html', form=form)

        new_playlist = Playlist(name=name, description=description)
        db.session.add(new_playlist)
        try:
            db.session.commit()
            flash(f"Playlist '{name}' created successfully!", "success")
            return redirect(url_for('show_playlist', playlist_id=new_playlist.id))
        except Exception as e:
            db.session.rollback()
            flash(f"Error creating playlist: {e}", "danger")
            # Log the error e for debugging
            print(f"DB Error: {e}")

    return render_template('playlist_form.html', form=form)

@app.route('/playlists/<int:playlist_id>')
def show_playlist(playlist_id):
    """Show details of a specific playlist and its songs."""
    playlist = Playlist.query.get_or_404(playlist_id)
    # Example using the dynamic loader if configured: playlist.songs.all()
    # Otherwise, playlist.songs should work directly if lazy='select' (default) or similar
    return render_template('playlist_detail.html', playlist=playlist)

# === Song Routes ===

@app.route('/songs')
def list_songs():
    """Show list of all songs."""
    songs = Song.query.order_by(Song.artist, Song.title).all()
    return render_template('songs.html', songs=songs)


@app.route('/songs/upload', methods=["GET", "POST"])
def upload_song():
    """Handle song upload form."""
    form = SongForm()

    if form.validate_on_submit():
        file = form.song_file.data
        title = form.title.data
        artist = form.artist.data
        album = form.album.data

        if file and allowed_file(file.filename):
            # Prevent directory traversal and create safe filename
            filename = secure_filename(f"{artist}_{title}_{file.filename}")
            # Construct full path
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Check if file with this path already exists in DB (or just on disk)
            if Song.query.filter_by(file_path=filename).first() or os.path.exists(filepath):
                 flash(f"A file for '{title}' by {artist} might already exist. Please check.", "warning")
                 return render_template('song_form.html', form=form)

            try:
                file.save(filepath) # Save the uploaded file

                new_song = Song(
                    title=title,
                    artist=artist,
                    album=album,
                    file_path=filename # Store relative path/filename
                )
                db.session.add(new_song)
                db.session.commit()

                flash(f"Song '{title}' by {artist} uploaded successfully!", "success")
                return redirect(url_for('list_songs'))

            except Exception as e:
                db.session.rollback()
                # Consider removing the partially saved file if save succeeded but db failed
                # if os.path.exists(filepath):
                #     os.remove(filepath)
                flash(f"Error uploading song: {e}", "danger")
                 # Log the error e for debugging
                print(f"Upload/DB Error: {e}")

        else:
            # This case might be caught by FileAllowed validator, but good practice
            flash("Invalid file type or no file selected.", "warning")

    # GET request or validation failed
    return render_template('song_form.html', form=form)


# Route to serve uploaded files (Needed for playback)
@app.route('/uploads/<filename>')
def serve_uploaded_file(filename):
    """Serve files from the upload folder."""
    # IMPORTANT: Add security checks here in a real app if needed
    # (e.g., check if user is logged in and allowed to access this file)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# === Add Song to Playlist Route ===

@app.route('/playlists/<int:playlist_id>/add-song', methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Show form to add songs to a specific playlist."""
    playlist = Playlist.query.get_or_404(playlist_id)
    form = AddSongToPlaylistForm()

    # Get songs already in the playlist to potentially exclude them or mark them
    current_song_ids = {song.id for song in playlist.songs}

    # Populate the choices for the form dynamically
    # Exclude songs already in the playlist from the choices
    available_songs = Song.query.filter(Song.id.notin_(current_song_ids)).order_by(Song.artist, Song.title).all()
    form.songs.choices = [(s.id, f"{s.artist} - {s.title}") for s in available_songs]

    if form.validate_on_submit():
        selected_song_ids = form.songs.data # List of IDs from checkboxes

        for song_id in selected_song_ids:
            song = Song.query.get(song_id)
            if song:
                # Check again if it's somehow already added (robustness)
                if song not in playlist.songs:
                    playlist.songs.append(song)
            else:
                flash(f"Song with ID {song_id} not found.", "warning") # Should not happen with coerce=int

        try:
            db.session.commit()
            flash(f"Selected songs added to '{playlist.name}'.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding songs: {e}", "danger")
            print(f"DB Error adding songs: {e}")

        return redirect(url_for('show_playlist', playlist_id=playlist_id))

    # GET request
    return render_template('add_song_to_playlist_form.html', playlist=playlist, form=form)

# === Error Handlers (Optional but Recommended) ===
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
     # Log the error e
    return render_template('500.html'), 500


# === Main Execution ===
if __name__ == '__main__':
    # Create tables if they don't exist (simple way for development)
    # In production, use migrations (Flask-Migrate)
    with app.app_context():
        db.create_all()
    app.run(debug=True) # Turn off debug in production!