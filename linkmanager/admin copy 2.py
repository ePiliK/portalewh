from django import forms
from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from .models import Client, Link
import csv
from io import TextIOWrapper
from decimal import Decimal

from django.contrib.auth.models import User

admin.site.site_header = "WebHero LinkHouse"
admin.site.site_title = "Webhero LinkHouse"
admin.site.index_title = "Benvenuto nell'Admin di WebHero LinkHouse"



class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('client', 'site_link', 'article_link', 'cost', 'za', 'da', 'created_at')
    list_filter = ('client', 'created_at')
    search_fields = ('client__name', 'site_link', 'article_link')
    change_list_template = "admin/link_changelist.html"  # Aggiungi questa riga
    
    # START HIDDEN customer
    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('client', 'site_link', 'article_link', 'cost', 'za', 'da', 'created_at')
        return ('client', 'site_link', 'article_link', 'za', 'da', 'created_at')

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return super().get_list_filter(request) + ('client',)
        return self.list_filter

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Filtra i link in base al cliente associato all'utente
        return qs.filter(client__user=request.user)
        # END
        
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv, name='import_csv'),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES["csv_file"]
                decoded_file = TextIOWrapper(csv_file.file, encoding='utf-8-sig')
                csv_reader = csv.DictReader(decoded_file)
                
                required_fields = ['client', 'site_link', 'article_link', 'cost', 'za', 'da']
                
                # Verifica che tutte le colonne necessarie siano presenti
                if not all(field in csv_reader.fieldnames for field in required_fields):
                    self.message_user(request, "Il file CSV non contiene tutte le colonne necessarie. Assicurati di avere: " + ", ".join(required_fields), level='ERROR')
                    return redirect("..")
                
                for row in csv_reader:
                    try:
                        client, _ = Client.objects.get_or_create(name=row['client'])
                        Link.objects.create(
                            client=client,
                            site_link=row['site_link'],
                            article_link=row['article_link'],
                            cost=Decimal(row['cost']),
                            za=row['za'],
                            da=row['da']
                        )
                    except KeyError as e:
                        self.message_user(request, f"Errore nella riga: campo mancante {str(e)}", level='ERROR')
                        return redirect("..")
                    except Exception as e:
                        self.message_user(request, f"Errore nell'elaborazione della riga: {str(e)}", level='ERROR')
                        return redirect("..")

                self.message_user(request, "I link sono stati importati con successo.")
                return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(request, "admin/csv_form.html", payload)

# Mantieni la registrazione esistente per ClientAdmin
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)