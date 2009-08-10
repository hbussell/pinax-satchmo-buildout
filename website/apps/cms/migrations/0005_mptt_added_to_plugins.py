
from south.db import db
from django.db import models
from cms.models import *
import datetime

class Migration:
    
    def forwards(self, orm):
        db.add_column('cms_cmsplugin', 'tree_id', models.PositiveIntegerField(db_index=True, editable=False))
        db.add_column('cms_cmsplugin', 'lft', models.PositiveIntegerField(db_index=True, editable=False))
        db.add_column('cms_cmsplugin', 'rght', models.PositiveIntegerField(db_index=True, editable=False))
        db.add_column('cms_cmsplugin', 'level', models.PositiveIntegerField(db_index=True, editable=False))
        if not db.dry_run:
            plugins = orm.CMSPlugin.objects.all().order_by('page', 'position')
            for plugin in plugins:
                if not plugin.parent_id and plugin.position:
                    plugin.tree_id = plugin.position
                    plugin.save()
            for plugin in plugins:
                if plugin.parent_id:
                    for p in plugins:
                        if p.pk == plugin.parent_id and p.position:
                            plugin.tree_id = p.tree_id
                            plugin.save()
                
    
    def backwards(self, orm):
        db.delete_column('cms_cmsplugin', 'tree_id')
        db.delete_column('cms_cmsplugin', 'lft')
        db.delete_column('cms_cmsplugin', 'rght')
        db.delete_column('cms_cmsplugin', 'level')
    
    
    models = {
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'db_table': "'django_site'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'cms.pagepermission': {
            'can_change_softroot': ('models.BooleanField', ['_("can change soft-root")'], {'default': 'False'}),
            'can_edit': ('models.BooleanField', ['_("can edit")'], {'default': 'True'}),
            'can_publish': ('models.BooleanField', ['_("can publish")'], {'default': 'True'}),
            'everybody': ('models.BooleanField', ['_("everybody")'], {'default': 'False'}),
            'group': ('models.ForeignKey', ['Group'], {'null': 'True', 'verbose_name': '_("group")', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'page': ('models.ForeignKey', ['Page'], {'null': 'True', 'verbose_name': '_("page")', 'blank': 'True'}),
            'type': ('models.IntegerField', ['_("type")'], {'default': '0'}),
            'user': ('models.ForeignKey', ['User'], {'null': 'True', 'verbose_name': '_("user")', 'blank': 'True'})
        },
        'cms.cmsplugin': {
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'default': 'datetime.datetime.now', 'editable': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'language': ('models.CharField', ['_("language")'], {'db_index': 'True', 'max_length': '3', 'editable': 'False', 'blank': 'False'}),
            'level': ('models.PositiveIntegerField', [],{'db_index':True, 'editable':False}),
            'lft': ('models.PositiveIntegerField', [],{'db_index':True, 'editable':False}),
            'page': ('models.ForeignKey', ['Page'], {'editable': 'False', 'verbose_name': '_("page")'}),
            'parent': ('models.ForeignKey', ["'self'"], {'null': 'True', 'editable': 'False', 'blank': 'True'}),
            'placeholder': ('models.CharField', ['_("slot")'], {'max_length': '50', 'editable': 'False', 'db_index': 'True'}),
            'plugin_type': ('models.CharField', ['_("plugin_name")'], {'max_length': '50', 'editable': 'False', 'db_index': 'True'}),
            'position': ('models.PositiveSmallIntegerField', ['_("position")'], {'null': 'True', 'editable': 'False', 'blank': 'True'}),
            'rght': ('models.PositiveIntegerField', [],{'db_index':True, 'editable':False}),
            'tree_id': ('models.PositiveIntegerField', [],{'db_index':True, 'editable':False}),
        },
        'cms.title': {
            'Meta': {'unique_together': "('language','page')"},
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'default': 'datetime.datetime.now', 'editable': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'language': ('models.CharField', ['_("language")'], {'max_length': '3', 'db_index': 'True'}),
            'page': ('models.ForeignKey', ['Page'], {'related_name': '"title_set"', 'verbose_name': '_("page")'}),
            'path': ('models.CharField', ['_("path")'], {'max_length': '255', 'db_index': 'True'}),
            'slug': ('models.SlugField', ['_("slug")'], {'unique': 'False', 'max_length': '255', 'db_index': 'True'}),
            'title': ('models.CharField', ['_("title")'], {'max_length': '255'})
        },
        'cms.page': {
            'Meta': {'ordering': "('tree_id','lft')"},
            'author': ('models.ForeignKey', ['User'], {'limit_choices_to': "{'page__isnull':False}", 'verbose_name': '_("author")'}),
            'creation_date': ('models.DateTimeField', [], {'default': 'datetime.datetime.now', 'editable': 'False'}),
            'has_url_overwrite': ('models.BooleanField', ['_("has url overwrite")'], {'default': 'False', 'db_index': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'in_navigation': ('models.BooleanField', ['_("in navigation")'], {'default': 'True', 'db_index': 'True'}),
            'level': ('models.PositiveIntegerField', [],{'db_index':True, 'editable':False}),
            'lft': ('models.PositiveIntegerField', [],{'db_index':True, 'editable':False}),
            'login_required': ('models.BooleanField', ["_('login required')"], {'default': 'False'}),
            'navigation_extenders': ('models.CharField', ['_("navigation extenders")'], {'blank': 'True', 'max_length': '80', 'null': 'True', 'db_index': 'True'}),
            'parent': ('models.ForeignKey', ["'self'"], {'db_index': 'True', 'related_name': "'children'", 'null': 'True', 'editable': 'False', 'blank': 'True'}),
            'publication_date': ('models.DateTimeField', ['_("publication date")'], {'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'publication_end_date': ('models.DateTimeField', ['_("publication end date")'], {'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'reverse_id': ('models.CharField', ['_("id")'], {'blank': 'True', 'max_length': '40', 'null': 'True', 'db_index': 'True'}),
            'rght': ('models.PositiveIntegerField', [],{'db_index':True, 'editable':False}),
            'sites': ('models.ManyToManyField', ['Site'], {'default': '[settings.SITE_ID]', 'verbose_name': '_("sites")'}),
            'soft_root': ('models.BooleanField', ['_("soft root")'], {'default': 'False', 'db_index': 'True'}),
            'status': ('models.IntegerField', ['_("status")'], {'default': 0, 'db_index': 'True'}),
            'template': ('models.CharField', ['_("template")'], {'max_length': '100'}),
            'tree_id': ('models.PositiveIntegerField', [],{'db_index':True, 'editable':False}),
            'url_overwrite': ('models.CharField', ['_("url overwrite")'], {'blank': 'True', 'max_length': '80', 'null': 'True', 'db_index': 'True'})
        },
        'auth.group': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    
    complete_apps = ['cms']
