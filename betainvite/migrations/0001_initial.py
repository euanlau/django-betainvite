# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'InvitationKey'
        db.create_table(u'betainvite_invitationkey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('date_invited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('from_user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='invitations_sent', null=True, to=orm['core.CoreUser'])),
            ('registrant', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='invitations_used', null=True, to=orm['core.CoreUser'])),
        ))
        db.send_create_signal(u'betainvite', ['InvitationKey'])

        # Adding model 'InvitationUser'
        db.create_table(u'betainvite_invitationuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('inviter', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.CoreUser'], unique=True)),
            ('invitations_remaining', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'betainvite', ['InvitationUser'])

        # Adding model 'WaitingListEntry'
        db.create_table(u'betainvite_waitinglistentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('invited', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'betainvite', ['WaitingListEntry'])


    def backwards(self, orm):
        # Deleting model 'InvitationKey'
        db.delete_table(u'betainvite_invitationkey')

        # Deleting model 'InvitationUser'
        db.delete_table(u'betainvite_invitationuser')

        # Deleting model 'WaitingListEntry'
        db.delete_table(u'betainvite_waitinglistentry')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'betainvite.invitationkey': {
            'Meta': {'object_name': 'InvitationKey'},
            'date_invited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'from_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'invitations_sent'", 'null': 'True', 'to': u"orm['core.CoreUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'registrant': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'invitations_used'", 'null': 'True', 'to': u"orm['core.CoreUser']"})
        },
        u'betainvite.invitationuser': {
            'Meta': {'object_name': 'InvitationUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invitations_remaining': ('django.db.models.fields.IntegerField', [], {}),
            'inviter': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.CoreUser']", 'unique': 'True'})
        },
        u'betainvite.waitinglistentry': {
            'Meta': {'ordering': "['created']", 'object_name': 'WaitingListEntry'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invited': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.coreuser': {
            'Meta': {'object_name': 'CoreUser', 'db_table': "u'core_user'"},
            'avatar': ('hotshop.core.fields.AutoRotatedImageField', [], {'default': "'default-profile.png'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'zh-tw'", 'max_length': '5'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '254'})
        }
    }

    complete_apps = ['betainvite']