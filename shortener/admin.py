from django.contrib import admin

from shortener.models import Link, Client


class LinkAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'shortened', )


admin.site.register(Link, LinkAdmin)
admin.site.register(Client)
