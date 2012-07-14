
import httplib2
import simplejson
from urllib import quote_plus

from pprint import pprint

class PelagiosAPIError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg


def annotations(pid):
    purl = "http://pleiades.stoa.org/places/" + pid
    results = []
    u = "http://pelagios.dme.ait.ac.at/api/places/" + quote_plus(
        purl) + "/datasets.json"
    h = httplib2.Http()
    resp, content = h.request(u, "GET")
    if resp['status'] == "200":
        r = simplejson.loads(content)
        for dataset in r:
            print(dataset['uri'])
            subs = []
            for d in dataset.get('subsets', [dataset]):
                if (dataset['title'] == (
                    "Pleiades Annotations in the Perseus Digital Library")
                    ) and d['title'] != "Greek and Roman Materials":
                        continue
                count = d['annotations_referencing_place']
                label = d['title'].rstrip(".")
                uri = d['uri'] + "/annotations?forPlace=%s" % purl
                subs.append((count, label, uri))
            results.append(
                (len(subs), dataset['title'], sorted(subs, reverse=True)))
    else:
        raise PelagiosAPIError, repr(resp)
    return sorted(results, reverse=True)

if __name__ == "__main__":
    r = annotations("579885")
    pprint(r)
    print(len(r))

