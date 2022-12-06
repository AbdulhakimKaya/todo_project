from django.shortcuts import render, redirect
from .models import Todos
from .forms import ListForms
from django.contrib import messages


# Create your views here.
def index(request):
    if request.method == "POST":
        form = ListForms(request.POST or None)
        if form.is_valid:
            form.save()
            todo_list = Todos.objects.all()
            return render(request, "todo_app/index.html", {"todo_list": todo_list})
    else:
        todo_list = Todos.objects.all()
        return render(request, "todo_app/index.html", {"todo_list": todo_list})


def about(request):
    return render(request, "todo_app/about.html")


def create(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        form = ListForms(request.POST or None)
        if form.is_valid:
            if len(title) > 100:
                messages.info(request, 'Başlık 100 karakterden fazla olamaz')
                return redirect('create')
            elif len(description) > 1000:
                messages.info(request, 'Açıklama 1000 karakterden fazla olamaz')
                return redirect('create')
            else:
                form.save()
                todo_list = Todos.objects.all()
                return render(request, "todo_app/create.html", {"todo_list": todo_list})

    else:
        todo_list = Todos.objects.all()
        return render(request, "todo_app/create.html", {"todo_list": todo_list})


def delete(request, Todos_id):
    todo = Todos.objects.get(pk=Todos_id)
    todo.delete()
    return redirect("index")


def yes_finish(request, Todos_id):
    todo = Todos.objects.get(pk=Todos_id)
    todo.finished = False
    todo.save()
    return redirect("index")


def no_finish(request, Todos_id):
    todo = Todos.objects.get(pk=Todos_id)
    todo.finished = True
    todo.save()
    return redirect("index")


def update(request, Todos_id):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        todo_list = Todos.objects.get(pk=Todos_id)
        form = ListForms(request.POST or None, instance=todo_list)
        if form.is_valid:
            if len(title) > 100:
                messages.info(request, 'Başlık 100 karakterden fazla olamaz')
                return redirect('update')
            elif len(description) > 1000:
                messages.info(request, 'Açıklama 1000 karakterden fazla olamaz')
                return redirect('update')
            else:
                form.save()
                return redirect("index")

    else:
        todo_list = Todos.objects.get(pk=Todos_id)
        return render(request, "todo_app/update.html", {'todo_list': todo_list})
