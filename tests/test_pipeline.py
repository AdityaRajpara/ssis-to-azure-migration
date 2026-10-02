import unittest
from migration_demo.ingest.sources import fetch_sources
from migration_demo.transform.jobs import normalize,aggregate,quality

class PipelineTests(unittest.TestCase):
    def test_offline_ingestion_covers_source_shapes(self):
        d=fetch_sources(False)
        self.assertTrue(d['311']);self.assertTrue(d['accounts']);self.assertEqual(d['sec']['entityName'],'APPLE INC')

    def test_transform_and_quality(self):
        s=normalize(fetch_sources(False));g=aggregate(s)
        self.assertEqual(sum(x['request_count'] for x in g['complaints_by_type']),len(s['service_requests']))
        self.assertTrue(all(c['passed'] for c in quality(s)))
        self.assertEqual(sum(x['exposure_usd'] for x in g['exposure_by_domain']),sum(a['exposure_usd'] for a in s['accounts']))

if __name__=='__main__': unittest.main()
