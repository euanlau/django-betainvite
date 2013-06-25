from django.contrib import admin
from .models import InvitationKey, InvitationUser, WaitingListEntry

class WaitingListEntryAdmin(admin.ModelAdmin):
    list_display = ('email', 'created', 'invited',)
    list_filter = ('created', 'invited')
    date_hierarchy = 'created'
    search_fields = ["email"]

class InvitationKeyAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'from_user', 'date_invited', 'key_expired')

class InvitationUserAdmin(admin.ModelAdmin):
    list_display = ('inviter', 'invitations_remaining')

admin.site.register(WaitingListEntry, WaitingListEntryAdmin)
admin.site.register(InvitationKey, InvitationKeyAdmin)
admin.site.register(InvitationUser, InvitationUserAdmin)
