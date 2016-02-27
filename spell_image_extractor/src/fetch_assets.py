import json
import urllib2
import glob
import os

apiphp_file = open('apiphp.json')
asset_urls = json.load(apiphp_file)
apiphp_file.close()
card_file = open('data/cards.xml', 'wb')
card_file.write(urllib2.urlopen('https://spellstone.synapse-games.com/assets/cards.xml').read())
card_file.close()
base_url = 'https://d3splaxnu2bep2.cloudfront.net/spellstone/asset_bundles/'
for asset_struct in asset_urls.values():
    asset_url = asset_struct['bundle_name']
    if os.path.exists('data/' + asset_url): 
        print 'Already downloaded', asset_url, 'skipping'
        continue
    asset_data = urllib2.urlopen(base_url + asset_url)
    outf = open('data/' + asset_url, 'wb')
    outf.write(asset_data.read())
    outf.close()
    