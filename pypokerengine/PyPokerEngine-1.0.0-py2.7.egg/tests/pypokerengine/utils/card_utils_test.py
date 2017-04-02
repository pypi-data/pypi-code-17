import pypokerengine.utils.card_utils as U

from mock import patch
from tests.base_unittest import BaseUnitTest
from pypokerengine.engine.card import Card

class CardUtilsTest(BaseUnitTest):

    def test_gen_cards(self):
        self.eq([Card(rank=1, suit=2), Card(rank=12, suit=4)], U.gen_cards(["CA", "DQ"]))
        self.eq([Card(rank=9, suit=8), Card(rank=10, suit=2)], U.gen_cards(["H9", "CT"]))
        self.eq([Card(rank=11, suit=16), Card(rank=13, suit=4)], U.gen_cards(["SJ", "DK"]))

    def test_montecarlo_simulation(self):
        my_cards = U.gen_cards(["D6", "D2"])
        community = U.gen_cards(['D5', 'D9', 'H6', 'CK'])

        mock_return = community + [Card.from_str("D7")]
        with patch('pypokerengine.utils.card_utils._fill_community_card', side_effect=[mock_return]):
            U._montecarlo_simulation(3, my_cards, community)
            U._fill_community_card.assert_called_with(community, used_card=my_cards+community)

        mock_return = [U.gen_cards(a) for a in [["D7"], ["DK", "HK", "H8", "SA"]]]
        with patch('pypokerengine.utils.card_utils._pick_unused_card', side_effect=mock_return):
            self.eq(1, U._montecarlo_simulation(3, my_cards, community))
            U._pick_unused_card.assert_called_with(4, Any(list))

        mock_return = [U.gen_cards(a) for a in [["S7"], ["DK", "HK", "H8", "SA"]]]
        with patch('pypokerengine.utils.card_utils._pick_unused_card', side_effect=mock_return):
            self.eq(0, U._montecarlo_simulation(3, my_cards, community))
            U._pick_unused_card.assert_called_with(4, Any(list))

def Any(cls):
    class Any(cls):
        def __eq__(self, other):
            return True
    return Any()
