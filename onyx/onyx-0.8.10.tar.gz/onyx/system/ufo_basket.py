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

from onyx.core import Date, RDate, DateRange
from onyx.core import Curve, GCurve, Interpolate, CurveUnion
from onyx.core import SetField, DictField, ValueType, Archivable
from onyx.core import MktIndirectionFactory, EnforceArchivableEntitlements

import numpy as np

__all__ = ["Basket"]


###############################################################################
@EnforceArchivableEntitlements("Database", "ArchivedOverwritable")
class Basket(Archivable):
    """
    Container-like object use to represent a basket of equally weighted assets.
    """
    FilterBy = DictField(default={})

    # -------------------------------------------------------------------------
    @MktIndirectionFactory(SetField)
    def Symbols(self, graph):
        pass

    # -------------------------------------------------------------------------
    @ValueType("PropSubGraph")
    def SymbolsCurve(self, graph, start=None, end=None):
        crv = self.get_history("Symbols", start, end)
        if len(graph(self, "FilterBy")):
            vls = []
            for symbols in crv.values:
                for attr, value in graph(self, "FilterBy").items():
                    symbols = {sym for sym in symbols
                               if graph(sym, attr) == value}
                vls.append(symbols)
            crv = GCurve(crv.dates, vls)
        return crv

    # -------------------------------------------------------------------------
    @ValueType()
    def FilteredSymbols(self, graph):
        symbols = graph(self, "Symbols")
        for attr, value in graph(self, "FilterBy").items():
            symbols = {sym for sym in symbols if graph(sym, attr) == value}
        return symbols

    # -------------------------------------------------------------------------
    @ValueType("PropSubGraph")
    def GetCurve(self, graph, start=None, end=None):
        start = start or Date.low_date()
        end = end or graph("Database", "MktDataDate")
        symbols_crv = graph(self, "SymbolsCurve", start, end)

        rts_crv = Curve()
        for date, symbols in symbols_crv:
            new_rts_crv = self.get_returns(graph, date, end, symbols)
            rts_crv = CurveUnion(new_rts_crv, rts_crv)

        returns = rts_crv.values
        returns[0] = 0.0

        # --- the benchkmark is reconstructed from the series of returns
        return Curve(rts_crv.dates, np.cumprod(1.0 + returns))

    # -------------------------------------------------------------------------
    def get_returns(self, graph, start, end, symbols):
        dts = list(DateRange(start + RDate("-1d"), end, "+1d"))
        rts = np.zeros(len(dts) - 1)

        # --- we adjust the start date to make sure that we always have at
        #     least one knot in the curve before start date (this is needed
        #     by Interpolate)
        start_adj = start + RDate("-1w")

        # --- the basket is rewighted daily, hence we just need to calculate
        #     the series of average returns
        for sym in symbols:
            crv = graph(sym, "PricesForRisk").crop(start_adj, end)
            vls = np.array([Interpolate(crv, d) for d in dts])
            rts += vls[1:] / vls[:-1] - 1.0

        num_of_symbols = len(symbols)
        if num_of_symbols:
            rts /= float(num_of_symbols)

        return Curve(dts[1:], rts)


# -----------------------------------------------------------------------------
def prepare_for_test():
    from onyx.core import AddIfMissing, Date, RDate, EvalBlock
    from . import ufo_database

    ufo_database.prepare_for_test()

    dt1 = Date.today() + RDate("-2m")
    dt2 = Date.today() + RDate("-1m")

    sym1 = {"aaa", "bbb"}
    sym2 = {"aaa", "ccc"}

    bskt = AddIfMissing(Basket(Name="TestBasket"))

    with EvalBlock() as eb:
        eb.change_value("Database", "ArchivedOverwritable", True)
        bskt.set_dated("Symbols", dt1, sym1)
        bskt.set_dated("Symbols", dt2, sym2)

    return bskt, [dt1, dt2], [sym1, sym2]
