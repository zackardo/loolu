"""
Built-in, globally-available admin actions.
"""

from django import template
from django.core.exceptions import PermissionDenied
from django.contrib.admin import helpers
from django.contrib.admin.util import get_deleted_objects, model_ngettext
from django.shortcuts import render_to_response
from django.utils.encoding import force_unicode
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy, ugettext as _
from google.appengine.ext import db
try:
    set
except NameError:
    from sets import Set as set     # Python 2.3 fallback

def delete_selected(modeladmin, request, queryset):
    """
    Default action which deletes the selected objects.

    This action first displays a confirmation page whichs shows all the
    deleteable objects, or, if the user has no permission one of the related
    childs (foreignkeys), a "permission denied" message.

    Next, it delets all selected objects and redirects back to the change list.
    """
    opts = modeladmin.model._meta
    app_label = opts.app_label

    # Check that the user has delete permission for the actual model
    if not modeladmin.has_delete_permission(request):
        raise PermissionDenied

    # Populate deletable_objects, a data structure of all related objects that
    # will also be deleted.

    # deletable_objects must be a list if we want to use '|unordered_list' in the template
    deletable_objects = []
    perms_needed = set()
    i = 0
    for obj in queryset:
        deletable_objects.append([mark_safe(u'%s: <a href="%s/">%s</a>' % (escape(force_unicode(capfirst(opts.verbose_name))), obj.pk, escape(obj))), []])
        get_deleted_objects(deletable_objects[i], perms_needed, request.user, obj, opts, 1, modeladmin.admin_site, levels_to_root=2)
        i=i+1

    # The user has already confirmed the deletion.
    # Do the deletion and return a None to display the change list view again.
    if request.POST.get('post'):
        if perms_needed:
            raise PermissionDenied
        n = len(queryset)
        if n:
            for obj in queryset:
                obj_display = force_unicode(obj)
                modeladmin.log_deletion(request, obj, obj_display)
            db.delete(queryset)
            modeladmin.message_user(request, _("Successfully deleted %(count)d %(items)s.") % {
                "count": n, "items": model_ngettext(modeladmin.opts, n)
            })
        # Return None to display the change list page again.
        return None

    context = {
        "title": _("Are you sure?"),
        "object_name": force_unicode(opts.verbose_name),
        "deletable_objects": deletable_objects,
        'queryset': queryset,
        "perms_lacking": perms_needed,
        "opts": opts,
        "root_path": modeladmin.admin_site.root_path,
        "app_label": app_label,
        'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
    }

    # Display the confirmation page
    return render_to_response(modeladmin.delete_confirmation_template or [
        "admin/%s/%s/delete_selected_confirmation.html" % (app_label, opts.object_name.lower()),
        "admin/%s/delete_selected_confirmation.html" % app_label,
        "admin/delete_selected_confirmation.html"
    ], context, context_instance=template.RequestContext(request))

delete_selected.short_description = ugettext_lazy("Delete selected %(verbose_name_plural)s")
