'''
Created on Apr 8, 2009

@author: patricklauber
'''
from cms.models import CMSPlugin
import re

OBJ_TAG_RE = re.compile(u"\{\{ plugin_object (\d+) \}\}")
OBJ_ADMIN_RE = re.compile(ur'<img [^>]*\bid="plugin_obj_(\d+)"[^>]*/?>')

def plugin_tags_to_admin_html(text):
    """
    Convert plugin object 'tags' into the form used to represent
    them in the admin text editor.
    """
    def _tag_to_admin(m):
        plugin_id = int(m.groups()[0])
        try:
            obj = CMSPlugin.objects.get(pk=plugin_id)
        except CMSPlugin.DoesNotExist:
            # Object must have been deleted.  It cannot be rendered to
            # end user, or edited, so just remove it from the HTML
            # altogether
            return u''
        return u'<img src="%(icon_src)s" alt="%(icon_alt)s" id="plugin_obj_%(id)d" />' % \
               dict(id=plugin_id,
                    icon_src=force_escape(obj.get_instance_icon_src()),
                    icon_alt=force_escape(obj.get_instance_icon_alt()),
                    )

    return OBJ_TAG_RE.sub(_tag_to_admin, text)

def plugin_tags_to_user_html(text, context, placeholder):
    """
    Convert plugin object 'tags' into the form for public site.

    context is the template context to use, placeholder is the placeholder name
    """
    def _render_tag(m):
        plugin_id = int(m.groups()[0])
        try:
            obj = CMSPlugin.objects.get(pk=plugin_id)
        except CMSPlugin.DoesNotExist:
            # Object must have been deleted.  It cannot be rendered to
            # end user so just remove it from the HTML altogether
            return u''
        return obj.render_plugin(context, placeholder)
    return OBJ_ADMIN_RE.sub(_render_tag, text)



def plugin_admin_html_to_tags(text):
    """
    Convert the HTML used in admin editor to represent plugin objects
    into the 'tag' form used in the database
    """
    return OBJ_ADMIN_RE.sub(lambda m: u"{{ plugin_object %s }}"  % m.groups()[0], text)

