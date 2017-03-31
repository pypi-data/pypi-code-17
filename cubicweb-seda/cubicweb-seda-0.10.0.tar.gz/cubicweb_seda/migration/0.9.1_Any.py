# coding: utf-8

for e in rql('Any X groupby X WHERE X container C HAVING COUNT(C) > 1').entities():
    container = max(c.eid for c in e.container)
    e.cw_set(container=None)
    e.cw_set(container=container)
    commit()

sync_schema_props_perms('container')

scheme = cnx.find('ConceptScheme', title=u'SEDA 2 : Status légaux').one()
for old_label, new_label in [(u'Archive publique', u'Archives publiques'),
                             (u'Archive privée', u'Archives privées')]:
    label = rql('Label X WHERE X label %(l)s, X label_of C, C in_scheme S, S eid %(s)s',
                {'s': scheme.eid, 'l': old_label}).one()
    label.cw_set(label=new_label)

commit()

scheme = cnx.find('ConceptScheme', title=u'SEDA : Niveaux de description').one()
for old_label, new_label in [(u"Dossier l'intérieur d'une série organique", u'Dossier'),
                             (u'Item', u'Pièce')]:
    label = rql('Label X WHERE X label %(l)s, X label_of C, C in_scheme S, S eid %(s)s',
                {'s': scheme.eid, 'l': old_label}).one()
    label.cw_set(label=new_label)
    # don't care about migrating updated definition for now
commit()


sync_schema_props_perms('seda_description_level')
