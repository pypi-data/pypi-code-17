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

from onyx.core import Date, RDate, Curve, GCurve
from onyx.core import Interpolate, ApplyAdjustments
from onyx.core import Archivable, ValueType, GetVal, EvalBlock
from onyx.core import StringField, ListField, ReferenceField
from onyx.core import MktIndirectionFactory, EnforceArchivableEntitlements

import numpy as np
import collections

__all__ = ["CorporateActions"]


###############################################################################
@EnforceArchivableEntitlements("Database", "ArchivedOverwritable")
class CorporateActions(Archivable):
    """
    Class used to represent corporate actions, archived by their Declared Date.
    """
    Asset = ReferenceField(obj_type="EquityAsset")

    # -------------------------------------------------------------------------
    @MktIndirectionFactory(StringField)
    def DvdCcy(self, graph):
        """
        Here we store the currency used for dividend payments.
        """
        pass

    # -------------------------------------------------------------------------
    @MktIndirectionFactory(ListField)
    def ActionInfo(self, graph):
        """
        Here we store the list of corporate actions as of the relevant ex-date.
        The structure is the following:
        [
            {
                "ex-date": first date after which shareholders are no longer
                           entitled to the benefits of the coporate action,
                "declared-date": the date when the corporate action is
                                 officially annaunced,
                "pay-date": the date when the payment takes place,
                "type": ["cash", "scrip", "split", "rights issue", "other"],
                "amount": for cash it's the gross dividend amount,
                          for scrip, split, rights issue, and "other" it's the
                          multiplicative factor.
            },
        ]
        """
        pass

    # -------------------------------------------------------------------------
    @ValueType()
    def LastKnot(self, graph):
#        date = date or graph("Database", "MktDataDate")
        date = graph("Database", "MktDataDate")
        return self.get_dated("ActionInfo", date, strict=False)

    # -------------------------------------------------------------------------
    @ValueType("Callable")
    def NextExDateActions(self, graph, start):
        # FIXME: this is extremely inefficient, we should use a specialized
        #        query
        pos_dt = graph("Database", "PositionsDate")
        crv = self.corp_actions_curve(start=max(start, pos_dt))
        if len(crv):
            return crv.front.value
        else:
            return [{"ex-date": Date.high_date(), "type": None}]

    # -------------------------------------------------------------------------
    @ValueType()
    def AdjustCurve(self, graph):
        ccy = graph(graph(self, "Asset"), "Denominated")
        mul = graph(graph(self, "Asset"), "Multiplier")

        def adjuster(crv):
            start = crv.front.date
            end = crv.back.date
            offset = RDate("-1b")
            adj_crv = Curve()

            for date, actions in self.corp_actions_curve(start=start, end=end):

                if date == start:
                    # --- remove this knot from the curve and skip this
                    #     corporate action
                    start += RDate("+1b")
                    continue

                prev_biz_date = date + offset
                prev_close = Interpolate(crv, prev_biz_date)[3]

                cash_items, mul_items = [], []
                for action in actions:
                    dvd_type = action["type"]
                    amount = action["amount"]
                    if dvd_type == "cash":
                        fx_adj = self.fx_ajustment(ccy, mul, date)
                        cash_items.append(amount*fx_adj)
                    else:
                        mul_items.append(amount)

                adj = 1.0 - sum(cash_items) / prev_close
                adj *= np.prod(mul_items)
                adj_crv[date] = adj

            adj_crv = Curve(adj_crv.dates,
                            np.cumprod(adj_crv.values[::-1])[::-1])

            return ApplyAdjustments(crv, adj_crv).crop(start=start, end=end)

        return adjuster

    # -------------------------------------------------------------------------
    def corp_actions_curve(self, by_date="ex-date", start=None, end=None):
        info_by_date = collections.defaultdict(list)
        if by_date == "ex-date":
            # --- given that archived records are stored by ex-date, we can use
            #     a specialized faster query
            for _, info in self.get_history("ActionInfo", start, end):
                for item in info:
                    info_by_date[item[by_date]].append(item)
        else:
            for _, info in self.get_history("ActionInfo"):
                for item in info:
                    date = item[by_date]
                    if date < start or date > end:
                        continue
                    info_by_date[date].append(item)

        return GCurve(info_by_date.keys(), info_by_date.values())

    # -------------------------------------------------------------------------
    def dvd_curve(self, start=None, end=None):
        """
        N.B.: we only include cash dividends here.
        """
        info_crv = self.corp_actions_curve(start=start, end=end)
        dvd_crv = Curve()
        for _, value in info_crv:
            for action in value:
                if action["type"] == "cash":
                    date = action["ex-date"]
                    if date in dvd_crv:
                        dvd_crv[date] += action["amount"]
                    else:
                        dvd_crv[date] = action["amount"]

        return dvd_crv

    # -------------------------------------------------------------------------
    def fx_adjustment(self, ccy, mul, mdd):
        with EvalBlock() as eb:
            eb.change_value("Database", "MktDataDate", mdd)
            dvd_ccy = GetVal(self, "DvdCcy")

        if ccy == dvd_ccy:
            return 1.0
        else:
            # --- dvd_ccy -> ccy
            to_usd = GetVal("{0:3s}/USD".format(dvd_ccy), "SpotByDate", mdd)
            to_ccy = 1.0 / GetVal("{0:3s}/USD".format(ccy), "SpotByDate", mdd)

            return to_usd * to_ccy / mul


# -----------------------------------------------------------------------------
def prepare_for_test():
    from ..system import ufo_database
    ufo_database.prepare_for_test()
