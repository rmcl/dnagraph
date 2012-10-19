# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Node'
        db.create_table('graph_node', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('length', self.gf('django.db.models.fields.IntegerField')()),
            ('locations', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('sequence', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('graph', ['Node'])

        # Adding M2M table for field parents on 'Node'
        db.create_table('graph_node_parents', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_node', models.ForeignKey(orm['graph.node'], null=False)),
            ('to_node', models.ForeignKey(orm['graph.node'], null=False))
        ))
        db.create_unique('graph_node_parents', ['from_node_id', 'to_node_id'])


    def backwards(self, orm):
        # Deleting model 'Node'
        db.delete_table('graph_node')

        # Removing M2M table for field parents on 'Node'
        db.delete_table('graph_node_parents')


    models = {
        'graph.node': {
            'Meta': {'object_name': 'Node'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {}),
            'locations': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parents': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['graph.Node']", 'symmetrical': 'False'}),
            'sequence': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['graph']