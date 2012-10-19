# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Node.ran_repeatmasker'
        db.add_column('graph_node', 'ran_repeatmasker',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Node.ran_repeatmasker'
        db.delete_column('graph_node', 'ran_repeatmasker')


    models = {
        'graph.node': {
            'Meta': {'object_name': 'Node'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {}),
            'locations': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parents': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['graph.Node']", 'symmetrical': 'False'}),
            'ran_repeatmasker': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sequence': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['graph']