from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Item


class ItemListView(ListView):
    model = Item
    template_name = 'app/item_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Item.objects.filter(is_recovered=False).order_by('-date_found')
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_found'] = Item.objects.count()
        context['total_recovered'] = Item.objects.filter(is_recovered=True).count()
        return context


class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = 'app/item_detail.html'


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'app/item_form.html'
    fields = ['title', 'description', 'category', 'image', 'location_found', 'date_found']
    success_url = reverse_lazy('my_reports') 

    def form_valid(self, form):
        form.instance.founder = self.request.user
        messages.success(self.request, "Item successfully posted to the portal!")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("CREATE FORM INVALID:", form.errors)
        messages.error(self.request, "Could not post item. Please check the fields.")
        return super().form_invalid(form)


class MyReportsListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'app/my_reports.html'
    context_object_name = 'user_items'

    def get_queryset(self):
        return Item.objects.filter(founder=self.request.user).order_by('-date_found')


@login_required
def mark_as_recovered(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if item.founder == request.user:
        item.is_recovered = True
        item.save()
        messages.success(request, f"Item '{item.title}' marked as recovered!")
    return redirect('my_reports')


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    template_name = 'app/item_form.html'
    fields = ['title', 'description', 'category', 'image', 'location_found', 'date_found']
    success_url = reverse_lazy('my_reports')

    def test_func(self):
        item = self.get_object()
        return self.request.user == item.founder

    def form_valid(self, form):
        messages.success(self.request, "Item updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("UPDATE FORM INVALID:", form.errors)
        return super().form_invalid(form)


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    template_name = 'app/item_confirm_delete.html'
    success_url = reverse_lazy('my_reports')

    def test_func(self):
        item = self.get_object()
        return self.request.user == item.founder
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Item deleted permanently.")
        return super().delete(request, *args, **kwargs)