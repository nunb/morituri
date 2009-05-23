# -*- Mode: Python; test-case-name: morituri.test.test_image_image -*-
# vi:si:et:sw=4:sts=4:ts=4

import os
import unittest

import gobject
gobject.threads_init()

from morituri.image import image
from morituri.common import task, common

def h(i):
    return "0x%08x" % i

class TrackSingleTestCase(unittest.TestCase):
    def setUp(self):
        self.image = image.Image(os.path.join(os.path.dirname(__file__),
            'track-single.cue'))
        self.runner = task.SyncRunner(verbose=False)
        self.image.setup(self.runner)

    def testAccurateRipChecksum(self):
        checksumtask = image.AccurateRipChecksumTask(self.image) 
        self.runner.run(checksumtask, verbose=False)

        self.assertEquals(len(checksumtask.checksums), 4)
        self.assertEquals(h(checksumtask.checksums[0]), '0x00000000')
        self.assertEquals(h(checksumtask.checksums[1]), '0x793fa868')
        self.assertEquals(h(checksumtask.checksums[2]), '0x8dd37c26')
        self.assertEquals(h(checksumtask.checksums[3]), '0x00000000')

    def testLength(self):
        self.assertEquals(self.image.table.getTrackLength(1), 2)
        self.assertEquals(self.image.table.getTrackLength(2), 2)
        self.assertEquals(self.image.table.getTrackLength(3), 2)
        self.assertEquals(self.image.table.getTrackLength(4), 4)

    def testCDDB(self):
        self.assertEquals(self.image.table.getCDDBDiscId(), "08000004")

    def testAccurateRip(self):
        self.assertEquals(self.image.table.getAccurateRipIds(), (
            "00000016", "0000005b"))

class TrackSeparateTestCase(unittest.TestCase):
    def setUp(self):
        self.image = image.Image(os.path.join(os.path.dirname(__file__),
            'track-separate.cue'))
        self.runner = task.SyncRunner(verbose=False)
        self.image.setup(self.runner)

    def testAccurateRipChecksum(self):
        checksumtask = image.AccurateRipChecksumTask(self.image) 
        self.runner.run(checksumtask, verbose=False)

        self.assertEquals(len(checksumtask.checksums), 4)
        self.assertEquals(h(checksumtask.checksums[0]), '0xd60e55e1')
        self.assertEquals(h(checksumtask.checksums[1]), '0xd63dc2d2')
        self.assertEquals(h(checksumtask.checksums[2]), '0xd63dc2d2')
        self.assertEquals(h(checksumtask.checksums[3]), '0x7271db39')

    def testLength(self):
        self.assertEquals(self.image.table.getTrackLength(1), 10)
        self.assertEquals(self.image.table.getTrackLength(2), 10)
        self.assertEquals(self.image.table.getTrackLength(3), 10)
        self.assertEquals(self.image.table.getTrackLength(4), 10)

    def testCDDB(self):
        self.assertEquals(self.image.table.getCDDBDiscId(), "08000004")

    def testAccurateRip(self):
        self.assertEquals(self.image.table.getAccurateRipIds(), (
            "00000064", "00000191"))

class AudioLengthTestCase(unittest.TestCase):
    def testLength(self):
        path = os.path.join(os.path.dirname(__file__), 'track.flac')
        t = image.AudioLengthTask(path)
        runner = task.SyncRunner()
        runner.run(t, verbose=False)
        self.assertEquals(t.length, 10 * common.SAMPLES_PER_FRAME)
