from haystack import indexes

from myproject.apps.ideas.models import Idea


class IdeaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)

    def get_model(self):
        return Idea

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.all()

    def prepare_text(self, idea):
        """
        Called for each language / backend
        """
        fields = [idea.translated_title, idea.translated_content]
        fields += [category.translated_title for category in idea.categories.all()]
        return "\n".join(fields)
