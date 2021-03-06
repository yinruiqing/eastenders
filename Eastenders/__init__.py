#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2017 CNRS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# AUTHORS
# Hervé BREDIN - http://herve.niderb.fr


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


import os.path as op
from pyannote.database import Database
from pyannote.database.protocol import SpeakerDiarizationProtocol
from pyannote.parser import MDTMParser


class EastendersSpeakerDiarizationProtocol(SpeakerDiarizationProtocol):
    """Base speaker diarization protocol for ETAPE database
    This class should be inherited from, not used directly.
    Parameters
    ----------
    preprocessors : dict or (key, preprocessor) iterable
        When provided, each protocol item (dictionary) are preprocessed, such
        that item[key] = preprocessor(**item). In case 'preprocessor' is not
        callable, it should be a string containing placeholder for item keys
        (e.g. {'wav': '/path/to/{uri}.wav'})
    """

    def __init__(self, preprocessors={}, **kwargs):
        super(EastendersSpeakerDiarizationProtocol, self).__init__(
            preprocessors=preprocessors, **kwargs)
        #self.uem_parser_ = UEMParser()
        #self.mdtm_parser_ = MDTMParser()

    def _subset(self, protocol, subset):

        data_dir = op.join(op.dirname(op.realpath(__file__)), 'data')
        

        #path = op.join(data_dir, '{protocol}.{subset}.uem'.format(subset=subset, protocol=protocol))
        #uems = self.uem_parser_.read(path)

        # load annotations
        #path = op.join(data_dir, '{protocol}.{subset}.mdtm'.format(subset=subset, protocol=protocol))
        #mdtms = self.mdtm_parser_.read(path)

        path = op.join(data_dir, '{protocol}.{subset}.lst'.format(subset=subset, protocol=protocol))
        with open(path) as f:
            uris = f.readlines()
        uris = [x.strip() for x in uris] 

        for uri in uris:
            #annotated = uems(uri)
            #annotation = mdtms(uri)
            current_file = {
                'database': 'Eastenders',
                'uri': uri}
            #    'annotated': annotated,
            #    'annotation': annotation
            yield current_file


# this protocol defines a speaker diarization protocol: as such, a few methods
# needs to be defined: trn_iter, dev_iter, and tst_iter.

class TV(EastendersSpeakerDiarizationProtocol):
    """My first speaker diarization protocol """

    def trn_iter(self):
        for _ in []:
            yield

    def dev_iter(self):
        for _ in []:
            yield

    def tst_iter(self):
        return self._subset('eastenders', 'all')

# this is where we define each protocol for this database.
# without this, `pyannote.database.get_protocol` won't be able to find them...

class Eastenders(Database):
    """MyDatabase database"""

    def __init__(self, preprocessors={}, **kwargs):
        super(Eastenders, self).__init__(preprocessors=preprocessors, **kwargs)

        # register the first protocol: it will be known as
        # MyDatabase.SpeakerDiarization.MyFirstProtocol
        self.register_protocol(
            'SpeakerDiarization', 'TV', TV)
