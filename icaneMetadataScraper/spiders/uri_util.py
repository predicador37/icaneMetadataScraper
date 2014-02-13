# -*- coding: utf-8 -*-
import urllib2 as urllib
import json

    
def getLiveJson(url):
    request = urllib.Request(url, headers={"Accept" : "application/json"})
    return urllib.urlopen(request)


def findLink(node, links):
   
    if (str(node["nodeType"]["uriTag"]) == "time-series" or str(node["nodeType"]["uriTag"])=="non-olap-native"):
        if links:        
            links.append(node["uri"])
        else:
            links = [node["uri"]]
        return links
    else:
        for child in node["children"]: #child is a dictionary        
            findLink(child, links)
            
    return None
    
        
def findUris(data):
    if str(data['nodeType']['uriTag'])=='time-series' or str(data['nodeType']['uriTag'])=='non-olap-native':
        if 'uri' in data:
            yield data['uri']
    for k in data:
        if isinstance(data[k], list) and k not in ['apiUris','links','sources','measures']:
            for i in data[k]:
                for j in findUris(i):
                    yield j
    

def getUris(rootUri):
    links = []
    content = getLiveJson(rootUri)
    nodes = json.load(content)

    if isinstance(nodes, list):
        for node in nodes:
            links = links + list(findUris(node))
    else:
        links = findUris(nodes)
    #print "Total initial nodes to scrap: " + str(len(nodes))      
    #print "Total scraped URIs: " + str(len(links))      
    #for link in links:
    #    print link
    return links