from django.contrib import admin
from .models import Eleve
from django.utils.text import Truncator


class EleveAdmin(admin.ModelAdmin):
    list_display = ('idul', 'dateCo', 'apercu_clee')
    list_filter = ('idul', 'dateCo',)
    date_hierarchy = 'dateCo'
    ordering = ('dateCo', )
    search_fields = ('idul', 'dateCo')

    def apercu_clee(self, eleve):
        """
        Retourne les 40 premiers caractères de la clée,
        suivi de points de suspension si le texte est plus long.
        """
        return Truncator(eleve.clee_publique_client).chars(40, truncate='...')

    # En-tête de notre colonne
    apercu_clee.short_description = 'Aperçu de la clée publique'


admin.site.register(Eleve, EleveAdmin)
