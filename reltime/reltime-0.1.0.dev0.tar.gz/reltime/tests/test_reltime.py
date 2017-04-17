"""Run unit test for reltime module."""

import unittest
import reltime
from datetime import datetime


class TagTestCase(unittest.TestCase):
    """Test reltime.tag()."""

    def test_tag_regexp1(self):
        """Test tagging of regexp 1."""
        input1 = "five days ago"
        output1 = "<TIME>five days ago</TIME>"
        self.assertEqual(reltime.tag(input1), output1)
        input2 = "forty days later"
        output2 = "<TIME>forty days later</TIME>"
        self.assertEqual(reltime.tag(input2), output2)
        input3 = "eleven months after"
        output3 = "<TIME>eleven months after</TIME>"
        self.assertEqual(reltime.tag(input3), output3)
        input4 = "seventy five years before"
        output4 = "<TIME>seventy five years before</TIME>"
        self.assertEqual(reltime.tag(input4), output4)

    def test_tag_regexp2(self):
        """Test tagging of regexp 2."""
        input1 = "this monday"
        output1 = "<TIME>this monday</TIME>"
        self.assertEqual(reltime.tag(input1), output1)
        input2 = "next week"
        output2 = "<TIME>next week</TIME>"
        self.assertEqual(reltime.tag(input2), output2)
        input3 = "last mon"
        output3 = "<TIME>last mon</TIME>"
        self.assertEqual(reltime.tag(input3), output3)
        input4 = "next tue"
        output4 = "<TIME>next tue</TIME>"
        self.assertEqual(reltime.tag(input4), output4)
        input5 = "next january"
        output5 = "<TIME>next january</TIME>"
        self.assertEqual(reltime.tag(input5), output5)
        input6 = "this apr"
        output6 = "<TIME>this apr</TIME>"
        self.assertEqual(reltime.tag(input6), output6)

    def test_tag_regexp3(self):
        """Test tagging of regexp 3."""
        input1 = "yesterday"
        output1 = "<TIME>yesterday</TIME>"
        self.assertEqual(reltime.tag(input1), output1)
        input2 = "tomorrow"
        output2 = "<TIME>tomorrow</TIME>"
        self.assertEqual(reltime.tag(input2), output2)
        input3 = "tonite"
        output3 = "<TIME>tonite</TIME>"
        self.assertEqual(reltime.tag(input3), output3)
        input4 = "today"
        output4 = "<TIME>today</TIME>"
        self.assertEqual(reltime.tag(input4), output4)

    def test_tag_regexp4(self):
        """Test tagging of regexp 4."""
        input1 = "2016-07-25 15:26:54"
        output1 = "<TIME>2016-07-25 15:26:54</TIME>"
        self.assertEqual(reltime.tag(input1), output1)
        input2 = "7/15/2015"
        output2 = "<TIME>7/15/2015</TIME>"
        self.assertEqual(reltime.tag(input2), output2)

    def test_tag_regexp5(self):
        """Test tagging of regexp 5."""
        input1 = "2016 "
        output1 = "<TIME>2016</TIME> "
        self.assertEqual(reltime.tag(input1), output1)

    def test_tag_regexp6(self):
        """Test tagging of regexp 6."""
        input1 = " 2-15 "
        output1 = " <TIME>2-15</TIME> "
        self.assertEqual(reltime.tag(input1), output1)
        input2 = " 02/19 "
        output2 = " <TIME>02/19</TIME> "
        self.assertEqual(reltime.tag(input2), output2)

    def test_tag_regexp7(self):
        """Test tagging of regexp 7."""
        input1 = "jan 17"
        output1 = "<TIME>jan 17</TIME>"
        self.assertEqual(reltime.tag(input1), output1)
        input2 = "June 3rd"
        output2 = "<TIME>June 3</TIME>rd"
        self.assertEqual(reltime.tag(input2), output2)

    def test_tag_regexp8(self):
        """Test tagging of regexp 8."""
        input1 = " tuesday "
        output1 = " <TIME>tuesday</TIME> "
        self.assertEqual(reltime.tag(input1), output1)
        input2 = " Wed "
        output2 = " <TIME>Wed</TIME> "
        self.assertEqual(reltime.tag(input2), output2)
        input3 = " every tues "
        output3 = " <TIME>every tues</TIME> "
        self.assertEqual(reltime.tag(input3), output3)
        input4 = " thur night "
        output4 = " <TIME>thur night</TIME> "
        self.assertEqual(reltime.tag(input4), output4)

    def test_tag_regexp9(self):
        """Test tagging of regexp 9."""
        input1 = " easter "
        output1 = " <TIME>easter</TIME> "
        self.assertEqual(reltime.tag(input1), output1)
        input2 = " st pattys "
        output2 = " <TIME>st pattys</TIME> "
        self.assertEqual(reltime.tag(input2), output2)
        input3 = " new year's eve "
        output3 = " <TIME>new year's eve</TIME> "
        self.assertEqual(reltime.tag(input3), output3)

    def test_tag_regexp10(self):
        """Test tagging of regexp 10."""
        input1 = "every day"
        output1 = "<TIME>every day</TIME>"
        self.assertEqual(reltime.tag(input1), output1)
        input2 = "everyday"
        output2 = "<TIME>everyday</TIME>"
        self.assertEqual(reltime.tag(input2), output2)

    def test_tag_regexp11(self):
        """Test tagging of regexp 11."""
        input1 = "this morning"
        output1 = "<TIME>this morning</TIME>"
        self.assertEqual(reltime.tag(input1), output1)


class GroundTestCase(unittest.TestCase):
    """Test reltime.ground()."""

    def test_ground_regexp1(self):
        """Test grounding of regexp 1."""
        base_time = datetime(2015, 10, 1)
        input = "twenty two days ago is not 4 months later"
        output = [datetime(2015, 9, 9), datetime(2016, 2, 1)]
        self.assertEqual(reltime.ground(input, base_time, replace=False), output)

    def test_ground_regexp2(self):
        """Test grounding of regexp 2."""
        base_time = datetime(2015, 10, 1)
        input = "this year, next january, last mon"
        output = [datetime(2015, 10, 1), datetime(2016, 1, 1), datetime(2015, 9, 28)]
        self.assertEqual(reltime.ground(input, base_time, replace=False), output)

    def test_ground_regexp3(self):
        """Test grounding of regexp 3."""
        base_time = datetime(2015, 10, 1)
        input = "yesterday tomorrow tonite. All the times!"
        output = [datetime(2015, 9, 30), datetime(2015, 10, 2), datetime(2015, 10, 1)]
        self.assertEqual(reltime.ground(input, base_time, replace=False), output)

    def test_ground_regexp4(self):
        """Test grounding of regexp 4."""
        base_time = datetime.now()
        input = "Lets go with 2016-07-25 15:26:54 and 2015/7/15"
        output = [datetime(2016, 7, 25), datetime(2015, 7, 15)]
        self.assertEqual(reltime.ground(input, base_time, replace=False), output)

    def test_ground_regexp5(self):
        """Test grounding of regexp 5."""
        base_time = datetime(2014, 7, 25)
        input = "the years 1760 and 2015 are my favorites "
        output = [datetime(1760, 7, 25), datetime(2015, 7, 25)]
        self.assertEqual(reltime.ground(input, base_time, replace=False), output)

    def test_ground_regexp6(self):
        """Test grounding of regexp 6."""
        base_time = datetime(2012, 9, 16)
        input = " 10/14, 1/8 "
        output = [datetime(2012, 10, 14), datetime(2013, 1, 8)]
        self.assertEqual(reltime.ground(input, base_time, replace=False), output)

    def test_ground_regexp7(self):
        """Test grounding of regexp 7."""
        base_time = datetime(2012, 9, 16)
        input = "I like october 14, but I don't like January 8"
        output = [datetime(2012, 10, 14), datetime(2013, 1, 8)]
        self.assertEqual(reltime.ground(input, base_time, replace=False), output)

    def test_ground_regexp8(self):
        """Test grounding of regexp 8."""
        base_time = datetime(2016, 12, 16)
        input = "party every tuesday and sat night!"
        output = [datetime(2016, 12, 20), datetime(2016, 12, 17)]
        self.assertEqual(reltime.ground(input, base_time, replace=False), output)

    def test_ground_regexp9(self):
        """Test grounding of regexp 9."""
        base_time = datetime(2016, 1, 10)
        input = "we have specials on easter, mardi gras, and mother's day every year"
        output = [datetime(2016, 3, 27), datetime(2016, 2, 9), datetime(2016, 5, 8)]
        self.assertEqual(reltime.ground(input, base_time, replace=False), output)

    def test_ground_regexp10(self):
        """Test grounding of regexp 10."""
        base_time = datetime(2016, 12, 16)
        input = "every day everyday what a day"
        output = [datetime(2016, 12, 16), datetime(2016, 12, 16)]
        self.assertEqual(reltime.ground(input, base_time), output)

    def test_ground_regexp11(self):
        """Test grounding of regexp 11."""
        base_time = datetime(2016, 12, 16)
        input = "this morning I had pancakes for breakfast"
        output = [datetime(2016, 12, 16)]
        self.assertEqual(reltime.ground(input, base_time, replace=False), output)

    def test_ground_replace(self):
        """Test Replace==True."""
        base_time = datetime(2016, 12, 16)
        input = "this morning I had pancakes for breakfast"
        output = ("GroundedTime I had pancakes for breakfast", [datetime(2016, 12, 16)])
        self.assertEqual(reltime.ground(input, base_time, replace=True), output)

    def big_test(self):
        """Test lots of stuff."""
        base_time = datetime(2016, 7, 27)
        input = "First Street Gallery Logo [http://r20.rs6.net/tn.jsp?f=001HzXGe-7Pq8-zlt4lLYuOB6gUgJEJfvwghspnK22oQib-APXPI0NJvw4FOyJ-4xeNZav5OPkxIyOQsfyuIrTtgvAciUdekfII_GAgmrQY6pkKX4UTFyOcNhtkQV1oqKapx2EbiJslP4Zp5SqYvrqZdv0wFGShjGfD3UMjN4Ckd0yUWWxJbMIVgb_PPTZtDMw_Zsz03Tp-yG7j_ZOA6KYh-yLemq0T9-WHTOzSRKM24GCpYZ7iuEuiPlJVWWnUxGq9r4TC4_t4W7aKvE-GoYd5iqwYE66IkjLAoAa0_GfWyxydRs3gG_MSGlZ7mk9JpCYyt739f5YyHJJZU_Rsq1LXEZ3aop9c-FXxcAT75giKC-YFJDdC6i62PgN4lBbmb8bSO7rw9o29TDI=&c=ThoQa9dOxQlD2qj4Bk8tMgNr0wZ2zRBFnBt1Dn8ZUxdsS9zF7nXBzw==&ch=EpYrBgwRbXI3pGGC5BCaG-UyW2nKlux6va6oeTixMap505rIlgSM5A==]\r\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\r\n\r\nOPENING RECEPTION THIS THURSDAY\r\n\r\nJULY 23, 6-8 PM\r\n2015\r\nMFA NATIONAL EXHIBITION\r\n\r\nThomas Wharton, Martini, digital print on canvas, 9 x 8 inches\r\n\r\nJULY 23 - AUGUST 14, 2015\r\n\r\nFirst Street Gallery proudly presents our fifth annual MFA NATIONAL EXHIBITION.\r\n\r\nThis exhibition highlights the vast reach of fine arts teaching throughout the United\r\nStates. The competition is open to all current and former MFA graduates within the\r\npast three years. Our Juror, David A. Ross, former Director of The Whitney Museum\r\nof American Art and The San Francisco Museum of Modern Art, has a 40-year career\r\n as a museum professional and educator. He is currently the Chair of the MFA Art\r\n Practice Program at SVA.\r\n\r\nARTISTS: Danny Baskin (UARK), Kimberly Becker (Heartwood), William Chambers (Mass\r\nArt), Donna Cleary (SVA), Sarah Dahlinger (Ohio), Jason Egitto (Syracuse), Lindsey\r\nElsey (Clemson), Dan Fenstermacher (SJSU), En Iwamura (Clemson), Richard James (KU),\r\nAnnie Johnston (UT-Austin), June Korea (SVA), James Lambert (Mass Art), Junko Ledneva\r\n(UAF), J. Myszka Lewis (UW-Madison), Wilson Parry (Parsons), Veronica Perez (MECA),\r\nDanette Pratt (Ohio), Jason Schwab (CCAD), Thomas Wharton (UT-Knoxville).\r\n\r\nFor more info please visit the 2015 MFA NATIONAL EXHIBITION album on our Facebook\r\npage. [http://r20.rs6.net/tn.jsp?f=001HzXGe-7Pq8-zlt4lLYuOB6gUgJEJfvwghspnK22oQib-APXPI0NJv4vTi_KIZjl5AqU4Nfz6z3iB6MWBRsf5QHv-4T8IUSmtSVEItfj8TEaoluebDWPmWv8D8ayfdc-wgMtgkfoRJvH4e6-s0HG2jeuCsdSgT2q8uK4gve2K-u9S0X-AI-dtxpp72dGVY3orPDp-aCm-Gm8b_bp2B_Kh4JXLtEQn1qL6y-T3w2wKAO_Ijb4WKJM54g==&c=ThoQa9dOxQlD2qj4Bk8tMgNr0wZ2zRBFnBt1Dn8ZUxdsS9zF7nXBzw==&ch=EpYrBgwRbXI3pGGC5BCaG-UyW2nKlux6va6oeTixMap505rIlgSM5A==]\r\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\r\n\r\nSummer Gallery Hours: 11 am - 6 pm, Monday through Friday\r\n\r\n526 West 26th Street, Suite 209, New York, New York 10001\r\n\r\n646-336-8053  646-336-8054 (fax)\r\n\r\nFirst Street Gallery is located in the heart of Chelsea, NYC between 10th & 11th\r\n Avenues.\r\n\r\n[Nearest Subways: C,E,R,1,F,V to 23rd St. - crosstown bus to 10th Ave.\r\n\r\nNearest Buses:  9th Avenue (#11), 8th Avenue (#10)\r\n\r\nFSG Gallery Location (Larger) [http://r20.rs6.net/tn.jsp?f=001HzXGe-7Pq8-zlt4lLYuOB6gUgJEJfvwghspnK22oQib-APXPI0NJv9jYInswQQnIHf9mxdYCKS9ToMDZN4irVXvv4MwYSp1ZjfI50OE1Y2967Oub1kz0wjySxJKj3ezzVdedGVNfhDs5KjNsU9YoKh10QUAKhOk2nGAC8Q3a-pWv97RCatjUAVBM7WMT7AJGSA0OBWeX7bTcrFyYvR22bYo1ae6kN-1gjlmyP9dQd1jUJV5ng7KzM9Z7llU0lf0gDIaVkcQCXHlri0iurEDQR7gKLHqt7HJ7SfdJWTvozHRJguONwJrFQCPxGS66mpFz3RKqny7gfvk7czIGzfJSeRRvkSn7iEy9Kvx0EYnRs4nyU2hD7MGLMGu_2JoxEqESH5h2evkMkSlz4NrOgAxrbyWih5sIS20qZvAB0n4Cvk1oBCq5iDtSNqvYzEhsA7y-FyJu8Up_FqzSNgQRJXWtavzSWlyedsQrI-0Ba23n0-7kSZn_x3gYecTQBXoa0ckLN-AOoBARMQQZCbjKbNCuAycfbYPGXr0s2QEDSWWApQbxArz-y09esTi-AqSdYRTvucIUE-CUuF8tvVT-g5HH0rKhCL_rpFOu92d0KATA6LAzUyJ1qNsRfPwLDDnFP-1d55XOjwVjjgFGJiuyxtHLNzk1rb6zm8r56l04_kJGQtDxirkS2EiQPKW6h_1SztVO0JIbrbkp2IUsLlRGL9PYCI7EGKe1rr25JbA9wduFJ-Yb53F_AAlJntavGutIdJAoY1AegpwvCGDCnFFeAB5VorTmDJs1uSldglx67lCigZSjpMySvnDhNllN1py8p6mfbOXxPxCmWynCeOvB5ltaFtXEP0bMcGW_9cZCoGsww42OlegTjkOyxA==&c=ThoQa9dOxQlD2qj4Bk8tMgNr0wZ2zRBFnBt1Dn8ZUxdsS9zF7nXBzw==&ch=EpYrBgwRbXI3pGGC5BCaG-UyW2nKlux6va6oeTixMap505rIlgSM5A==]\r\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\r\n\r\nJoin Our Mailing List [http://visitor.constantcontact.com/email.jsp?m=1103049216003]\r\n\r\ns 2001-2011 First Street Gallery\r\n\r\nArtist images copyrighted by the individual artists. All rights reserved.\r\n\r\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\r\nForward email\r\nhttp://ui.constantcontact.com/sa/fwtf.jsp?llr=dauwnjdab&m=1103049216003&ea=$events@liveapp.com$&a=1121719149089\r\n\r\nThis email was sent to events@liveapp.com by firststreetgallery@earthlink.net.\r\n\r\nUpdate Profile/Email Address\r\nhttp://visitor.constantcontact.com/do?p=oo&m=001JtllHKXFqd_bBq0Avb7lPA%3D%3D&ch=0d2a4930-e9f2-11e4-af5b-d4ae52754aa9&ca=cd656f5e-7d82-4a66-9e64-9ee1bb170ae9\r\n\r\n\r\nInstant removal with SafeUnsubscribe(TM)\r\nhttp://visitor.constantcontact.com/do?p=un&m=001JtllHKXFqd_bBq0Avb7lPA%3D%3D&ch=0d2a4930-e9f2-11e4-af5b-d4ae52754aa9&ca=cd656f5e-7d82-4a66-9e64-9ee1bb170ae9\r\n\r\n\r\nPrivacy Policy:\r\nhttp://ui.constantcontact.com/roving/CCPrivacyPolicy.jsp\r\n\r\nOnline Marketing by\r\nConstant Contact(R)\r\nwww.constantcontact.com\r\n\r\n\r\n\r\nFirst Street Gallery | 526 W. 26th Street, Suite 209 | New York | NY | 10001"
        output = ([datetime(2016, 7, 28, 0, 0), datetime(2017, 6, 8, 0, 0), datetime(2016, 7, 23, 0, 0),
                  datetime(2016, 7, 23, 0, 0), datetime(2016, 8, 14, 0, 0), datetime(2016, 8, 1, 0, 0),
                  datetime(2016, 7, 29, 0, 0), datetime(2015, 7, 27, 0, 0), datetime(2015, 7, 27, 0, 0),
                  datetime(2015, 7, 27, 0, 0)])
        self.assertEqual(reltime.ground(input, base_time), output)

if __name__ == '__main__':
    unittest.main()