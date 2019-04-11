import lyricsgenius
import re
import json
import os


class VerseScraper():
    def __init__(self, client_access_token, verbose=False):
        self.genius = lyricsgenius.Genius(client_access_token)
        if verbose:
            lyricsgenius.verbose = True

    def process_lyrics(self, lyrics, song_name, album, song_artist):
        """Process raw text from Genius API and return a dictionary with verses.
        Will 
        """
        lyric_dict = {}

        # Replace (most) unicode characters with their ASCII equivalent
        lyrics = lyrics.replace("\u200b", "").replace(
            "\u2014", "-").replace("\u2018", "'").replace("\u2019", "'")
        lyrics = lyrics.replace("\u201c", "\"").replace("\u201d", "\"")

        # Use a regular expression to fetch verses, had a few different
        # attempts
        out = re.findall(
            r'\[(?P<Type>.*)(?:\:\s(?P<Artist>.*)|\s(?:[1-9]))\]\n(?P<verse>[^\[]*)[$\n]?',
            lyrics)

        # each match will be of format (Type, Artist, Verse lyrics)
        # Type corresponds to the type of verse (e.g. "Verse", "Chorus",
        # "Hook")
        for match in out:
            lyric_type = match[0]
            if "Verse" in lyric_type:
                # If the artist's name is not included in the match or
                # the provided song artist appears first in the match
                # The second condition handles the case where multiple
                # artists are listed.
                if not match[1] or (
                        song_artist in match[1] and match[1].index(song_artist) == 1):
                    artist = song_artist
                else:
                    artist = match[1].strip()

                # This is literally to make sure Andre 3000 isn't split into two separate entries
                # i.e. some songs have him with an accent over the "e", some do not
                artist = artist.replace("\u00e9", "e")

                # Get the verse and split it into an array by line
                verse = match[2]
                verse = verse.split("\n")
                # remove unnecessary empty strings
                verse = list(filter(None, verse))

                # update our lyric dictionary
                if artist not in lyric_dict:
                    lyric_dict[artist] = {}
                if album not in lyric_dict[artist]:
                    lyric_dict[artist][album] = {}
                if song_name not in lyric_dict[artist][album]:
                    lyric_dict[artist][album][song_name] = []

                lyric_dict[artist][album][song_name].append(verse)

        return lyric_dict

    def merge_lyric_dicts(self, dict1, dict2):
        """Combine two lyric dictionaries without overwriting any values"""
        return_dict = dict1.copy()

        for artist, _ in dict2.items():
            if artist not in return_dict:
                return_dict[artist] = dict2[artist]
            else:
                for album in dict2[artist]:
                    if album not in return_dict[artist]:
                        return_dict[artist][album] = dict2[artist][album]
                    else:
                        for song, lyrics in dict2[artist][album].items():
                            if song not in return_dict[artist][album]:
                                return_dict[artist][album][song] = lyrics
        return return_dict

    def save_verses_to_json(self, lyric_dict, filename="Lyrics"):
        """Write everything in the lyric dictionary to a single JSON file."""
        filename = filename + ".json"

        if os.path.isfile(filename):
            while True:
                res = input(
                    "{} already exists. Overwrite?\n(y/n): ".format(filename)).lower()
                if res == 'y':
                    break
                elif res == 'n':
                    print("Aborting.")
                    return
                else:
                    print("Enter y/n")

        with open(filename, 'w') as lyrics_file:
            json.dump(lyric_dict, lyrics_file, indent=4)
        return

    def save_json_to_folders(self, filename, prefix_folder=None):
        """Save the content of a JSON verses file to multiple text files
        Folder structure is as follows: <prefix_folder>/<artist>/<album>/<song>.txt

        Keyword arguments:
        prefix_folder -- the folder to use as the root directory to save to
        """
        with open(filename) as file:
            lyric_dict = json.load(file)

        if prefix_folder:
            os.makedirs(prefix_folder, exist_ok=True)

        for artist, _ in lyric_dict.items():
            artist_dir = self.make_string_filename_safe(artist)
            if prefix_folder:
                artist_dir = prefix_folder + "/" + \
                    self.make_string_filename_safe(artist)

            os.makedirs(artist_dir, exist_ok=True)
            for album, _ in lyric_dict[artist].items():
                formatted_album = self.make_string_filename_safe(album)
                album_dir = artist_dir + "/" + formatted_album

                os.makedirs(album_dir, exist_ok=True)
                for song, _ in lyric_dict[artist][album].items():
                    formatted_song = self.make_string_filename_safe(song)
                    with open(album_dir + "/" + formatted_song + ".txt", "w") as song_file:
                        for verse in lyric_dict[artist][album][song]:
                            for line in verse:
                                song_file.write("{}\n".format(line))

        return

    def fetch_verses_for_artists(
            self,
            artists,
            max_songs_per_artist=10,
            sort_by="popularity"):
        """Fetch verses for given artists and compile into a dictionary.

        Keyword arguments:
        max_song_per_artist -- number of songs to fetch for each artist
        sort_by -- 'popularity' (default) or 'title'
        """
        lyric_dict = {}
        for artist in artists:
            artist = self.genius.search_artist(
                artist, max_songs=max_songs_per_artist, sort=sort_by)
            for song in artist.songs:

                # If a song doesn't have an album, skip it--album is needed for organizing
                # songs. TODO: potentially handle this case later
                if not song.album:
                    print("no album found for " + song.title)
                    continue
                new_dict = self.process_lyrics(
                    song.lyrics, song.title, song.album, artist.name)
                lyric_dict = self.merge_lyric_dicts(lyric_dict, new_dict)

        return lyric_dict

    def make_string_filename_safe(string):
        """Remove non-alphanumeric characters to make string filename safe."""
        string = string.replace("&", "and")
        return "".join([c for c in string if c.isalpha()
                        or c.isdigit() or c == ' ']).rstrip()
