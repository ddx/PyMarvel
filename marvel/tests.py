import json
import os
import unittest

from .marvel import Marvel
from .core import TextObject, Image
from .creator import CreatorList, CreatorSummary
from .character import CharacterDataWrapper, CharacterDataContainer, Character, CharacterList, CharacterSummary
from .story import StoryList, StorySummary
from .event import EventList, EventSummary, Event
from .comic import ComicDataWrapper, ComicDataContainer, Comic, ComicSummary, ComicDate, ComicPrice
from .config import *

class PyMarvelTestCase(unittest.TestCase):

    def setUp(self):
        self.m = Marvel(PUBLIC_KEY, PRIVATE_KEY)

    def tearDown(self):
        pass

    def test_get_character(self):
        cdw = self.m.get_character(1009718)

        assert cdw.code == 200
        assert cdw.status == 'Ok'
        assert cdw.data.results[0].name == "Wolverine"

        print "\nGet Character: \n"
        print cdw.data.results[0].name

    def test_get_character_get_comics(self):
        character = self.m.get_character(1009718).data.result
        comic_dw = character.get_comics()

        assert comic_dw.code == 200
        assert comic_dw.status == 'Ok'
        
        print "\nWolverine comics: \n"
        for c in comic_dw.data.results:
            print "%s - %s" % (c.id, c.title)

        comic_dw_params = character.get_comics(format="comic", formatType="comic", hasDigitalIssue=True, orderBy="title", limit=10, offset=30)

        assert comic_dw_params.code == 200
        assert comic_dw_params.status == 'Ok'
        
        print "\nWolverine comics with parameters: \n"
        for c in comic_dw_params.data.results:
            print "%s - %s" % (c.id, c.title)


    def test_get_character_get_events(self):
        character = self.m.get_character(1009718).data.result
        events_dw = character.get_events()

        assert events_dw.code == 200
        assert events_dw.status == 'Ok'

        print "\nCharacter.get_events(): \n"
        for e in events_dw.data.results:
            print "%s - %s" % (e.id, e.title)

        events_dw_params = character.get_events(orderBy="startDate", limit=10)

        assert events_dw_params.code == 200
        assert events_dw_params.status == 'Ok'

        print "\nCharacter.get_events(params): \n"
        for e in events_dw_params.data.results:
            print "%s - %s" % (e.id, e.title)

    def test_get_characters(self):
        cdw = self.m.get_characters(orderBy="name,-modified", limit="10", offset="15")

        assert cdw.code == 200
        assert cdw.status == 'Ok'

        assert cdw.data.count > 0
        assert cdw.data.offset == 15
        assert cdw.data.limit == 10
        assert len(cdw.data.results) > 0

        assert type(cdw) is CharacterDataWrapper
        assert type(cdw.data) is CharacterDataContainer
        assert type(cdw.data.results) is list

        print "\nGet Characters: \n"
        for c in cdw.data.results:
            print "%s - %s" % (c.id, c.name)

    def test_get_characters_next(self):
        cdw = self.m.get_characters(orderBy="name,-modified", limit="20", offset="15")
        new_cdw = cdw.next()

        assert new_cdw.code == 200

        #poor test?
        assert new_cdw.data.offset == cdw.data.offset + cdw.data.limit


    def test_get_comic(self):
        #Need a comic with everything
        cdw = self.m.get_comic(531)

        assert cdw.code == 200
        assert cdw.status == 'Ok'

        assert cdw.data.count > 0
        assert cdw.data.offset == 0
        assert len(cdw.data.results) > 0

        assert type(cdw) is ComicDataWrapper
        assert type(cdw.data) is ComicDataContainer
        assert type(cdw.data.results) is list

        #properties
        #textObjects
        assert len(cdw.data.results[0].textObjects) > 0
        assert isinstance(cdw.data.results[0].textObjects[0], TextObject)
        #collections
        assert isinstance(cdw.data.results[0].collections[0], ComicSummary)
        #prices/dates
        assert isinstance(cdw.data.results[0].prices[0], ComicPrice)
        assert isinstance(cdw.data.results[0].dates[0], ComicDate)
        #images
        assert isinstance(cdw.data.results[0].thumbnail, Image)
        assert isinstance(cdw.data.results[0].images[0], Image)
        #lists
        assert isinstance(cdw.data.results[0].creators, CreatorList)
        assert isinstance(cdw.data.results[0].creators.items[0], CreatorSummary)
        assert isinstance(cdw.data.results[0].characters, CharacterList)
        assert isinstance(cdw.data.results[0].characters.items[0], CharacterSummary)
        assert isinstance(cdw.data.results[0].stories, StoryList)
        assert isinstance(cdw.data.results[0].stories.items[0], StorySummary)
        #TODO: Need a test case with an Event
        #assert isinstance(cdw.data.results[0].events, EventList)
        #assert isinstance(cdw.data.results[0].events.items[0], EventSummary)



        
    def test_get_comics(self):
        cdw = self.m.get_comics(orderBy="issueNumber,-modified", limit="10", offset="15")

        assert cdw.code == 200
        assert cdw.status == 'Ok'

        assert cdw.data.count > 0
        assert cdw.data.offset == 15
        assert cdw.data.limit == 10
        assert len(cdw.data.results) > 0

        assert type(cdw) is ComicDataWrapper
        assert type(cdw.data) is ComicDataContainer
        assert type(cdw.data.results) is list

        for c in cdw.data.results:
            print "%s - %s" % (c.id, c.title)
            

    def test_get_creator(self):
        #Grab Stan the Man
        cdw = self.m.get_creator(30)

        assert cdw.code == 200
        assert cdw.status == 'Ok'
        assert cdw.data.result.firstName == "Stan"
        assert cdw.data.result.lastName == "Lee"

    def test_get_creator_get_comics(self):
        #Grab Stan the Man
        theman = self.m.get_creator(30).data.result
        
        comic_dw = theman.get_comics()

        assert comic_dw.code == 200
        assert comic_dw.status == 'Ok'
        
        print "\nCreator.get_comics(): \n"
        for c in comic_dw.data.results:
            print "%s - %s" % (c.id, c.title)

        comic_dw_params = theman.get_comics(format="comic", formatType="comic", hasDigitalIssue=True, orderBy="title", limit=10, offset=30)

        assert comic_dw_params.code == 200
        assert comic_dw_params.status == 'Ok'
        
        print "\nCreator.get_comics(params): \n"
        for c in comic_dw_params.data.results:
            print "%s - %s" % (c.id, c.title)


    def test_get_event(self):
        event_dw = self.m.get_event(253)

        assert event_dw.code == 200
        assert event_dw.status == 'Ok'        

        print "\nMarvel.get_event: \n"
        event = event_dw.data.result
        assert isinstance(event, Event)
        assert event.title == "Infinity Gauntlet"
        print event.title
        print event.description


    def test_get_events(self):
        response = self.m.get_events(characters="1009351,1009718")

        assert response.code == 200
        assert response.status == 'Ok'

        assert response.data.total > 0

        print "\nMarvel.get_events: \n"
        for e in response.data.results:
            print "%s" % e.title

if __name__ == '__main__':
    unittest.main()

"python -m unittest marvel.tests"