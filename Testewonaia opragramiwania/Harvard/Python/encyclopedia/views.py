from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from . import util
import random
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):       
    entry = util.get_entry(title)
    if entry:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown2.markdown(entry)
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "Entry not found."
        })

def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        if util.get_entry(title):
            return render(request, "encyclopedia/create.html", {
                "message": "The entry with such title already exists."
            })
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/create.html")

def search(request):
    query = request.GET.get("q")
    entries = util.list_entries()
    if util.get_entry(query):
        return redirect("entry", title=query)
    results = [entry for entry in entries if query.lower() in entry.lower()]
    return render(request, "encyclopedia/search.html", {
        "results": results,
        "query": query
    })

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect("entry", title=random_entry)

def edit(request, title):
    entry = util.get_entry(title)
    if not entry:
        raise Http404("Entry not found.")
    
    if request.method == "POST":
        content = request.POST["content"]
        util.save_entry(title, content)
        return redirect("entry", title=title)
    
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": entry
    })

from django.shortcuts import render

def view_css(request):
    return render(request, 'encyclopedia/wiki_entry.html', {
        'title': 'CSS',
        'content': 'Content of the CSS entry from Wikipedia.'
    })

def view_django(request):
    return render(request, 'encyclopedia/wiki_entry.html', {
        'title': 'Django (web framework)',
        'content': 'Content of the Django entry from Wikipedia.'
    })

def view_git(request):
    return render(request, 'encyclopedia/wiki_entry.html', {
        'title': 'Git',
        'content': 'Content of the Git entry from Wikipedia.'
    })

def view_html(request):
    return render(request, 'encyclopedia/wiki_entry.html', {
        'title': 'HTML',
        'content': 'Content of the HTML entry from Wikipedia.'
    })

def view_python(request):
    return render(request, 'encyclopedia/wiki_entry.html', {
        'title': 'Python (programming language)',
        'content': 'Content of the Python entry from Wikipedia.'
    })


                
