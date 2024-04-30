import api, time, json
import unittest

class TestCuboid(unittest.TestCase):
    def test_calling(self):
        expected = {'currentStation': 'New Haven Union Station',
                    'direction': 'eastbound',
                    'callingAt': ['New Haven State Street', 'Branford', 'Guilford', 'Madison', 'Clinton', 'Westbrook', 'Old Saybrook', 'New London'],
                     'terminatesAt': 'New London'}
        self.assertAlmostEqual(api.getCallingAt("eastbound", "New Haven Union Station"), expected)

print()
#print(json.dumps(api.getAllTrainsAtStation(round(time.time()), "Madison", True)))
#print(api.parseTime("7:15 AM", 21, 4, 2024))