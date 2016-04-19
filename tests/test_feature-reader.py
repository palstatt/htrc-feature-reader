import pytest
from htrc_features import FeatureReader
import htrc_features
import os


@pytest.fixture(scope="module")
def paths():
    return [(os.path.join('tests', 'data',
                          'green-gables-15pages-basic.json.bz2'),
             os.path.join('tests', 'data',
                          'green-gables-15pages-advanced.json.bz2')),
            (os.path.join('tests', 'data',
                          'frankenstein-15pages-basic.json.bz2'),
             os.path.join('tests', 'data',
                          'frankenstein-15pages-advanced.json.bz2'))]


class TestFeatureReader():
    TITLES = ['Anne of Green Gables / L.M. Montgomery.',
              'Frankenstein : or, The modern Prometheus.']

    def test_single_path_load(self, paths):
        path = paths[0][0]
        feature_reader = FeatureReader(path)
        vol = next(feature_reader.volumes())
        assert type(vol) == htrc_features.feature_reader.Volume

    def test_tuple_path_load(self, paths):
        paths = paths[0]
        feature_reader = FeatureReader(paths)
        vol = next(feature_reader.volumes())
        assert type(vol) == htrc_features.feature_reader.Volume

    def test_list_load(self, paths):
        paths = [basic for basic, advanced in paths]
        feature_reader = FeatureReader(paths)
        vol = next(feature_reader.volumes())
        assert type(vol) == htrc_features.feature_reader.Volume

    def test_list_tuple_load(self, paths):
        feature_reader = FeatureReader(paths)
        for i, vol in enumerate(feature_reader):
            assert type(vol) == htrc_features.feature_reader.Volume
            assert vol.title == self.TITLES[i]

    def test_json_only_load(self, paths):
        path = paths[0]
        feature_reader = FeatureReader(path)
        basicjson, advjson = next(feature_reader.jsons())
        assert type(basicjson) == dict
        assert type(advjson) == dict
        assert basicjson['features']['pages'][7]['header']['tokenCount'] == 5
        assert advjson['features']['pages'][7]['body']['capAlphaSeq'] == 2

    def test_iteration(self, paths):
        feature_reader = FeatureReader(paths)
        for vol in feature_reader:
            assert type(vol) == htrc_features.feature_reader.Volume
        for vol in feature_reader.volumes():
            assert type(vol) == htrc_features.feature_reader.Volume

    def test_first(self, paths):
        feature_reader = FeatureReader(paths)
        vol = feature_reader.first()
        assert type(vol) == htrc_features.feature_reader.Volume
        assert vol.title == self.TITLES[0]

    def test_uncompressed(self, paths):
        paths = [(basic.replace('.bz2', ''), advanced.replace('.bz2', ''))
                 for basic, advanced in paths]
        feature_reader = FeatureReader(paths, compressed=False)
        for i, vol in enumerate(feature_reader):
            assert type(vol) == htrc_features.feature_reader.Volume
            assert vol.title == self.TITLES[i]

    def test_compress_error(self, paths):
        feature_reader = FeatureReader(paths, compressed=False)
        with pytest.raises(ValueError):
            next(feature_reader.volumes())

        paths = [(basic.replace('.bz2', ''), advanced.replace('.bz2', ''))
                 for basic, advanced in paths]
        feature_reader = FeatureReader(paths, compressed=True)
        with pytest.raises(IOError):
            next(feature_reader.volumes())
