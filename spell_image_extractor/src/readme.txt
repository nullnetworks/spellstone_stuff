First you need to download the asset bundle list from a web browser. Bring up
the network monitor and download the response to the init call to api.php.

Search for "asset_bundles" and remove everything from the start of the file up
to the opening brace after the "asset_bundles" value. Find the matching closing
brace and delete everything after it. Save this file as apiphp.json

Run fetch_assets.py to download all of the asset bundles.

Run extract_assets.bat from a terminal to extract the assets using disunity. A
copy is included.

Run image_extractor to extract the card images from the atlases.

Run imgbrowse to browse any un-named images and names and match them up. Once
you click in the listbox, left and right change the picture and enter applies
the selected name to the selected image.
