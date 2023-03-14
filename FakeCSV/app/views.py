import csv
import os
import uuid
from random import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse_lazy
from faker import Faker

from .forms import *
from .models import *

# Create your views here.


def login(request):
    return render(request, 'login.html')

# Декоратор блокує доступ неаутентифікованим користувачам
@login_required
def schemas(request):
    all_schemas = Schema.objects.all()
    return render(request, 'schemas.html', {'title': 'Schemas', 'schemas': all_schemas})


@login_required
def create_schema(request):
    schema_id = request.session.get('schema_id', None)
    if schema_id is None:  # если объекта нет, то создаем его
        schema = Schema.objects.create(user=request.user)
        request.session['schema_id'] = schema.id  # сохраняем ID объекта в сессии
    else:
        schema = Schema.objects.get(id=schema_id)
    if request.method == 'POST':
        # форма для создания таблицы
        form = SchemaColumnForm(request.POST)
        schemaform = SchemaForm(request.POST)

        if schemaform.is_valid():
            # создаем новый объект модели и заполняем его данными из формы
            schema.title = schemaform.cleaned_data['title']
            schema.column_separator = schemaform.cleaned_data['column_separator']
            schema.string_separator = schemaform.cleaned_data['string_separator']
            schema.save()
            # очищаем сессию
            request.session.flush()
            return redirect('data_sets')
        if form.is_valid():
            # форма создания колонок для таблицы
            schema_id = request.session['schema_id']
            # создаем новый объект модели и заполняем его данными из формы
            new_obj = SchemaColumn(
                column_name=form.cleaned_data['column_name'],
                type=form.cleaned_data['type'],
                order=form.cleaned_data['order'],
                min_number=form.cleaned_data['min_number'],
                max_number=form.cleaned_data['max_number'],
                table=Schema.objects.get(id=schema_id)
            )
            new_obj.save()  # сохраняем объект в базу
            queryset = SchemaColumn.objects.filter(table=schema_id).order_by('order')
            return render(request, 'create_schema.html', {'title': 'Create schema', 'form': form, 'queryset': queryset,
                                                          'schemaform': schemaform})
    else:
        form = SchemaColumnForm()
        schemaform = SchemaForm()
    queryset = SchemaColumn.objects.filter(table=schema).order_by('order')
    return render(request, 'create_schema.html',
                  {'title': 'Create schema', 'form': form, 'queryset': queryset, 'schemaform': schemaform})


@login_required
def data_sets(request, schema_id):
    schema = get_object_or_404(Schema, id=schema_id)
    columns = SchemaColumn.objects.filter(table=schema_id).order_by('order')
    datasets = DataSet.objects.filter(table=schema_id)

    if request.method == 'POST':
        form = DataSetForm(request.POST)
        if form.is_valid():
            rows = form.cleaned_data['rows']
            separator = schema.column_separator
            character = schema.string_separator
            headers = columns.only('column_name')
            types = [str(col.type) for col in columns]

            new_dataset = DataSet.objects.create(
                status='loading',
                table=schema,
                file=generate_csv(schema.title, headers, rows, separator, character, types))
            new_dataset.status = "Ready"
            new_dataset.save()
    else:
        form = DataSetForm()

    return render(request, 'data_sets.html', {'columns': columns, 'title': 'Data sets', 'form': form,
                                              'datasets': datasets})


def generate_csv(filename, fieldnames, num_rows, column_separator=',', string_separator='"', field_types=None):
    # Create a Faker object
    fake = Faker()
    new_filename = filename + str(uuid.uuid4())       #renaming file
    # Open a CSV file for writing
    with open(new_filename, 'w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=column_separator, quotechar=string_separator,
                                quoting=csv.QUOTE_MINIMAL)

        # Write the header row
        writer.writeheader()

        # Write the data rows
        for i in range(num_rows):
            # Generate fake data using the Faker library
            data = {}
            for j, field in enumerate(fieldnames):
                if field_types and len(field_types) > j and field_types[j]:
                    data[field] = getattr(fake, field_types[j])()
                else:
                    data[field] = getattr(fake, field)()

            # Write the data to a CSV row
            writer.writerow(data)
    return new_filename


def delete_item(request, item_id):
    item = get_object_or_404(SchemaColumn, id=item_id)
    item.delete()
    return redirect('new_schema')


def delete_schema(request, schema_id):
    item = get_object_or_404(Schema, id=schema_id)
    item.delete()
    return redirect('schemas')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('schemas')

    def get_context_data(self, **kwargs):
        return {'title': 'Авторизація', 'form': self.form_class}


def logout_user(request):
    logout(request)
    return redirect('login')


def schema_dataset_download(request, dataset_id):
    dataset = get_object_or_404(DataSet, id=dataset_id)
    response = HttpResponse(dataset.file, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={dataset.file}'
    return response

