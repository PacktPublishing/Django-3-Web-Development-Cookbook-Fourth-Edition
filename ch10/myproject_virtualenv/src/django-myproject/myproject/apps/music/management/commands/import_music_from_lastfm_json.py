from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Imports top songs from last.fm as JSON."
    SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3
    API_URL = "http://ws.audioscrobbler.com/2.0/"

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument("--max_pages", type=int, default=0)

    def handle(self, *args, **options):
        self.verbosity = options.get("verbosity", self.NORMAL)
        self.max_pages = options["max_pages"]
        self.prepare()
        self.main()
        self.finalize()

    def prepare(self):
        from django.conf import settings

        self.imported_counter = 0
        self.skipped_counter = 0
        self.params = {
            "method": "tag.gettoptracks",
            "tag": "indie",
            "api_key": settings.LAST_FM_API_KEY,
            "format": "json",
            "page": 1,
        }

    def main(self):
        import requests

        response = requests.get(self.API_URL, params=self.params)
        if response.status_code != requests.codes.ok:
            self.stderr.write(f"Error connecting to {response.url}")
            return
        response_dict = response.json()
        pages = int(
            response_dict.get("tracks", {}).get("@attr", {}).get("totalPages", 1)
        )

        if self.max_pages > 0:
            pages = min(pages, self.max_pages)

        if self.verbosity >= self.NORMAL:
            self.stdout.write(f"=== Importing {pages} page(s) of tracks ===")

        self.save_page(response_dict)

        for page_number in range(2, pages + 1):
            self.params["page"] = page_number
            response = requests.get(self.API_URL, params=self.params)
            if response.status_code != requests.codes.ok:
                self.stderr.write(f"Error connecting to {response.url}")
                return
            response_dict = response.json()
            self.save_page(response_dict)

    def save_page(self, data):
        import os
        import requests
        from io import BytesIO
        from django.core.files import File
        from ...forms import SongForm

        for track_dict in data.get("tracks", {}).get("track"):
            if not track_dict:
                continue

            song_dict = {
                "artist": track_dict.get("artist", {}).get("name", ""),
                "title": track_dict.get("name", ""),
                "url": track_dict.get("url", ""),
            }
            form = SongForm(data=song_dict)
            if form.is_valid():
                song = form.save()

                image_dict = track_dict.get("image", None)
                if image_dict:
                    image_url = image_dict[1]["#text"]
                    image_response = requests.get(image_url)
                    song.image.save(
                        os.path.basename(image_url),
                        File(BytesIO(image_response.content)),
                    )

                if self.verbosity >= self.NORMAL:
                    self.stdout.write(f" - {song}\n")
                self.imported_counter += 1
            else:
                if self.verbosity >= self.NORMAL:
                    self.stderr.write(
                        f"Errors importing song "
                        f"{song_dict['artist']} - {song_dict['title']}:\n"
                    )
                    self.stderr.write(f"{form.errors.as_json()}\n")
                self.skipped_counter += 1

    def finalize(self):
        if self.verbosity >= self.NORMAL:
            self.stdout.write(f"-------------------------\n")
            self.stdout.write(f"Songs imported: {self.imported_counter}\n")
            self.stdout.write(f"Songs skipped: {self.skipped_counter}\n")
