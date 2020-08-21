from random import choice

from django.http import Http404
from django.shortcuts import render
from markdown2 import Markdown

from . import util


def index(request):
    """List all wiki entries."""
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, entry_title):
    """Display single wiki entry."""
    entry = util.get_entry(entry_title)
    if entry is None:
        raise Http404
    mark_downer = Markdown()
    ctx = {'content': mark_downer.convert(entry), 'title': entry_title}
    return render(request, 'encyclopedia/entry_page.html', context=ctx)


def random_page(request):
    """Display random wiki entry."""
    random_entry = choice(util.list_entries())
    return entry_page(request, random_entry)
