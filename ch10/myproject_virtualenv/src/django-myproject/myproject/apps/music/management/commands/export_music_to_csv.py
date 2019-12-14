from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Exports music to a local CSV file."
    SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("file_path",
                            nargs=1,
                            type=str)

    def handle(self, *args, **options):
        self.verbosity = options.get("verbosity", self.NORMAL)
        self.file_path = options["file_path"][0]  # first file path provided
        self.prepare()
        self.main()
        self.finalize()

    def prepare(self):
        self.counter = 0

    def main(self):
        import csv
        from myproject.apps.music.models import Song

        if self.verbosity >= self.NORMAL:
            self.stdout.write("=== Importing movies ===\n")

        with open(self.file_path, mode="w") as f:
            writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for song in Song.objects.all():
                writer.writerow([song.artist, song.title, song.url])
                if self.verbosity >= self.NORMAL:
                    self.stdout.write(f" - {song}\n")
                self.counter += 1

    def finalize(self):
        if self.verbosity >= self.NORMAL:
            self.stdout.write(f"-------------------------\n")
            self.stdout.write(f"Songs exported: {self.counter}\n")
