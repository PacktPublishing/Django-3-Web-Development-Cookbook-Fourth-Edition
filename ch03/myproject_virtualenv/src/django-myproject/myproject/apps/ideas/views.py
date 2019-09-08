from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.forms import modelformset_factory

from .forms import IdeaForm, IdeaTranslationsForm
from .models import Idea, IdeaTranslations


class IdeaList(ListView):
    model = Idea


class IdeaDetail(DetailView):
    model = Idea
    context_object_name = "idea"


@login_required
def add_idea(request):
    IdeaTranslationsFormSet = modelformset_factory(
        IdeaTranslations, form=IdeaTranslationsForm, extra=0, can_delete=True
    )
    if request.method == "POST":
        form = IdeaForm(request, data=request.POST, files=request.FILES)
        translations_formset = IdeaTranslationsFormSet(
            queryset=IdeaTranslations.objects.none(),
            data=request.POST,
            files=request.FILES,
            prefix="translations",
            form_kwargs={"request": request},
        )
        if form.is_valid() and translations_formset.is_valid():
            idea = form.save()
            translations = translations_formset.save(commit=False)
            for translation in translations:
                translation.idea = idea
                translation.save()
            translations_formset.save_m2m()
            for translation in translations_formset.deleted_objects:
                translation.delete()
            return redirect("ideas:idea_detail", pk=idea.pk)
    else:
        form = IdeaForm(request)
        translations_formset = IdeaTranslationsFormSet(
            queryset=IdeaTranslations.objects.none(),
            prefix="translations",
            form_kwargs={"request": request},
        )

    context = {"form": form, "translations_formset": translations_formset}
    return render(request, "ideas/idea_form.html", context)


@login_required
def change_idea(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    IdeaTranslationsFormSet = modelformset_factory(
        IdeaTranslations, form=IdeaTranslationsForm, extra=0, can_delete=True
    )
    if request.method == "POST":
        form = IdeaForm(request, data=request.POST, files=request.FILES, instance=idea)
        translations_formset = IdeaTranslationsFormSet(
            queryset=idea.translations.all(),
            data=request.POST,
            files=request.FILES,
            prefix="translations",
            form_kwargs={"request": request},
        )
        if form.is_valid() and translations_formset.is_valid():
            idea = form.save()
            translations = translations_formset.save(commit=False)
            for translation in translations:
                translation.idea = idea
                translation.save()
            translations_formset.save_m2m()
            for translation in translations_formset.deleted_objects:
                translation.delete()
            return redirect("ideas:idea_detail", pk=idea.pk)
    else:
        form = IdeaForm(request, instance=idea)
        translations_formset = IdeaTranslationsFormSet(
            queryset=idea.translations.all(),
            prefix="translations",
            form_kwargs={"request": request},
        )

    context = {"idea": idea, "form": form, "translations_formset": translations_formset}
    return render(request, "ideas/idea_form.html", context)


@login_required
def delete_idea(request, pk):
    import os
    import contextlib

    idea = get_object_or_404(Idea, pk=pk)
    if request.method == "POST":
        if idea.picture:
            with contextlib.suppress(FileNotFoundError):
                os.remove(idea.picture_large.path)
                os.remove(idea.picture_thumbnail.path)
            idea.picture.delete()
        idea.delete()
        return redirect("ideas:idea_list")
    context = {"idea": idea}
    return render(request, "ideas/idea_deleting_confirmation.html", context)
