from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as tr
from task_manager.labels.forms import CreateLabelForm, ShowLabelsForm, UpdateLabelForm
from django.shortcuts import render, redirect
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


class LabelsView(TemplateView):

    def get(self, request, *args, **kwargs):
        form = ShowLabelsForm()
        context = {
                'labels': Label.objects.all().order_by('id'),
                'form': form
            }
        return render(request, 'labels.html', context)


class LabelCreateView(CreateView):

    def get(self, request, *args, **kwargs):
        form = CreateLabelForm()
        return render(request, 'labels/create_label.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CreateLabelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, tr('Метка успешно создана'))
            return redirect('home')
        else:
            return render(request, 'labels/create_label.html', {'form': form})


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = UpdateLabelForm
    template_name = 'labels/update_label.html'
    success_url = reverse_lazy('labels')
    success_message = tr('Метка успешно изменена')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class LabelDeleteView(DeleteView):

    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        context = {}
        label = Label.objects.get(id=label_id)
        context['label'] = label
        return render(request, 'labels/delete_label.html', context)

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        label = Label.objects.get(id=label_id)  # retrieve a label from db
        if Task.objects.filter(labels=label):
            messages.error(
                self.request,
                tr('Невозможно удалить метку, потому что она используется')
            )
            return redirect('labels')
        label.delete()
        messages.info(request, tr('Метка успешно удалёна'))
        return redirect('labels')
