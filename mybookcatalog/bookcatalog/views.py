from django.shortcuts import redirect, render
from .models import Book
from .forms import BookForm 
from django.http import JsonResponse
from pymongo import MongoClient

def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookcatalog/book_list.html', {'books': books})

def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookcatalog/book_form.html', {'form': form})

def search(request):
    query = request.GET.get('q', '')
    client = MongoClient('mongodb://localhost:27017/')
    db = client.BookCatalog
    collection = db.bookcatalog_book

    if query:
        search_results = collection.find({'$text': {'$search': query}})
        results = [
            {
                'title': doc['title'],
                'author': doc['author'],
                'description': doc['description'],
                'publish_date': doc['publish_date'],
                'cover_image': doc.get('cover_image') 
            } 
            for doc in search_results
        ]
    else:
        results = []
        
    # print(results)
    client.close()
    return JsonResponse(results, safe=False)
