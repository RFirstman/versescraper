# Verse Scraper

`versescraper` is a tool that fetches verses and bars for given musicians. It utilizes the Genius API through John W. Miller's [LyricsGenius](https://github.com/johnwmillr/LyricsGenius) package.

I found that the LyricsGenius package worked well for fetching lyrics for an artist, but I found that it did not enable me to retrieve individual verses from those songs. So, I utilized regular expressions and text processing to extract individual verses and their authors from Genius API data.

## Installation

Before installing the python package, you will need a free account and client access token from the [Genius API](http://genius.com/api-clients). The [usage section](#Usage) details how to set up VerseScraper using the token.

Once you have your client access token, install with pip.

```
pip install versescraper
```

## Usage

Create a verses dictionary for given artists.

```python
import versescraper
scraper = versescraper.VerseScraper("your_access_token_goes_here")
verses = scraper.fetch_verses_for_artists(["Outkast", "Kendrick Lamar"])
```

Save the results to a JSON file

```python
scraper.save_verses_to_json(verses, filename="verses")
```