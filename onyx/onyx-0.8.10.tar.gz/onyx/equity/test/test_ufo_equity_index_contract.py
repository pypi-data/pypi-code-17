###############################################################################
#
#   Copyright: (c) 2015 Carlo Sbraccia
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
###############################################################################

from onyx.core import GetVal, OnyxTestCase
from onyx.equity import ufo_equity_index_contract

import unittest


###############################################################################
class UnitTest(OnyxTestCase):
    # -------------------------------------------------------------------------
    def setUp(self):
        super().setUp()
        cnt, prc = ufo_equity_index_contract.prepare_for_test()[0]
        self.cnt = cnt
        self.prc = prc

    # -------------------------------------------------------------------------
    def test_Ticker(self):
        mth = GetVal(self.cnt, "DeliveryMonth")
        bbg_ticker = "VG{0:s}{1:s}".format(mth[0], mth[-1])
        self.assertEqual(GetVal(self.cnt, "Ticker"), bbg_ticker)

    # -------------------------------------------------------------------------
    def test_UniqueId(self):
        mth = GetVal(self.cnt, "DeliveryMonth")
        idx = GetVal(GetVal(self.cnt, "EquityIndex"), "Symbol")
        self.assertEqual(GetVal(self.cnt, "UniqueId"),
                         "{0:s} {1:s}".format(idx, mth))

    # -------------------------------------------------------------------------
    def test_Spot(self):
        self.assertEqual(GetVal(self.cnt, "Spot"), self.prc)


if __name__ == "__main__":
    from onyx.core.utils.unittest import UseEphemeralDbs
    with UseEphemeralDbs():
        unittest.main(failfast=True)
