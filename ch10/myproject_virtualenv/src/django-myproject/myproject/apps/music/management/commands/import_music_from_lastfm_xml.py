from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Imports top songs from last.fm as XML."
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
            "format": "xml",
        }

    def main(self):
        import requests
        from defusedxml import ElementTree

        response = requests.get(self.API_URL, params=self.params)
        if response.status_code != requests.codes.ok:
            self.stderr.write(f"Error connecting to {response.url}")
            return
        root = ElementTree.fromstring(response.content)

        pages = int(root.find("tracks").attrib.get("totalPages", 1))
        if self.max_pages > 0:
            pages = min(pages, self.max_pages)

        if self.verbosity >= self.NORMAL:
            self.stdout.write(f"=== Importing {pages} page(s) of songs ===")

        self.save_page(root)

        for page_number in range(2, pages + 1):
            self.params["page"] = page_number
            response = requests.get(self.API_URL, params=self.params)
            if response.status_code != requests.codes.ok:
                self.stderr.write(f"Error connecting to {response.url}")
                return
            root = ElementTree.fromstring(response.content)
            self.save_page(root)

    def save_page(self, root):
        import os
        import requests
        from io import BytesIO
        from django.core.files import File
        from ...forms import SongForm

        for track_node in root.findall("tracks/track"):
            if not track_node:
                continue

            song_dict = {
                "artist": track_node.find("artist/name").text,
                "title": track_node.find("name").text,
                "url": track_node.find("url").text,
            }
            form = SongForm(data=song_dict)
            if form.is_valid():
                song = form.save()

                image_node = track_node.find("image[@size='medium']")
                if image_node is not None:
                    image_url = image_node.text
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
