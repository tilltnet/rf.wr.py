# -*- coding: UTF-8 -*-
import xml.etree.ElementTree as ET
import codecs
import raumfeld

########
with codecs.open('favorites', 'a+', 'UTF-8') as f:
            content = f.readlines()
alternater = 0
counter = 0
URIs = []
Meta = []
for line in content:
        if alternater == 0:
                URIs.append(line.encode('UTF-8'))
                alternater = 1
        else:
                Meta.append(line.encode('UTF-8'))
                alternater = 0
        counter = counter + 1
URIs = [each.replace('\n', '') for each in URIs]
Meta = [each.replace('\n', '') for each in Meta]

for i in range(1,len(URIs)):
        if Meta[i] == '':
                Meta[i] = u''.join([u'<DIDL-Lite xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dlna="urn:schemas-dlna-org:metadata-1-0/" xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" xmlns:raumfeld="urn:schemas-raumfeld-com:meta-data/raumfeld"><container><dc:title>',URIs[i],u'</dc:title></container></DIDL-Lite>'])

no = 1

trees = [ET.fromstring(each) for each in Meta]
namespaces = {'dc': 'http://purl.org/dc/elements/1.1/', 'upnp':'urn:schemas-upnp-org:metadata-1-0/upnp/'}
titles = [tree[0].find('dc:title', namespaces).text for tree in trees]
cover_imgs = [tree[0].find('upnp:albumArtURI', namespaces).text for tree in trees]


zones = raumfeld.discover()
active_zone = zones[0]
if active_zone == 999:
        print('err_msg')
URIs.append(active_zone.currentURI)
Meta.append(active_zone.currentURIMetaData)

print(type(active_zone.currentURIMetaData))
print(active_zone.currentURIMetaData)
out_list = []
for i in range(0,len(URIs)):
        out_list.append(URIs[i])
        out_list.append(Meta[i])
with codecs.open('favorites','w', encoding='UTF-8') as f:
        for item in out_list:
                f.write("%s\n" % item)
