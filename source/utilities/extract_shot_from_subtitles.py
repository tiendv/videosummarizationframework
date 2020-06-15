import os
import xml.etree.ElementTree as ET

root_path = '/mmlabstorage/datasets/TRECVID/TRECVID_BBC_EastEnders/transcripts'

file='5638099347502840287.xml'

temp= '/mmlabstorage/datasets/TRECVID/TRECVID_BBC_EastEnders/transcripts/5115997969040288798.xml'
path = os.path.join(root_path,file)
print(path)
tree = ET.parse(temp)
root = tree.getroot()
#root = ET.fromstring(country_data_as_string)
print(root)