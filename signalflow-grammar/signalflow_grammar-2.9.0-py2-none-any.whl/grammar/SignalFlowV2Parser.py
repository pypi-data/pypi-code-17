# Generated from grammar/SignalFlowV2Parser.g4 by ANTLR 4.5.2
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO

def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3")
        buf.write(u"L\u0220\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t")
        buf.write(u"\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write(u"\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4")
        buf.write(u"\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30")
        buf.write(u"\t\30\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t")
        buf.write(u"\35\4\36\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$")
        buf.write(u"\t$\4%\t%\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t")
        buf.write(u",\4-\t-\4.\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63")
        buf.write(u"\t\63\4\64\t\64\4\65\t\65\4\66\t\66\3\2\3\2\7\2o\n\2")
        buf.write(u"\f\2\16\2r\13\2\3\2\3\2\3\3\3\3\7\3x\n\3\f\3\16\3{\13")
        buf.write(u"\3\3\3\3\3\3\4\3\4\3\4\3\4\5\4\u0083\n\4\3\4\5\4\u0086")
        buf.write(u"\n\4\3\4\3\4\3\5\6\5\u008b\n\5\r\5\16\5\u008c\3\6\3\6")
        buf.write(u"\3\6\3\7\3\7\3\7\3\7\3\7\3\7\3\b\3\b\5\b\u009a\n\b\3")
        buf.write(u"\b\3\b\3\t\3\t\3\t\7\t\u00a1\n\t\f\t\16\t\u00a4\13\t")
        buf.write(u"\3\n\3\n\3\n\5\n\u00a9\n\n\3\13\3\13\3\f\3\f\5\f\u00af")
        buf.write(u"\n\f\3\r\3\r\3\r\7\r\u00b4\n\r\f\r\16\r\u00b7\13\r\3")
        buf.write(u"\r\5\r\u00ba\n\r\3\r\3\r\3\16\3\16\3\16\3\16\5\16\u00c2")
        buf.write(u"\n\16\3\17\3\17\3\17\5\17\u00c7\n\17\3\17\3\17\3\20\3")
        buf.write(u"\20\3\20\7\20\u00ce\n\20\f\20\16\20\u00d1\13\20\3\20")
        buf.write(u"\5\20\u00d4\n\20\3\21\3\21\5\21\u00d8\n\21\3\22\3\22")
        buf.write(u"\3\22\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\5")
        buf.write(u"\23\u00e6\n\23\3\24\3\24\3\24\5\24\u00eb\n\24\3\25\3")
        buf.write(u"\25\3\25\5\25\u00f0\n\25\3\26\3\26\3\26\7\26\u00f5\n")
        buf.write(u"\26\f\26\16\26\u00f8\13\26\3\26\5\26\u00fb\n\26\3\27")
        buf.write(u"\3\27\3\27\7\27\u0100\n\27\f\27\16\27\u0103\13\27\3\30")
        buf.write(u"\3\30\3\30\7\30\u0108\n\30\f\30\16\30\u010b\13\30\3\31")
        buf.write(u"\3\31\5\31\u010f\n\31\3\32\3\32\3\33\3\33\3\33\5\33\u0116")
        buf.write(u"\n\33\3\34\3\34\3\34\3\34\5\34\u011c\n\34\3\35\3\35\3")
        buf.write(u"\35\3\35\3\35\3\35\3\35\3\35\3\35\7\35\u0127\n\35\f\35")
        buf.write(u"\16\35\u012a\13\35\3\35\3\35\3\35\5\35\u012f\n\35\3\36")
        buf.write(u"\3\36\3\36\3\36\6\36\u0135\n\36\r\36\16\36\u0136\3\36")
        buf.write(u"\3\36\5\36\u013b\n\36\3\37\3\37\3\37\3\37\3\37\3\37\5")
        buf.write(u"\37\u0143\n\37\3\37\5\37\u0146\n\37\3 \3 \3 \3 \3 \3")
        buf.write(u"!\3!\3!\7!\u0150\n!\f!\16!\u0153\13!\3\"\3\"\3\"\7\"")
        buf.write(u"\u0158\n\"\f\"\16\"\u015b\13\"\3#\3#\3#\5#\u0160\n#\3")
        buf.write(u"$\3$\3$\3$\3$\3$\3$\3$\3$\3$\3$\5$\u016d\n$\3$\7$\u0170")
        buf.write(u"\n$\f$\16$\u0173\13$\3%\3%\3%\7%\u0178\n%\f%\16%\u017b")
        buf.write(u"\13%\3&\3&\3&\7&\u0180\n&\f&\16&\u0183\13&\3\'\3\'\3")
        buf.write(u"\'\7\'\u0188\n\'\f\'\16\'\u018b\13\'\3(\3(\3(\3(\3(\7")
        buf.write(u"(\u0192\n(\f(\16(\u0195\13(\3)\3)\3)\7)\u019a\n)\f)\16")
        buf.write(u")\u019d\13)\3*\3*\3*\7*\u01a2\n*\f*\16*\u01a5\13*\3+")
        buf.write(u"\3+\3+\5+\u01aa\n+\3,\3,\3,\5,\u01af\n,\3-\3-\7-\u01b3")
        buf.write(u"\n-\f-\16-\u01b6\13-\3.\3.\3.\3.\3.\3.\3.\6.\u01bf\n")
        buf.write(u".\r.\16.\u01c0\3.\3.\3.\5.\u01c6\n.\3/\3/\5/\u01ca\n")
        buf.write(u"/\3/\3/\3/\3/\3/\3/\3/\5/\u01d3\n/\3\60\3\60\5\60\u01d7")
        buf.write(u"\n\60\3\60\3\60\5\60\u01db\n\60\5\60\u01dd\n\60\3\61")
        buf.write(u"\3\61\3\61\3\61\7\61\u01e3\n\61\f\61\16\61\u01e6\13\61")
        buf.write(u"\5\61\u01e8\n\61\3\61\3\61\3\62\3\62\5\62\u01ee\n\62")
        buf.write(u"\3\62\3\62\3\63\3\63\3\63\3\63\3\63\3\63\3\63\3\63\3")
        buf.write(u"\63\7\63\u01fb\n\63\f\63\16\63\u01fe\13\63\3\63\5\63")
        buf.write(u"\u0201\n\63\5\63\u0203\n\63\3\63\3\63\3\64\3\64\3\64")
        buf.write(u"\7\64\u020a\n\64\f\64\16\64\u020d\13\64\3\64\5\64\u0210")
        buf.write(u"\n\64\3\65\3\65\3\65\7\65\u0215\n\65\f\65\16\65\u0218")
        buf.write(u"\13\65\3\66\3\66\5\66\u021c\n\66\3\66\3\66\3\66\2\2\67")
        buf.write(u"\2\4\6\b\n\f\16\20\22\24\26\30\32\34\36 \"$&(*,.\60\62")
        buf.write(u"\64\668:<>@BDFHJLNPRTVXZ\\^`bdfhj\2\6\3\3$$\3\2:;\4\2")
        buf.write(u"++<<\4\2:;==\u023f\2p\3\2\2\2\4u\3\2\2\2\6~\3\2\2\2\b")
        buf.write(u"\u008a\3\2\2\2\n\u008e\3\2\2\2\f\u0091\3\2\2\2\16\u0097")
        buf.write(u"\3\2\2\2\20\u009d\3\2\2\2\22\u00a5\3\2\2\2\24\u00aa\3")
        buf.write(u"\2\2\2\26\u00ae\3\2\2\2\30\u00b0\3\2\2\2\32\u00c1\3\2")
        buf.write(u"\2\2\34\u00c6\3\2\2\2\36\u00ca\3\2\2\2 \u00d7\3\2\2\2")
        buf.write(u"\"\u00d9\3\2\2\2$\u00dc\3\2\2\2&\u00e7\3\2\2\2(\u00ec")
        buf.write(u"\3\2\2\2*\u00f1\3\2\2\2,\u00fc\3\2\2\2.\u0104\3\2\2\2")
        buf.write(u"\60\u010c\3\2\2\2\62\u0110\3\2\2\2\64\u0115\3\2\2\2\66")
        buf.write(u"\u0117\3\2\2\28\u011d\3\2\2\2:\u013a\3\2\2\2<\u0145\3")
        buf.write(u"\2\2\2>\u0147\3\2\2\2@\u014c\3\2\2\2B\u0154\3\2\2\2D")
        buf.write(u"\u015f\3\2\2\2F\u0161\3\2\2\2H\u0174\3\2\2\2J\u017c\3")
        buf.write(u"\2\2\2L\u0184\3\2\2\2N\u018c\3\2\2\2P\u0196\3\2\2\2R")
        buf.write(u"\u019e\3\2\2\2T\u01a9\3\2\2\2V\u01ab\3\2\2\2X\u01b0\3")
        buf.write(u"\2\2\2Z\u01c5\3\2\2\2\\\u01d2\3\2\2\2^\u01dc\3\2\2\2")
        buf.write(u"`\u01de\3\2\2\2b\u01eb\3\2\2\2d\u01f1\3\2\2\2f\u0206")
        buf.write(u"\3\2\2\2h\u0211\3\2\2\2j\u021b\3\2\2\2lo\7$\2\2mo\5\26")
        buf.write(u"\f\2nl\3\2\2\2nm\3\2\2\2or\3\2\2\2pn\3\2\2\2pq\3\2\2")
        buf.write(u"\2qs\3\2\2\2rp\3\2\2\2st\7\2\2\3t\3\3\2\2\2uy\5f\64\2")
        buf.write(u"vx\7$\2\2wv\3\2\2\2x{\3\2\2\2yw\3\2\2\2yz\3\2\2\2z|\3")
        buf.write(u"\2\2\2{y\3\2\2\2|}\7\2\2\3}\5\3\2\2\2~\177\7G\2\2\177")
        buf.write(u"\u0085\5.\30\2\u0080\u0082\7,\2\2\u0081\u0083\5h\65\2")
        buf.write(u"\u0082\u0081\3\2\2\2\u0082\u0083\3\2\2\2\u0083\u0084")
        buf.write(u"\3\2\2\2\u0084\u0086\7-\2\2\u0085\u0080\3\2\2\2\u0085")
        buf.write(u"\u0086\3\2\2\2\u0086\u0087\3\2\2\2\u0087\u0088\7$\2\2")
        buf.write(u"\u0088\7\3\2\2\2\u0089\u008b\5\6\4\2\u008a\u0089\3\2")
        buf.write(u"\2\2\u008b\u008c\3\2\2\2\u008c\u008a\3\2\2\2\u008c\u008d")
        buf.write(u"\3\2\2\2\u008d\t\3\2\2\2\u008e\u008f\5\b\5\2\u008f\u0090")
        buf.write(u"\5\f\7\2\u0090\13\3\2\2\2\u0091\u0092\7\3\2\2\u0092\u0093")
        buf.write(u"\7%\2\2\u0093\u0094\5\16\b\2\u0094\u0095\7/\2\2\u0095")
        buf.write(u"\u0096\5:\36\2\u0096\r\3\2\2\2\u0097\u0099\7,\2\2\u0098")
        buf.write(u"\u009a\5\20\t\2\u0099\u0098\3\2\2\2\u0099\u009a\3\2\2")
        buf.write(u"\2\u009a\u009b\3\2\2\2\u009b\u009c\7-\2\2\u009c\17\3")
        buf.write(u"\2\2\2\u009d\u00a2\5\22\n\2\u009e\u009f\7.\2\2\u009f")
        buf.write(u"\u00a1\5\22\n\2\u00a0\u009e\3\2\2\2\u00a1\u00a4\3\2\2")
        buf.write(u"\2\u00a2\u00a0\3\2\2\2\u00a2\u00a3\3\2\2\2\u00a3\21\3")
        buf.write(u"\2\2\2\u00a4\u00a2\3\2\2\2\u00a5\u00a8\5\24\13\2\u00a6")
        buf.write(u"\u00a7\7\62\2\2\u00a7\u00a9\5<\37\2\u00a8\u00a6\3\2\2")
        buf.write(u"\2\u00a8\u00a9\3\2\2\2\u00a9\23\3\2\2\2\u00aa\u00ab\7")
        buf.write(u"%\2\2\u00ab\25\3\2\2\2\u00ac\u00af\5\30\r\2\u00ad\u00af")
        buf.write(u"\5\64\33\2\u00ae\u00ac\3\2\2\2\u00ae\u00ad\3\2\2\2\u00af")
        buf.write(u"\27\3\2\2\2\u00b0\u00b5\5\32\16\2\u00b1\u00b2\7\60\2")
        buf.write(u"\2\u00b2\u00b4\5\32\16\2\u00b3\u00b1\3\2\2\2\u00b4\u00b7")
        buf.write(u"\3\2\2\2\u00b5\u00b3\3\2\2\2\u00b5\u00b6\3\2\2\2\u00b6")
        buf.write(u"\u00b9\3\2\2\2\u00b7\u00b5\3\2\2\2\u00b8\u00ba\7\60\2")
        buf.write(u"\2\u00b9\u00b8\3\2\2\2\u00b9\u00ba\3\2\2\2\u00ba\u00bb")
        buf.write(u"\3\2\2\2\u00bb\u00bc\t\2\2\2\u00bc\31\3\2\2\2\u00bd\u00c2")
        buf.write(u"\5\34\17\2\u00be\u00c2\5\62\32\2\u00bf\u00c2\5 \21\2")
        buf.write(u"\u00c0\u00c2\5\66\34\2\u00c1\u00bd\3\2\2\2\u00c1\u00be")
        buf.write(u"\3\2\2\2\u00c1\u00bf\3\2\2\2\u00c1\u00c0\3\2\2\2\u00c2")
        buf.write(u"\33\3\2\2\2\u00c3\u00c4\5\36\20\2\u00c4\u00c5\7\62\2")
        buf.write(u"\2\u00c5\u00c7\3\2\2\2\u00c6\u00c3\3\2\2\2\u00c6\u00c7")
        buf.write(u"\3\2\2\2\u00c7\u00c8\3\2\2\2\u00c8\u00c9\5f\64\2\u00c9")
        buf.write(u"\35\3\2\2\2\u00ca\u00cf\7%\2\2\u00cb\u00cc\7.\2\2\u00cc")
        buf.write(u"\u00ce\7%\2\2\u00cd\u00cb\3\2\2\2\u00ce\u00d1\3\2\2\2")
        buf.write(u"\u00cf\u00cd\3\2\2\2\u00cf\u00d0\3\2\2\2\u00d0\u00d3")
        buf.write(u"\3\2\2\2\u00d1\u00cf\3\2\2\2\u00d2\u00d4\7.\2\2\u00d3")
        buf.write(u"\u00d2\3\2\2\2\u00d3\u00d4\3\2\2\2\u00d4\37\3\2\2\2\u00d5")
        buf.write(u"\u00d8\5\"\22\2\u00d6\u00d8\5$\23\2\u00d7\u00d5\3\2\2")
        buf.write(u"\2\u00d7\u00d6\3\2\2\2\u00d8!\3\2\2\2\u00d9\u00da\7\7")
        buf.write(u"\2\2\u00da\u00db\5,\27\2\u00db#\3\2\2\2\u00dc\u00dd\7")
        buf.write(u"\6\2\2\u00dd\u00de\5.\30\2\u00de\u00e5\7\7\2\2\u00df")
        buf.write(u"\u00e6\7+\2\2\u00e0\u00e1\7,\2\2\u00e1\u00e2\5*\26\2")
        buf.write(u"\u00e2\u00e3\7-\2\2\u00e3\u00e6\3\2\2\2\u00e4\u00e6\5")
        buf.write(u"*\26\2\u00e5\u00df\3\2\2\2\u00e5\u00e0\3\2\2\2\u00e5")
        buf.write(u"\u00e4\3\2\2\2\u00e6%\3\2\2\2\u00e7\u00ea\7%\2\2\u00e8")
        buf.write(u"\u00e9\7\b\2\2\u00e9\u00eb\7%\2\2\u00ea\u00e8\3\2\2\2")
        buf.write(u"\u00ea\u00eb\3\2\2\2\u00eb\'\3\2\2\2\u00ec\u00ef\5.\30")
        buf.write(u"\2\u00ed\u00ee\7\b\2\2\u00ee\u00f0\7%\2\2\u00ef\u00ed")
        buf.write(u"\3\2\2\2\u00ef\u00f0\3\2\2\2\u00f0)\3\2\2\2\u00f1\u00f6")
        buf.write(u"\5&\24\2\u00f2\u00f3\7.\2\2\u00f3\u00f5\5&\24\2\u00f4")
        buf.write(u"\u00f2\3\2\2\2\u00f5\u00f8\3\2\2\2\u00f6\u00f4\3\2\2")
        buf.write(u"\2\u00f6\u00f7\3\2\2\2\u00f7\u00fa\3\2\2\2\u00f8\u00f6")
        buf.write(u"\3\2\2\2\u00f9\u00fb\7.\2\2\u00fa\u00f9\3\2\2\2\u00fa")
        buf.write(u"\u00fb\3\2\2\2\u00fb+\3\2\2\2\u00fc\u0101\5(\25\2\u00fd")
        buf.write(u"\u00fe\7.\2\2\u00fe\u0100\5(\25\2\u00ff\u00fd\3\2\2\2")
        buf.write(u"\u0100\u0103\3\2\2\2\u0101\u00ff\3\2\2\2\u0101\u0102")
        buf.write(u"\3\2\2\2\u0102-\3\2\2\2\u0103\u0101\3\2\2\2\u0104\u0109")
        buf.write(u"\7%\2\2\u0105\u0106\7)\2\2\u0106\u0108\7%\2\2\u0107\u0105")
        buf.write(u"\3\2\2\2\u0108\u010b\3\2\2\2\u0109\u0107\3\2\2\2\u0109")
        buf.write(u"\u010a\3\2\2\2\u010a/\3\2\2\2\u010b\u0109\3\2\2\2\u010c")
        buf.write(u"\u010e\7\4\2\2\u010d\u010f\5f\64\2\u010e\u010d\3\2\2")
        buf.write(u"\2\u010e\u010f\3\2\2\2\u010f\61\3\2\2\2\u0110\u0111\5")
        buf.write(u"\60\31\2\u0111\63\3\2\2\2\u0112\u0116\58\35\2\u0113\u0116")
        buf.write(u"\5\f\7\2\u0114\u0116\5\n\6\2\u0115\u0112\3\2\2\2\u0115")
        buf.write(u"\u0113\3\2\2\2\u0115\u0114\3\2\2\2\u0116\65\3\2\2\2\u0117")
        buf.write(u"\u0118\7\13\2\2\u0118\u011b\5<\37\2\u0119\u011a\7.\2")
        buf.write(u"\2\u011a\u011c\5<\37\2\u011b\u0119\3\2\2\2\u011b\u011c")
        buf.write(u"\3\2\2\2\u011c\67\3\2\2\2\u011d\u011e\7\f\2\2\u011e\u011f")
        buf.write(u"\5<\37\2\u011f\u0120\7/\2\2\u0120\u0128\5:\36\2\u0121")
        buf.write(u"\u0122\7\r\2\2\u0122\u0123\5<\37\2\u0123\u0124\7/\2\2")
        buf.write(u"\u0124\u0125\5:\36\2\u0125\u0127\3\2\2\2\u0126\u0121")
        buf.write(u"\3\2\2\2\u0127\u012a\3\2\2\2\u0128\u0126\3\2\2\2\u0128")
        buf.write(u"\u0129\3\2\2\2\u0129\u012e\3\2\2\2\u012a\u0128\3\2\2")
        buf.write(u"\2\u012b\u012c\7\16\2\2\u012c\u012d\7/\2\2\u012d\u012f")
        buf.write(u"\5:\36\2\u012e\u012b\3\2\2\2\u012e\u012f\3\2\2\2\u012f")
        buf.write(u"9\3\2\2\2\u0130\u013b\5\30\r\2\u0131\u0132\7$\2\2\u0132")
        buf.write(u"\u0134\7K\2\2\u0133\u0135\5\26\f\2\u0134\u0133\3\2\2")
        buf.write(u"\2\u0135\u0136\3\2\2\2\u0136\u0134\3\2\2\2\u0136\u0137")
        buf.write(u"\3\2\2\2\u0137\u0138\3\2\2\2\u0138\u0139\7L\2\2\u0139")
        buf.write(u"\u013b\3\2\2\2\u013a\u0130\3\2\2\2\u013a\u0131\3\2\2")
        buf.write(u"\2\u013b;\3\2\2\2\u013c\u0142\5@!\2\u013d\u013e\7\f\2")
        buf.write(u"\2\u013e\u013f\5@!\2\u013f\u0140\7\16\2\2\u0140\u0141")
        buf.write(u"\5<\37\2\u0141\u0143\3\2\2\2\u0142\u013d\3\2\2\2\u0142")
        buf.write(u"\u0143\3\2\2\2\u0143\u0146\3\2\2\2\u0144\u0146\5> \2")
        buf.write(u"\u0145\u013c\3\2\2\2\u0145\u0144\3\2\2\2\u0146=\3\2\2")
        buf.write(u"\2\u0147\u0148\7\26\2\2\u0148\u0149\7%\2\2\u0149\u014a")
        buf.write(u"\7/\2\2\u014a\u014b\5<\37\2\u014b?\3\2\2\2\u014c\u0151")
        buf.write(u"\5B\"\2\u014d\u014e\7\27\2\2\u014e\u0150\5B\"\2\u014f")
        buf.write(u"\u014d\3\2\2\2\u0150\u0153\3\2\2\2\u0151\u014f\3\2\2")
        buf.write(u"\2\u0151\u0152\3\2\2\2\u0152A\3\2\2\2\u0153\u0151\3\2")
        buf.write(u"\2\2\u0154\u0159\5D#\2\u0155\u0156\7\30\2\2\u0156\u0158")
        buf.write(u"\5D#\2\u0157\u0155\3\2\2\2\u0158\u015b\3\2\2\2\u0159")
        buf.write(u"\u0157\3\2\2\2\u0159\u015a\3\2\2\2\u015aC\3\2\2\2\u015b")
        buf.write(u"\u0159\3\2\2\2\u015c\u015d\7\31\2\2\u015d\u0160\5D#\2")
        buf.write(u"\u015e\u0160\5F$\2\u015f\u015c\3\2\2\2\u015f\u015e\3")
        buf.write(u"\2\2\2\u0160E\3\2\2\2\u0161\u0171\5H%\2\u0162\u016d\7")
        buf.write(u"@\2\2\u0163\u016d\7D\2\2\u0164\u016d\7B\2\2\u0165\u016d")
        buf.write(u"\7E\2\2\u0166\u016d\7F\2\2\u0167\u016d\7A\2\2\u0168\u016d")
        buf.write(u"\7C\2\2\u0169\u016d\7\32\2\2\u016a\u016b\7\32\2\2\u016b")
        buf.write(u"\u016d\7\31\2\2\u016c\u0162\3\2\2\2\u016c\u0163\3\2\2")
        buf.write(u"\2\u016c\u0164\3\2\2\2\u016c\u0165\3\2\2\2\u016c\u0166")
        buf.write(u"\3\2\2\2\u016c\u0167\3\2\2\2\u016c\u0168\3\2\2\2\u016c")
        buf.write(u"\u0169\3\2\2\2\u016c\u016a\3\2\2\2\u016d\u016e\3\2\2")
        buf.write(u"\2\u016e\u0170\5H%\2\u016f\u016c\3\2\2\2\u0170\u0173")
        buf.write(u"\3\2\2\2\u0171\u016f\3\2\2\2\u0171\u0172\3\2\2\2\u0172")
        buf.write(u"G\3\2\2\2\u0173\u0171\3\2\2\2\u0174\u0179\5J&\2\u0175")
        buf.write(u"\u0176\7\65\2\2\u0176\u0178\5J&\2\u0177\u0175\3\2\2\2")
        buf.write(u"\u0178\u017b\3\2\2\2\u0179\u0177\3\2\2\2\u0179\u017a")
        buf.write(u"\3\2\2\2\u017aI\3\2\2\2\u017b\u0179\3\2\2\2\u017c\u0181")
        buf.write(u"\5L\'\2\u017d\u017e\7\66\2\2\u017e\u0180\5L\'\2\u017f")
        buf.write(u"\u017d\3\2\2\2\u0180\u0183\3\2\2\2\u0181\u017f\3\2\2")
        buf.write(u"\2\u0181\u0182\3\2\2\2\u0182K\3\2\2\2\u0183\u0181\3\2")
        buf.write(u"\2\2\u0184\u0189\5N(\2\u0185\u0186\7\67\2\2\u0186\u0188")
        buf.write(u"\5N(\2\u0187\u0185\3\2\2\2\u0188\u018b\3\2\2\2\u0189")
        buf.write(u"\u0187\3\2\2\2\u0189\u018a\3\2\2\2\u018aM\3\2\2\2\u018b")
        buf.write(u"\u0189\3\2\2\2\u018c\u0193\5P)\2\u018d\u018e\78\2\2\u018e")
        buf.write(u"\u0192\5P)\2\u018f\u0190\79\2\2\u0190\u0192\5P)\2\u0191")
        buf.write(u"\u018d\3\2\2\2\u0191\u018f\3\2\2\2\u0192\u0195\3\2\2")
        buf.write(u"\2\u0193\u0191\3\2\2\2\u0193\u0194\3\2\2\2\u0194O\3\2")
        buf.write(u"\2\2\u0195\u0193\3\2\2\2\u0196\u019b\5R*\2\u0197\u0198")
        buf.write(u"\t\3\2\2\u0198\u019a\5R*\2\u0199\u0197\3\2\2\2\u019a")
        buf.write(u"\u019d\3\2\2\2\u019b\u0199\3\2\2\2\u019b\u019c\3\2\2")
        buf.write(u"\2\u019cQ\3\2\2\2\u019d\u019b\3\2\2\2\u019e\u01a3\5T")
        buf.write(u"+\2\u019f\u01a0\t\4\2\2\u01a0\u01a2\5T+\2\u01a1\u019f")
        buf.write(u"\3\2\2\2\u01a2\u01a5\3\2\2\2\u01a3\u01a1\3\2\2\2\u01a3")
        buf.write(u"\u01a4\3\2\2\2\u01a4S\3\2\2\2\u01a5\u01a3\3\2\2\2\u01a6")
        buf.write(u"\u01a7\t\5\2\2\u01a7\u01aa\5T+\2\u01a8\u01aa\5V,\2\u01a9")
        buf.write(u"\u01a6\3\2\2\2\u01a9\u01a8\3\2\2\2\u01aaU\3\2\2\2\u01ab")
        buf.write(u"\u01ae\5X-\2\u01ac\u01ad\7\61\2\2\u01ad\u01af\5T+\2\u01ae")
        buf.write(u"\u01ac\3\2\2\2\u01ae\u01af\3\2\2\2\u01afW\3\2\2\2\u01b0")
        buf.write(u"\u01b4\5Z.\2\u01b1\u01b3\5\\/\2\u01b2\u01b1\3\2\2\2\u01b3")
        buf.write(u"\u01b6\3\2\2\2\u01b4\u01b2\3\2\2\2\u01b4\u01b5\3\2\2")
        buf.write(u"\2\u01b5Y\3\2\2\2\u01b6\u01b4\3\2\2\2\u01b7\u01c6\5`")
        buf.write(u"\61\2\u01b8\u01c6\5b\62\2\u01b9\u01c6\5d\63\2\u01ba\u01c6")
        buf.write(u"\7%\2\2\u01bb\u01c6\7\'\2\2\u01bc\u01c6\7(\2\2\u01bd")
        buf.write(u"\u01bf\7&\2\2\u01be\u01bd\3\2\2\2\u01bf\u01c0\3\2\2\2")
        buf.write(u"\u01c0\u01be\3\2\2\2\u01c0\u01c1\3\2\2\2\u01c1\u01c6")
        buf.write(u"\3\2\2\2\u01c2\u01c6\7\33\2\2\u01c3\u01c6\7\34\2\2\u01c4")
        buf.write(u"\u01c6\7\35\2\2\u01c5\u01b7\3\2\2\2\u01c5\u01b8\3\2\2")
        buf.write(u"\2\u01c5\u01b9\3\2\2\2\u01c5\u01ba\3\2\2\2\u01c5\u01bb")
        buf.write(u"\3\2\2\2\u01c5\u01bc\3\2\2\2\u01c5\u01be\3\2\2\2\u01c5")
        buf.write(u"\u01c2\3\2\2\2\u01c5\u01c3\3\2\2\2\u01c5\u01c4\3\2\2")
        buf.write(u"\2\u01c6[\3\2\2\2\u01c7\u01c9\7,\2\2\u01c8\u01ca\5h\65")
        buf.write(u"\2\u01c9\u01c8\3\2\2\2\u01c9\u01ca\3\2\2\2\u01ca\u01cb")
        buf.write(u"\3\2\2\2\u01cb\u01d3\7-\2\2\u01cc\u01cd\7\63\2\2\u01cd")
        buf.write(u"\u01ce\5^\60\2\u01ce\u01cf\7\64\2\2\u01cf\u01d3\3\2\2")
        buf.write(u"\2\u01d0\u01d1\7)\2\2\u01d1\u01d3\7%\2\2\u01d2\u01c7")
        buf.write(u"\3\2\2\2\u01d2\u01cc\3\2\2\2\u01d2\u01d0\3\2\2\2\u01d3")
        buf.write(u"]\3\2\2\2\u01d4\u01dd\5<\37\2\u01d5\u01d7\5<\37\2\u01d6")
        buf.write(u"\u01d5\3\2\2\2\u01d6\u01d7\3\2\2\2\u01d7\u01d8\3\2\2")
        buf.write(u"\2\u01d8\u01da\7/\2\2\u01d9\u01db\5<\37\2\u01da\u01d9")
        buf.write(u"\3\2\2\2\u01da\u01db\3\2\2\2\u01db\u01dd\3\2\2\2\u01dc")
        buf.write(u"\u01d4\3\2\2\2\u01dc\u01d6\3\2\2\2\u01dd_\3\2\2\2\u01de")
        buf.write(u"\u01e7\7\63\2\2\u01df\u01e4\5<\37\2\u01e0\u01e1\7.\2")
        buf.write(u"\2\u01e1\u01e3\5<\37\2\u01e2\u01e0\3\2\2\2\u01e3\u01e6")
        buf.write(u"\3\2\2\2\u01e4\u01e2\3\2\2\2\u01e4\u01e5\3\2\2\2\u01e5")
        buf.write(u"\u01e8\3\2\2\2\u01e6\u01e4\3\2\2\2\u01e7\u01df\3\2\2")
        buf.write(u"\2\u01e7\u01e8\3\2\2\2\u01e8\u01e9\3\2\2\2\u01e9\u01ea")
        buf.write(u"\7\64\2\2\u01eaa\3\2\2\2\u01eb\u01ed\7,\2\2\u01ec\u01ee")
        buf.write(u"\5f\64\2\u01ed\u01ec\3\2\2\2\u01ed\u01ee\3\2\2\2\u01ee")
        buf.write(u"\u01ef\3\2\2\2\u01ef\u01f0\7-\2\2\u01f0c\3\2\2\2\u01f1")
        buf.write(u"\u0202\7>\2\2\u01f2\u01f3\5<\37\2\u01f3\u01f4\7/\2\2")
        buf.write(u"\u01f4\u01fc\5<\37\2\u01f5\u01f6\7.\2\2\u01f6\u01f7\5")
        buf.write(u"<\37\2\u01f7\u01f8\7/\2\2\u01f8\u01f9\5<\37\2\u01f9\u01fb")
        buf.write(u"\3\2\2\2\u01fa\u01f5\3\2\2\2\u01fb\u01fe\3\2\2\2\u01fc")
        buf.write(u"\u01fa\3\2\2\2\u01fc\u01fd\3\2\2\2\u01fd\u0200\3\2\2")
        buf.write(u"\2\u01fe\u01fc\3\2\2\2\u01ff\u0201\7.\2\2\u0200\u01ff")
        buf.write(u"\3\2\2\2\u0200\u0201\3\2\2\2\u0201\u0203\3\2\2\2\u0202")
        buf.write(u"\u01f2\3\2\2\2\u0202\u0203\3\2\2\2\u0203\u0204\3\2\2")
        buf.write(u"\2\u0204\u0205\7?\2\2\u0205e\3\2\2\2\u0206\u020b\5<\37")
        buf.write(u"\2\u0207\u0208\7.\2\2\u0208\u020a\5<\37\2\u0209\u0207")
        buf.write(u"\3\2\2\2\u020a\u020d\3\2\2\2\u020b\u0209\3\2\2\2\u020b")
        buf.write(u"\u020c\3\2\2\2\u020c\u020f\3\2\2\2\u020d\u020b\3\2\2")
        buf.write(u"\2\u020e\u0210\7.\2\2\u020f\u020e\3\2\2\2\u020f\u0210")
        buf.write(u"\3\2\2\2\u0210g\3\2\2\2\u0211\u0216\5j\66\2\u0212\u0213")
        buf.write(u"\7.\2\2\u0213\u0215\5j\66\2\u0214\u0212\3\2\2\2\u0215")
        buf.write(u"\u0218\3\2\2\2\u0216\u0214\3\2\2\2\u0216\u0217\3\2\2")
        buf.write(u"\2\u0217i\3\2\2\2\u0218\u0216\3\2\2\2\u0219\u021a\7%")
        buf.write(u"\2\2\u021a\u021c\7\62\2\2\u021b\u0219\3\2\2\2\u021b\u021c")
        buf.write(u"\3\2\2\2\u021c\u021d\3\2\2\2\u021d\u021e\5<\37\2\u021e")
        buf.write(u"k\3\2\2\2Cnpy\u0082\u0085\u008c\u0099\u00a2\u00a8\u00ae")
        buf.write(u"\u00b5\u00b9\u00c1\u00c6\u00cf\u00d3\u00d7\u00e5\u00ea")
        buf.write(u"\u00ef\u00f6\u00fa\u0101\u0109\u010e\u0115\u011b\u0128")
        buf.write(u"\u012e\u0136\u013a\u0142\u0145\u0151\u0159\u015f\u016c")
        buf.write(u"\u0171\u0179\u0181\u0189\u0191\u0193\u019b\u01a3\u01a9")
        buf.write(u"\u01ae\u01b4\u01c0\u01c5\u01c9\u01d2\u01d6\u01da\u01dc")
        buf.write(u"\u01e4\u01e7\u01ed\u01fc\u0200\u0202\u020b\u020f\u0216")
        buf.write(u"\u021b")
        return buf.getvalue()


class SignalFlowV2Parser ( Parser ):

    grammarFileName = "SignalFlowV2Parser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ u"<INVALID>", u"'def'", u"'return'", u"'raise'", u"'from'", 
                     u"'import'", u"'as'", u"'global'", u"'nonlocal'", u"'assert'", 
                     u"'if'", u"'elif'", u"'else'", u"'while'", u"'for'", 
                     u"'in'", u"'try'", u"'finally'", u"'with'", u"'except'", 
                     u"'lambda'", u"'or'", u"'and'", u"'not'", u"'is'", 
                     u"'None'", u"'True'", u"'False'", u"'class'", u"'yield'", 
                     u"'del'", u"'pass'", u"'continue'", u"'break'", u"<INVALID>", 
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                     u"'.'", u"'...'", u"'*'", u"'('", u"')'", u"','", u"':'", 
                     u"';'", u"'**'", u"'='", u"'['", u"']'", u"'|'", u"'^'", 
                     u"'&'", u"'<<'", u"'>>'", u"'+'", u"'-'", u"'/'", u"'~'", 
                     u"'{'", u"'}'", u"'<'", u"'>'", u"'=='", u"'>='", u"'<='", 
                     u"'<>'", u"'!='", u"'@'", u"'->'" ]

    symbolicNames = [ u"<INVALID>", u"DEF", u"RETURN", u"RAISE", u"FROM", 
                      u"IMPORT", u"AS", u"GLOBAL", u"NONLOCAL", u"ASSERT", 
                      u"IF", u"ELIF", u"ELSE", u"WHILE", u"FOR", u"IN", 
                      u"TRY", u"FINALLY", u"WITH", u"EXCEPT", u"LAMBDA", 
                      u"OR", u"AND", u"NOT", u"IS", u"NONE", u"TRUE", u"FALSE", 
                      u"CLASS", u"YIELD", u"DEL", u"PASS", u"CONTINUE", 
                      u"BREAK", u"NEWLINE", u"ID", u"STRING", u"INT", u"FLOAT", 
                      u"DOT", u"ELLIPSE", u"STAR", u"OPEN_PAREN", u"CLOSE_PAREN", 
                      u"COMMA", u"COLON", u"SEMICOLON", u"POWER", u"ASSIGN", 
                      u"OPEN_BRACK", u"CLOSE_BRACK", u"OR_OP", u"XOR", u"AND_OP", 
                      u"LEFT_SHIFT", u"RIGHT_SHIFT", u"ADD", u"MINUS", u"DIV", 
                      u"NOT_OP", u"OPEN_BRACE", u"CLOSE_BRACE", u"LESS_THAN", 
                      u"GREATER_THAN", u"EQUALS", u"GT_EQ", u"LT_EQ", u"NOT_EQ_1", 
                      u"NOT_EQ_2", u"AT", u"ARROW", u"SKIP_", u"COMMENT", 
                      u"INDENT", u"DEDENT" ]

    RULE_program = 0
    RULE_eval_input = 1
    RULE_decorator = 2
    RULE_decorators = 3
    RULE_decorated = 4
    RULE_function_definition = 5
    RULE_parameters = 6
    RULE_var_args_list = 7
    RULE_var_args_list_param_def = 8
    RULE_var_args_list_param_name = 9
    RULE_statement = 10
    RULE_simple_statement = 11
    RULE_small_statement = 12
    RULE_expr_statement = 13
    RULE_id_list = 14
    RULE_import_statement = 15
    RULE_import_name = 16
    RULE_import_from = 17
    RULE_import_as_name = 18
    RULE_dotted_as_name = 19
    RULE_import_as_names = 20
    RULE_dotted_as_names = 21
    RULE_dotted_name = 22
    RULE_return_statement = 23
    RULE_flow_statement = 24
    RULE_compound_statement = 25
    RULE_assert_statement = 26
    RULE_if_statement = 27
    RULE_suite = 28
    RULE_test = 29
    RULE_lambdef = 30
    RULE_or_test = 31
    RULE_and_test = 32
    RULE_not_test = 33
    RULE_comparison = 34
    RULE_expr = 35
    RULE_xor_expr = 36
    RULE_and_expr = 37
    RULE_shift_expr = 38
    RULE_arith_expr = 39
    RULE_term = 40
    RULE_factor = 41
    RULE_power = 42
    RULE_atom_expr = 43
    RULE_atom = 44
    RULE_trailer = 45
    RULE_subscript = 46
    RULE_list_expr = 47
    RULE_tuple_expr = 48
    RULE_dict_expr = 49
    RULE_testlist = 50
    RULE_actual_args = 51
    RULE_argument = 52

    ruleNames =  [ u"program", u"eval_input", u"decorator", u"decorators", 
                   u"decorated", u"function_definition", u"parameters", 
                   u"var_args_list", u"var_args_list_param_def", u"var_args_list_param_name", 
                   u"statement", u"simple_statement", u"small_statement", 
                   u"expr_statement", u"id_list", u"import_statement", u"import_name", 
                   u"import_from", u"import_as_name", u"dotted_as_name", 
                   u"import_as_names", u"dotted_as_names", u"dotted_name", 
                   u"return_statement", u"flow_statement", u"compound_statement", 
                   u"assert_statement", u"if_statement", u"suite", u"test", 
                   u"lambdef", u"or_test", u"and_test", u"not_test", u"comparison", 
                   u"expr", u"xor_expr", u"and_expr", u"shift_expr", u"arith_expr", 
                   u"term", u"factor", u"power", u"atom_expr", u"atom", 
                   u"trailer", u"subscript", u"list_expr", u"tuple_expr", 
                   u"dict_expr", u"testlist", u"actual_args", u"argument" ]

    EOF = Token.EOF
    DEF=1
    RETURN=2
    RAISE=3
    FROM=4
    IMPORT=5
    AS=6
    GLOBAL=7
    NONLOCAL=8
    ASSERT=9
    IF=10
    ELIF=11
    ELSE=12
    WHILE=13
    FOR=14
    IN=15
    TRY=16
    FINALLY=17
    WITH=18
    EXCEPT=19
    LAMBDA=20
    OR=21
    AND=22
    NOT=23
    IS=24
    NONE=25
    TRUE=26
    FALSE=27
    CLASS=28
    YIELD=29
    DEL=30
    PASS=31
    CONTINUE=32
    BREAK=33
    NEWLINE=34
    ID=35
    STRING=36
    INT=37
    FLOAT=38
    DOT=39
    ELLIPSE=40
    STAR=41
    OPEN_PAREN=42
    CLOSE_PAREN=43
    COMMA=44
    COLON=45
    SEMICOLON=46
    POWER=47
    ASSIGN=48
    OPEN_BRACK=49
    CLOSE_BRACK=50
    OR_OP=51
    XOR=52
    AND_OP=53
    LEFT_SHIFT=54
    RIGHT_SHIFT=55
    ADD=56
    MINUS=57
    DIV=58
    NOT_OP=59
    OPEN_BRACE=60
    CLOSE_BRACE=61
    LESS_THAN=62
    GREATER_THAN=63
    EQUALS=64
    GT_EQ=65
    LT_EQ=66
    NOT_EQ_1=67
    NOT_EQ_2=68
    AT=69
    ARROW=70
    SKIP_=71
    COMMENT=72
    INDENT=73
    DEDENT=74

    def __init__(self, input):
        super(SignalFlowV2Parser, self).__init__(input)
        self.checkVersion("4.5.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class ProgramContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.ProgramContext, self).__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(SignalFlowV2Parser.EOF, 0)

        def NEWLINE(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.NEWLINE)
            else:
                return self.getToken(SignalFlowV2Parser.NEWLINE, i)

        def statement(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.StatementContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.StatementContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_program

        def enterRule(self, listener):
            if hasattr(listener, "enterProgram"):
                listener.enterProgram(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitProgram"):
                listener.exitProgram(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitProgram"):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = SignalFlowV2Parser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 110
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.DEF) | (1 << SignalFlowV2Parser.RETURN) | (1 << SignalFlowV2Parser.FROM) | (1 << SignalFlowV2Parser.IMPORT) | (1 << SignalFlowV2Parser.ASSERT) | (1 << SignalFlowV2Parser.IF) | (1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.NEWLINE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NOT_OP) | (1 << SignalFlowV2Parser.OPEN_BRACE))) != 0) or _la==SignalFlowV2Parser.AT:
                self.state = 108
                token = self._input.LA(1)
                if token in [SignalFlowV2Parser.NEWLINE]:
                    self.state = 106
                    self.match(SignalFlowV2Parser.NEWLINE)

                elif token in [SignalFlowV2Parser.DEF, SignalFlowV2Parser.RETURN, SignalFlowV2Parser.FROM, SignalFlowV2Parser.IMPORT, SignalFlowV2Parser.ASSERT, SignalFlowV2Parser.IF, SignalFlowV2Parser.LAMBDA, SignalFlowV2Parser.NOT, SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.ID, SignalFlowV2Parser.STRING, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.OPEN_BRACK, SignalFlowV2Parser.ADD, SignalFlowV2Parser.MINUS, SignalFlowV2Parser.NOT_OP, SignalFlowV2Parser.OPEN_BRACE, SignalFlowV2Parser.AT]:
                    self.state = 107
                    self.statement()

                else:
                    raise NoViableAltException(self)

                self.state = 112
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 113
            self.match(SignalFlowV2Parser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Eval_inputContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Eval_inputContext, self).__init__(parent, invokingState)
            self.parser = parser

        def testlist(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestlistContext,0)


        def EOF(self):
            return self.getToken(SignalFlowV2Parser.EOF, 0)

        def NEWLINE(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.NEWLINE)
            else:
                return self.getToken(SignalFlowV2Parser.NEWLINE, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_eval_input

        def enterRule(self, listener):
            if hasattr(listener, "enterEval_input"):
                listener.enterEval_input(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitEval_input"):
                listener.exitEval_input(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitEval_input"):
                return visitor.visitEval_input(self)
            else:
                return visitor.visitChildren(self)




    def eval_input(self):

        localctx = SignalFlowV2Parser.Eval_inputContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_eval_input)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 115
            self.testlist()
            self.state = 119
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.NEWLINE:
                self.state = 116
                self.match(SignalFlowV2Parser.NEWLINE)
                self.state = 121
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 122
            self.match(SignalFlowV2Parser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class DecoratorContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.DecoratorContext, self).__init__(parent, invokingState)
            self.parser = parser

        def dotted_name(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Dotted_nameContext,0)


        def NEWLINE(self):
            return self.getToken(SignalFlowV2Parser.NEWLINE, 0)

        def actual_args(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Actual_argsContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_decorator

        def enterRule(self, listener):
            if hasattr(listener, "enterDecorator"):
                listener.enterDecorator(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitDecorator"):
                listener.exitDecorator(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitDecorator"):
                return visitor.visitDecorator(self)
            else:
                return visitor.visitChildren(self)




    def decorator(self):

        localctx = SignalFlowV2Parser.DecoratorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_decorator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 124
            self.match(SignalFlowV2Parser.AT)
            self.state = 125
            self.dotted_name()
            self.state = 131
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.OPEN_PAREN:
                self.state = 126
                self.match(SignalFlowV2Parser.OPEN_PAREN)
                self.state = 128
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NOT_OP) | (1 << SignalFlowV2Parser.OPEN_BRACE))) != 0):
                    self.state = 127
                    self.actual_args()


                self.state = 130
                self.match(SignalFlowV2Parser.CLOSE_PAREN)


            self.state = 133
            self.match(SignalFlowV2Parser.NEWLINE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class DecoratorsContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.DecoratorsContext, self).__init__(parent, invokingState)
            self.parser = parser

        def decorator(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.DecoratorContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.DecoratorContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_decorators

        def enterRule(self, listener):
            if hasattr(listener, "enterDecorators"):
                listener.enterDecorators(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitDecorators"):
                listener.exitDecorators(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitDecorators"):
                return visitor.visitDecorators(self)
            else:
                return visitor.visitChildren(self)




    def decorators(self):

        localctx = SignalFlowV2Parser.DecoratorsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_decorators)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 136 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 135
                self.decorator()
                self.state = 138 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==SignalFlowV2Parser.AT):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class DecoratedContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.DecoratedContext, self).__init__(parent, invokingState)
            self.parser = parser

        def decorators(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.DecoratorsContext,0)


        def function_definition(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Function_definitionContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_decorated

        def enterRule(self, listener):
            if hasattr(listener, "enterDecorated"):
                listener.enterDecorated(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitDecorated"):
                listener.exitDecorated(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitDecorated"):
                return visitor.visitDecorated(self)
            else:
                return visitor.visitChildren(self)




    def decorated(self):

        localctx = SignalFlowV2Parser.DecoratedContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_decorated)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 140
            self.decorators()
            self.state = 141
            self.function_definition()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Function_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Function_definitionContext, self).__init__(parent, invokingState)
            self.parser = parser

        def DEF(self):
            return self.getToken(SignalFlowV2Parser.DEF, 0)

        def ID(self):
            return self.getToken(SignalFlowV2Parser.ID, 0)

        def parameters(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.ParametersContext,0)


        def suite(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.SuiteContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_function_definition

        def enterRule(self, listener):
            if hasattr(listener, "enterFunction_definition"):
                listener.enterFunction_definition(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitFunction_definition"):
                listener.exitFunction_definition(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitFunction_definition"):
                return visitor.visitFunction_definition(self)
            else:
                return visitor.visitChildren(self)




    def function_definition(self):

        localctx = SignalFlowV2Parser.Function_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_function_definition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 143
            self.match(SignalFlowV2Parser.DEF)
            self.state = 144
            self.match(SignalFlowV2Parser.ID)
            self.state = 145
            self.parameters()
            self.state = 146
            self.match(SignalFlowV2Parser.COLON)
            self.state = 147
            self.suite()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ParametersContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.ParametersContext, self).__init__(parent, invokingState)
            self.parser = parser

        def OPEN_PAREN(self):
            return self.getToken(SignalFlowV2Parser.OPEN_PAREN, 0)

        def CLOSE_PAREN(self):
            return self.getToken(SignalFlowV2Parser.CLOSE_PAREN, 0)

        def var_args_list(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Var_args_listContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_parameters

        def enterRule(self, listener):
            if hasattr(listener, "enterParameters"):
                listener.enterParameters(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitParameters"):
                listener.exitParameters(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitParameters"):
                return visitor.visitParameters(self)
            else:
                return visitor.visitChildren(self)




    def parameters(self):

        localctx = SignalFlowV2Parser.ParametersContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_parameters)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 149
            self.match(SignalFlowV2Parser.OPEN_PAREN)
            self.state = 151
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.ID:
                self.state = 150
                self.var_args_list()


            self.state = 153
            self.match(SignalFlowV2Parser.CLOSE_PAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Var_args_listContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Var_args_listContext, self).__init__(parent, invokingState)
            self.parser = parser

        def var_args_list_param_def(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Var_args_list_param_defContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Var_args_list_param_defContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_var_args_list

        def enterRule(self, listener):
            if hasattr(listener, "enterVar_args_list"):
                listener.enterVar_args_list(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitVar_args_list"):
                listener.exitVar_args_list(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitVar_args_list"):
                return visitor.visitVar_args_list(self)
            else:
                return visitor.visitChildren(self)




    def var_args_list(self):

        localctx = SignalFlowV2Parser.Var_args_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_var_args_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 155
            self.var_args_list_param_def()
            self.state = 160
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.COMMA:
                self.state = 156
                self.match(SignalFlowV2Parser.COMMA)
                self.state = 157
                self.var_args_list_param_def()
                self.state = 162
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Var_args_list_param_defContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Var_args_list_param_defContext, self).__init__(parent, invokingState)
            self.parser = parser

        def var_args_list_param_name(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Var_args_list_param_nameContext,0)


        def test(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_var_args_list_param_def

        def enterRule(self, listener):
            if hasattr(listener, "enterVar_args_list_param_def"):
                listener.enterVar_args_list_param_def(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitVar_args_list_param_def"):
                listener.exitVar_args_list_param_def(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitVar_args_list_param_def"):
                return visitor.visitVar_args_list_param_def(self)
            else:
                return visitor.visitChildren(self)




    def var_args_list_param_def(self):

        localctx = SignalFlowV2Parser.Var_args_list_param_defContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_var_args_list_param_def)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 163
            self.var_args_list_param_name()
            self.state = 166
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.ASSIGN:
                self.state = 164
                self.match(SignalFlowV2Parser.ASSIGN)
                self.state = 165
                self.test()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Var_args_list_param_nameContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Var_args_list_param_nameContext, self).__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(SignalFlowV2Parser.ID, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_var_args_list_param_name

        def enterRule(self, listener):
            if hasattr(listener, "enterVar_args_list_param_name"):
                listener.enterVar_args_list_param_name(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitVar_args_list_param_name"):
                listener.exitVar_args_list_param_name(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitVar_args_list_param_name"):
                return visitor.visitVar_args_list_param_name(self)
            else:
                return visitor.visitChildren(self)




    def var_args_list_param_name(self):

        localctx = SignalFlowV2Parser.Var_args_list_param_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_var_args_list_param_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 168
            self.match(SignalFlowV2Parser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class StatementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.StatementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def simple_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Simple_statementContext,0)


        def compound_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Compound_statementContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterStatement"):
                listener.enterStatement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitStatement"):
                listener.exitStatement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitStatement"):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = SignalFlowV2Parser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_statement)
        try:
            self.state = 172
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.RETURN, SignalFlowV2Parser.FROM, SignalFlowV2Parser.IMPORT, SignalFlowV2Parser.ASSERT, SignalFlowV2Parser.LAMBDA, SignalFlowV2Parser.NOT, SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.ID, SignalFlowV2Parser.STRING, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.OPEN_BRACK, SignalFlowV2Parser.ADD, SignalFlowV2Parser.MINUS, SignalFlowV2Parser.NOT_OP, SignalFlowV2Parser.OPEN_BRACE]:
                self.enterOuterAlt(localctx, 1)
                self.state = 170
                self.simple_statement()

            elif token in [SignalFlowV2Parser.DEF, SignalFlowV2Parser.IF, SignalFlowV2Parser.AT]:
                self.enterOuterAlt(localctx, 2)
                self.state = 171
                self.compound_statement()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Simple_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Simple_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def small_statement(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Small_statementContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Small_statementContext,i)


        def NEWLINE(self):
            return self.getToken(SignalFlowV2Parser.NEWLINE, 0)

        def EOF(self):
            return self.getToken(SignalFlowV2Parser.EOF, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_simple_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterSimple_statement"):
                listener.enterSimple_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitSimple_statement"):
                listener.exitSimple_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitSimple_statement"):
                return visitor.visitSimple_statement(self)
            else:
                return visitor.visitChildren(self)




    def simple_statement(self):

        localctx = SignalFlowV2Parser.Simple_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_simple_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 174
            self.small_statement()
            self.state = 179
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,10,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 175
                    self.match(SignalFlowV2Parser.SEMICOLON)
                    self.state = 176
                    self.small_statement() 
                self.state = 181
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,10,self._ctx)

            self.state = 183
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.SEMICOLON:
                self.state = 182
                self.match(SignalFlowV2Parser.SEMICOLON)


            self.state = 185
            _la = self._input.LA(1)
            if not(_la==SignalFlowV2Parser.EOF or _la==SignalFlowV2Parser.NEWLINE):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Small_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Small_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def expr_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Expr_statementContext,0)


        def flow_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Flow_statementContext,0)


        def import_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Import_statementContext,0)


        def assert_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Assert_statementContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_small_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterSmall_statement"):
                listener.enterSmall_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitSmall_statement"):
                listener.exitSmall_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitSmall_statement"):
                return visitor.visitSmall_statement(self)
            else:
                return visitor.visitChildren(self)




    def small_statement(self):

        localctx = SignalFlowV2Parser.Small_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_small_statement)
        try:
            self.state = 191
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.LAMBDA, SignalFlowV2Parser.NOT, SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.ID, SignalFlowV2Parser.STRING, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.OPEN_BRACK, SignalFlowV2Parser.ADD, SignalFlowV2Parser.MINUS, SignalFlowV2Parser.NOT_OP, SignalFlowV2Parser.OPEN_BRACE]:
                self.enterOuterAlt(localctx, 1)
                self.state = 187
                self.expr_statement()

            elif token in [SignalFlowV2Parser.RETURN]:
                self.enterOuterAlt(localctx, 2)
                self.state = 188
                self.flow_statement()

            elif token in [SignalFlowV2Parser.FROM, SignalFlowV2Parser.IMPORT]:
                self.enterOuterAlt(localctx, 3)
                self.state = 189
                self.import_statement()

            elif token in [SignalFlowV2Parser.ASSERT]:
                self.enterOuterAlt(localctx, 4)
                self.state = 190
                self.assert_statement()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Expr_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Expr_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def testlist(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestlistContext,0)


        def id_list(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Id_listContext,0)


        def ASSIGN(self):
            return self.getToken(SignalFlowV2Parser.ASSIGN, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_expr_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterExpr_statement"):
                listener.enterExpr_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitExpr_statement"):
                listener.exitExpr_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitExpr_statement"):
                return visitor.visitExpr_statement(self)
            else:
                return visitor.visitChildren(self)




    def expr_statement(self):

        localctx = SignalFlowV2Parser.Expr_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_expr_statement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 196
            self._errHandler.sync(self);
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                self.state = 193
                self.id_list()
                self.state = 194
                self.match(SignalFlowV2Parser.ASSIGN)


            self.state = 198
            self.testlist()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Id_listContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Id_listContext, self).__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.ID)
            else:
                return self.getToken(SignalFlowV2Parser.ID, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_id_list

        def enterRule(self, listener):
            if hasattr(listener, "enterId_list"):
                listener.enterId_list(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitId_list"):
                listener.exitId_list(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitId_list"):
                return visitor.visitId_list(self)
            else:
                return visitor.visitChildren(self)




    def id_list(self):

        localctx = SignalFlowV2Parser.Id_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_id_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 200
            self.match(SignalFlowV2Parser.ID)
            self.state = 205
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,14,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 201
                    self.match(SignalFlowV2Parser.COMMA)
                    self.state = 202
                    self.match(SignalFlowV2Parser.ID) 
                self.state = 207
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,14,self._ctx)

            self.state = 209
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.COMMA:
                self.state = 208
                self.match(SignalFlowV2Parser.COMMA)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Import_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Import_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def import_name(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Import_nameContext,0)


        def import_from(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Import_fromContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_import_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterImport_statement"):
                listener.enterImport_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitImport_statement"):
                listener.exitImport_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitImport_statement"):
                return visitor.visitImport_statement(self)
            else:
                return visitor.visitChildren(self)




    def import_statement(self):

        localctx = SignalFlowV2Parser.Import_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_import_statement)
        try:
            self.state = 213
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.IMPORT]:
                self.enterOuterAlt(localctx, 1)
                self.state = 211
                self.import_name()

            elif token in [SignalFlowV2Parser.FROM]:
                self.enterOuterAlt(localctx, 2)
                self.state = 212
                self.import_from()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Import_nameContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Import_nameContext, self).__init__(parent, invokingState)
            self.parser = parser

        def IMPORT(self):
            return self.getToken(SignalFlowV2Parser.IMPORT, 0)

        def dotted_as_names(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Dotted_as_namesContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_import_name

        def enterRule(self, listener):
            if hasattr(listener, "enterImport_name"):
                listener.enterImport_name(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitImport_name"):
                listener.exitImport_name(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitImport_name"):
                return visitor.visitImport_name(self)
            else:
                return visitor.visitChildren(self)




    def import_name(self):

        localctx = SignalFlowV2Parser.Import_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_import_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 215
            self.match(SignalFlowV2Parser.IMPORT)
            self.state = 216
            self.dotted_as_names()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Import_fromContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Import_fromContext, self).__init__(parent, invokingState)
            self.parser = parser

        def FROM(self):
            return self.getToken(SignalFlowV2Parser.FROM, 0)

        def dotted_name(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Dotted_nameContext,0)


        def IMPORT(self):
            return self.getToken(SignalFlowV2Parser.IMPORT, 0)

        def import_as_names(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Import_as_namesContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_import_from

        def enterRule(self, listener):
            if hasattr(listener, "enterImport_from"):
                listener.enterImport_from(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitImport_from"):
                listener.exitImport_from(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitImport_from"):
                return visitor.visitImport_from(self)
            else:
                return visitor.visitChildren(self)




    def import_from(self):

        localctx = SignalFlowV2Parser.Import_fromContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_import_from)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 218
            self.match(SignalFlowV2Parser.FROM)
            self.state = 219
            self.dotted_name()
            self.state = 220
            self.match(SignalFlowV2Parser.IMPORT)
            self.state = 227
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.STAR]:
                self.state = 221
                self.match(SignalFlowV2Parser.STAR)

            elif token in [SignalFlowV2Parser.OPEN_PAREN]:
                self.state = 222
                self.match(SignalFlowV2Parser.OPEN_PAREN)
                self.state = 223
                self.import_as_names()
                self.state = 224
                self.match(SignalFlowV2Parser.CLOSE_PAREN)

            elif token in [SignalFlowV2Parser.ID]:
                self.state = 226
                self.import_as_names()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Import_as_nameContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Import_as_nameContext, self).__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.ID)
            else:
                return self.getToken(SignalFlowV2Parser.ID, i)

        def AS(self):
            return self.getToken(SignalFlowV2Parser.AS, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_import_as_name

        def enterRule(self, listener):
            if hasattr(listener, "enterImport_as_name"):
                listener.enterImport_as_name(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitImport_as_name"):
                listener.exitImport_as_name(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitImport_as_name"):
                return visitor.visitImport_as_name(self)
            else:
                return visitor.visitChildren(self)




    def import_as_name(self):

        localctx = SignalFlowV2Parser.Import_as_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_import_as_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 229
            self.match(SignalFlowV2Parser.ID)
            self.state = 232
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.AS:
                self.state = 230
                self.match(SignalFlowV2Parser.AS)
                self.state = 231
                self.match(SignalFlowV2Parser.ID)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Dotted_as_nameContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Dotted_as_nameContext, self).__init__(parent, invokingState)
            self.parser = parser

        def dotted_name(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Dotted_nameContext,0)


        def AS(self):
            return self.getToken(SignalFlowV2Parser.AS, 0)

        def ID(self):
            return self.getToken(SignalFlowV2Parser.ID, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_dotted_as_name

        def enterRule(self, listener):
            if hasattr(listener, "enterDotted_as_name"):
                listener.enterDotted_as_name(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitDotted_as_name"):
                listener.exitDotted_as_name(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitDotted_as_name"):
                return visitor.visitDotted_as_name(self)
            else:
                return visitor.visitChildren(self)




    def dotted_as_name(self):

        localctx = SignalFlowV2Parser.Dotted_as_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_dotted_as_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 234
            self.dotted_name()
            self.state = 237
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.AS:
                self.state = 235
                self.match(SignalFlowV2Parser.AS)
                self.state = 236
                self.match(SignalFlowV2Parser.ID)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Import_as_namesContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Import_as_namesContext, self).__init__(parent, invokingState)
            self.parser = parser

        def import_as_name(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Import_as_nameContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Import_as_nameContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_import_as_names

        def enterRule(self, listener):
            if hasattr(listener, "enterImport_as_names"):
                listener.enterImport_as_names(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitImport_as_names"):
                listener.exitImport_as_names(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitImport_as_names"):
                return visitor.visitImport_as_names(self)
            else:
                return visitor.visitChildren(self)




    def import_as_names(self):

        localctx = SignalFlowV2Parser.Import_as_namesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_import_as_names)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 239
            self.import_as_name()
            self.state = 244
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,20,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 240
                    self.match(SignalFlowV2Parser.COMMA)
                    self.state = 241
                    self.import_as_name() 
                self.state = 246
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,20,self._ctx)

            self.state = 248
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.COMMA:
                self.state = 247
                self.match(SignalFlowV2Parser.COMMA)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Dotted_as_namesContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Dotted_as_namesContext, self).__init__(parent, invokingState)
            self.parser = parser

        def dotted_as_name(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Dotted_as_nameContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Dotted_as_nameContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_dotted_as_names

        def enterRule(self, listener):
            if hasattr(listener, "enterDotted_as_names"):
                listener.enterDotted_as_names(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitDotted_as_names"):
                listener.exitDotted_as_names(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitDotted_as_names"):
                return visitor.visitDotted_as_names(self)
            else:
                return visitor.visitChildren(self)




    def dotted_as_names(self):

        localctx = SignalFlowV2Parser.Dotted_as_namesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_dotted_as_names)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 250
            self.dotted_as_name()
            self.state = 255
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.COMMA:
                self.state = 251
                self.match(SignalFlowV2Parser.COMMA)
                self.state = 252
                self.dotted_as_name()
                self.state = 257
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Dotted_nameContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Dotted_nameContext, self).__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.ID)
            else:
                return self.getToken(SignalFlowV2Parser.ID, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_dotted_name

        def enterRule(self, listener):
            if hasattr(listener, "enterDotted_name"):
                listener.enterDotted_name(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitDotted_name"):
                listener.exitDotted_name(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitDotted_name"):
                return visitor.visitDotted_name(self)
            else:
                return visitor.visitChildren(self)




    def dotted_name(self):

        localctx = SignalFlowV2Parser.Dotted_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_dotted_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 258
            self.match(SignalFlowV2Parser.ID)
            self.state = 263
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.DOT:
                self.state = 259
                self.match(SignalFlowV2Parser.DOT)
                self.state = 260
                self.match(SignalFlowV2Parser.ID)
                self.state = 265
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Return_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Return_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def RETURN(self):
            return self.getToken(SignalFlowV2Parser.RETURN, 0)

        def testlist(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestlistContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_return_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterReturn_statement"):
                listener.enterReturn_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitReturn_statement"):
                listener.exitReturn_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitReturn_statement"):
                return visitor.visitReturn_statement(self)
            else:
                return visitor.visitChildren(self)




    def return_statement(self):

        localctx = SignalFlowV2Parser.Return_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_return_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 266
            self.match(SignalFlowV2Parser.RETURN)
            self.state = 268
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NOT_OP) | (1 << SignalFlowV2Parser.OPEN_BRACE))) != 0):
                self.state = 267
                self.testlist()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Flow_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Flow_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def return_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Return_statementContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_flow_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterFlow_statement"):
                listener.enterFlow_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitFlow_statement"):
                listener.exitFlow_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitFlow_statement"):
                return visitor.visitFlow_statement(self)
            else:
                return visitor.visitChildren(self)




    def flow_statement(self):

        localctx = SignalFlowV2Parser.Flow_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_flow_statement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 270
            self.return_statement()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Compound_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Compound_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def if_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.If_statementContext,0)


        def function_definition(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Function_definitionContext,0)


        def decorated(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.DecoratedContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_compound_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterCompound_statement"):
                listener.enterCompound_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitCompound_statement"):
                listener.exitCompound_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitCompound_statement"):
                return visitor.visitCompound_statement(self)
            else:
                return visitor.visitChildren(self)




    def compound_statement(self):

        localctx = SignalFlowV2Parser.Compound_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_compound_statement)
        try:
            self.state = 275
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.IF]:
                self.enterOuterAlt(localctx, 1)
                self.state = 272
                self.if_statement()

            elif token in [SignalFlowV2Parser.DEF]:
                self.enterOuterAlt(localctx, 2)
                self.state = 273
                self.function_definition()

            elif token in [SignalFlowV2Parser.AT]:
                self.enterOuterAlt(localctx, 3)
                self.state = 274
                self.decorated()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Assert_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Assert_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def ASSERT(self):
            return self.getToken(SignalFlowV2Parser.ASSERT, 0)

        def test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.TestContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_assert_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterAssert_statement"):
                listener.enterAssert_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitAssert_statement"):
                listener.exitAssert_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitAssert_statement"):
                return visitor.visitAssert_statement(self)
            else:
                return visitor.visitChildren(self)




    def assert_statement(self):

        localctx = SignalFlowV2Parser.Assert_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_assert_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 277
            self.match(SignalFlowV2Parser.ASSERT)
            self.state = 278
            self.test()
            self.state = 281
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.COMMA:
                self.state = 279
                self.match(SignalFlowV2Parser.COMMA)
                self.state = 280
                self.test()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class If_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.If_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(SignalFlowV2Parser.IF, 0)

        def test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.TestContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,i)


        def suite(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.SuiteContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.SuiteContext,i)


        def ELIF(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.ELIF)
            else:
                return self.getToken(SignalFlowV2Parser.ELIF, i)

        def ELSE(self):
            return self.getToken(SignalFlowV2Parser.ELSE, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_if_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterIf_statement"):
                listener.enterIf_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitIf_statement"):
                listener.exitIf_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitIf_statement"):
                return visitor.visitIf_statement(self)
            else:
                return visitor.visitChildren(self)




    def if_statement(self):

        localctx = SignalFlowV2Parser.If_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_if_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 283
            self.match(SignalFlowV2Parser.IF)
            self.state = 284
            self.test()
            self.state = 285
            self.match(SignalFlowV2Parser.COLON)
            self.state = 286
            self.suite()
            self.state = 294
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.ELIF:
                self.state = 287
                self.match(SignalFlowV2Parser.ELIF)
                self.state = 288
                self.test()
                self.state = 289
                self.match(SignalFlowV2Parser.COLON)
                self.state = 290
                self.suite()
                self.state = 296
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 300
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.ELSE:
                self.state = 297
                self.match(SignalFlowV2Parser.ELSE)
                self.state = 298
                self.match(SignalFlowV2Parser.COLON)
                self.state = 299
                self.suite()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class SuiteContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.SuiteContext, self).__init__(parent, invokingState)
            self.parser = parser

        def simple_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Simple_statementContext,0)


        def NEWLINE(self):
            return self.getToken(SignalFlowV2Parser.NEWLINE, 0)

        def INDENT(self):
            return self.getToken(SignalFlowV2Parser.INDENT, 0)

        def DEDENT(self):
            return self.getToken(SignalFlowV2Parser.DEDENT, 0)

        def statement(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.StatementContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.StatementContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_suite

        def enterRule(self, listener):
            if hasattr(listener, "enterSuite"):
                listener.enterSuite(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitSuite"):
                listener.exitSuite(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitSuite"):
                return visitor.visitSuite(self)
            else:
                return visitor.visitChildren(self)




    def suite(self):

        localctx = SignalFlowV2Parser.SuiteContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_suite)
        self._la = 0 # Token type
        try:
            self.state = 312
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.RETURN, SignalFlowV2Parser.FROM, SignalFlowV2Parser.IMPORT, SignalFlowV2Parser.ASSERT, SignalFlowV2Parser.LAMBDA, SignalFlowV2Parser.NOT, SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.ID, SignalFlowV2Parser.STRING, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.OPEN_BRACK, SignalFlowV2Parser.ADD, SignalFlowV2Parser.MINUS, SignalFlowV2Parser.NOT_OP, SignalFlowV2Parser.OPEN_BRACE]:
                self.enterOuterAlt(localctx, 1)
                self.state = 302
                self.simple_statement()

            elif token in [SignalFlowV2Parser.NEWLINE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 303
                self.match(SignalFlowV2Parser.NEWLINE)
                self.state = 304
                self.match(SignalFlowV2Parser.INDENT)
                self.state = 306 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 305
                    self.statement()
                    self.state = 308 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.DEF) | (1 << SignalFlowV2Parser.RETURN) | (1 << SignalFlowV2Parser.FROM) | (1 << SignalFlowV2Parser.IMPORT) | (1 << SignalFlowV2Parser.ASSERT) | (1 << SignalFlowV2Parser.IF) | (1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NOT_OP) | (1 << SignalFlowV2Parser.OPEN_BRACE))) != 0) or _la==SignalFlowV2Parser.AT):
                        break

                self.state = 310
                self.match(SignalFlowV2Parser.DEDENT)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TestContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.TestContext, self).__init__(parent, invokingState)
            self.parser = parser

        def or_test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Or_testContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Or_testContext,i)


        def IF(self):
            return self.getToken(SignalFlowV2Parser.IF, 0)

        def ELSE(self):
            return self.getToken(SignalFlowV2Parser.ELSE, 0)

        def test(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,0)


        def lambdef(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.LambdefContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_test

        def enterRule(self, listener):
            if hasattr(listener, "enterTest"):
                listener.enterTest(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitTest"):
                listener.exitTest(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitTest"):
                return visitor.visitTest(self)
            else:
                return visitor.visitChildren(self)




    def test(self):

        localctx = SignalFlowV2Parser.TestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_test)
        self._la = 0 # Token type
        try:
            self.state = 323
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.NOT, SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.ID, SignalFlowV2Parser.STRING, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.OPEN_BRACK, SignalFlowV2Parser.ADD, SignalFlowV2Parser.MINUS, SignalFlowV2Parser.NOT_OP, SignalFlowV2Parser.OPEN_BRACE]:
                self.enterOuterAlt(localctx, 1)
                self.state = 314
                self.or_test()
                self.state = 320
                _la = self._input.LA(1)
                if _la==SignalFlowV2Parser.IF:
                    self.state = 315
                    self.match(SignalFlowV2Parser.IF)
                    self.state = 316
                    self.or_test()
                    self.state = 317
                    self.match(SignalFlowV2Parser.ELSE)
                    self.state = 318
                    self.test()



            elif token in [SignalFlowV2Parser.LAMBDA]:
                self.enterOuterAlt(localctx, 2)
                self.state = 322
                self.lambdef()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LambdefContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.LambdefContext, self).__init__(parent, invokingState)
            self.parser = parser

        def LAMBDA(self):
            return self.getToken(SignalFlowV2Parser.LAMBDA, 0)

        def ID(self):
            return self.getToken(SignalFlowV2Parser.ID, 0)

        def COLON(self):
            return self.getToken(SignalFlowV2Parser.COLON, 0)

        def test(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_lambdef

        def enterRule(self, listener):
            if hasattr(listener, "enterLambdef"):
                listener.enterLambdef(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitLambdef"):
                listener.exitLambdef(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitLambdef"):
                return visitor.visitLambdef(self)
            else:
                return visitor.visitChildren(self)




    def lambdef(self):

        localctx = SignalFlowV2Parser.LambdefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_lambdef)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 325
            self.match(SignalFlowV2Parser.LAMBDA)
            self.state = 326
            self.match(SignalFlowV2Parser.ID)
            self.state = 327
            self.match(SignalFlowV2Parser.COLON)
            self.state = 328
            self.test()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Or_testContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Or_testContext, self).__init__(parent, invokingState)
            self.parser = parser

        def and_test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.And_testContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.And_testContext,i)


        def OR(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.OR)
            else:
                return self.getToken(SignalFlowV2Parser.OR, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_or_test

        def enterRule(self, listener):
            if hasattr(listener, "enterOr_test"):
                listener.enterOr_test(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitOr_test"):
                listener.exitOr_test(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitOr_test"):
                return visitor.visitOr_test(self)
            else:
                return visitor.visitChildren(self)




    def or_test(self):

        localctx = SignalFlowV2Parser.Or_testContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_or_test)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 330
            self.and_test()
            self.state = 335
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.OR:
                self.state = 331
                self.match(SignalFlowV2Parser.OR)
                self.state = 332
                self.and_test()
                self.state = 337
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class And_testContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.And_testContext, self).__init__(parent, invokingState)
            self.parser = parser

        def not_test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Not_testContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Not_testContext,i)


        def AND(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.AND)
            else:
                return self.getToken(SignalFlowV2Parser.AND, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_and_test

        def enterRule(self, listener):
            if hasattr(listener, "enterAnd_test"):
                listener.enterAnd_test(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitAnd_test"):
                listener.exitAnd_test(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitAnd_test"):
                return visitor.visitAnd_test(self)
            else:
                return visitor.visitChildren(self)




    def and_test(self):

        localctx = SignalFlowV2Parser.And_testContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_and_test)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 338
            self.not_test()
            self.state = 343
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.AND:
                self.state = 339
                self.match(SignalFlowV2Parser.AND)
                self.state = 340
                self.not_test()
                self.state = 345
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Not_testContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Not_testContext, self).__init__(parent, invokingState)
            self.parser = parser

        def NOT(self):
            return self.getToken(SignalFlowV2Parser.NOT, 0)

        def not_test(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Not_testContext,0)


        def comparison(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.ComparisonContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_not_test

        def enterRule(self, listener):
            if hasattr(listener, "enterNot_test"):
                listener.enterNot_test(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitNot_test"):
                listener.exitNot_test(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitNot_test"):
                return visitor.visitNot_test(self)
            else:
                return visitor.visitChildren(self)




    def not_test(self):

        localctx = SignalFlowV2Parser.Not_testContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_not_test)
        try:
            self.state = 349
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.NOT]:
                self.enterOuterAlt(localctx, 1)
                self.state = 346
                self.match(SignalFlowV2Parser.NOT)
                self.state = 347
                self.not_test()

            elif token in [SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.ID, SignalFlowV2Parser.STRING, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.OPEN_BRACK, SignalFlowV2Parser.ADD, SignalFlowV2Parser.MINUS, SignalFlowV2Parser.NOT_OP, SignalFlowV2Parser.OPEN_BRACE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 348
                self.comparison()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ComparisonContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.ComparisonContext, self).__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.ExprContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.ExprContext,i)


        def LESS_THAN(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.LESS_THAN)
            else:
                return self.getToken(SignalFlowV2Parser.LESS_THAN, i)

        def LT_EQ(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.LT_EQ)
            else:
                return self.getToken(SignalFlowV2Parser.LT_EQ, i)

        def EQUALS(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.EQUALS)
            else:
                return self.getToken(SignalFlowV2Parser.EQUALS, i)

        def NOT_EQ_1(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.NOT_EQ_1)
            else:
                return self.getToken(SignalFlowV2Parser.NOT_EQ_1, i)

        def NOT_EQ_2(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.NOT_EQ_2)
            else:
                return self.getToken(SignalFlowV2Parser.NOT_EQ_2, i)

        def GREATER_THAN(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.GREATER_THAN)
            else:
                return self.getToken(SignalFlowV2Parser.GREATER_THAN, i)

        def GT_EQ(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.GT_EQ)
            else:
                return self.getToken(SignalFlowV2Parser.GT_EQ, i)

        def IS(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.IS)
            else:
                return self.getToken(SignalFlowV2Parser.IS, i)

        def NOT(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.NOT)
            else:
                return self.getToken(SignalFlowV2Parser.NOT, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_comparison

        def enterRule(self, listener):
            if hasattr(listener, "enterComparison"):
                listener.enterComparison(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitComparison"):
                listener.exitComparison(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitComparison"):
                return visitor.visitComparison(self)
            else:
                return visitor.visitChildren(self)




    def comparison(self):

        localctx = SignalFlowV2Parser.ComparisonContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_comparison)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 351
            self.expr()
            self.state = 367
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 24)) & ~0x3f) == 0 and ((1 << (_la - 24)) & ((1 << (SignalFlowV2Parser.IS - 24)) | (1 << (SignalFlowV2Parser.LESS_THAN - 24)) | (1 << (SignalFlowV2Parser.GREATER_THAN - 24)) | (1 << (SignalFlowV2Parser.EQUALS - 24)) | (1 << (SignalFlowV2Parser.GT_EQ - 24)) | (1 << (SignalFlowV2Parser.LT_EQ - 24)) | (1 << (SignalFlowV2Parser.NOT_EQ_1 - 24)) | (1 << (SignalFlowV2Parser.NOT_EQ_2 - 24)))) != 0):
                self.state = 362
                self._errHandler.sync(self);
                la_ = self._interp.adaptivePredict(self._input,36,self._ctx)
                if la_ == 1:
                    self.state = 352
                    self.match(SignalFlowV2Parser.LESS_THAN)
                    pass

                elif la_ == 2:
                    self.state = 353
                    self.match(SignalFlowV2Parser.LT_EQ)
                    pass

                elif la_ == 3:
                    self.state = 354
                    self.match(SignalFlowV2Parser.EQUALS)
                    pass

                elif la_ == 4:
                    self.state = 355
                    self.match(SignalFlowV2Parser.NOT_EQ_1)
                    pass

                elif la_ == 5:
                    self.state = 356
                    self.match(SignalFlowV2Parser.NOT_EQ_2)
                    pass

                elif la_ == 6:
                    self.state = 357
                    self.match(SignalFlowV2Parser.GREATER_THAN)
                    pass

                elif la_ == 7:
                    self.state = 358
                    self.match(SignalFlowV2Parser.GT_EQ)
                    pass

                elif la_ == 8:
                    self.state = 359
                    self.match(SignalFlowV2Parser.IS)
                    pass

                elif la_ == 9:
                    self.state = 360
                    self.match(SignalFlowV2Parser.IS)
                    self.state = 361
                    self.match(SignalFlowV2Parser.NOT)
                    pass


                self.state = 364
                self.expr()
                self.state = 369
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ExprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.ExprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def xor_expr(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Xor_exprContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Xor_exprContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterExpr"):
                listener.enterExpr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitExpr"):
                listener.exitExpr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitExpr"):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = SignalFlowV2Parser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 370
            self.xor_expr()
            self.state = 375
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.OR_OP:
                self.state = 371
                self.match(SignalFlowV2Parser.OR_OP)
                self.state = 372
                self.xor_expr()
                self.state = 377
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Xor_exprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Xor_exprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def and_expr(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.And_exprContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.And_exprContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_xor_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterXor_expr"):
                listener.enterXor_expr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitXor_expr"):
                listener.exitXor_expr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitXor_expr"):
                return visitor.visitXor_expr(self)
            else:
                return visitor.visitChildren(self)




    def xor_expr(self):

        localctx = SignalFlowV2Parser.Xor_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_xor_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 378
            self.and_expr()
            self.state = 383
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.XOR:
                self.state = 379
                self.match(SignalFlowV2Parser.XOR)
                self.state = 380
                self.and_expr()
                self.state = 385
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class And_exprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.And_exprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def shift_expr(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Shift_exprContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Shift_exprContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_and_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterAnd_expr"):
                listener.enterAnd_expr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitAnd_expr"):
                listener.exitAnd_expr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitAnd_expr"):
                return visitor.visitAnd_expr(self)
            else:
                return visitor.visitChildren(self)




    def and_expr(self):

        localctx = SignalFlowV2Parser.And_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_and_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 386
            self.shift_expr()
            self.state = 391
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.AND_OP:
                self.state = 387
                self.match(SignalFlowV2Parser.AND_OP)
                self.state = 388
                self.shift_expr()
                self.state = 393
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Shift_exprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Shift_exprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def arith_expr(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Arith_exprContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Arith_exprContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_shift_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterShift_expr"):
                listener.enterShift_expr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitShift_expr"):
                listener.exitShift_expr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitShift_expr"):
                return visitor.visitShift_expr(self)
            else:
                return visitor.visitChildren(self)




    def shift_expr(self):

        localctx = SignalFlowV2Parser.Shift_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_shift_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 394
            self.arith_expr()
            self.state = 401
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.LEFT_SHIFT or _la==SignalFlowV2Parser.RIGHT_SHIFT:
                self.state = 399
                token = self._input.LA(1)
                if token in [SignalFlowV2Parser.LEFT_SHIFT]:
                    self.state = 395
                    self.match(SignalFlowV2Parser.LEFT_SHIFT)
                    self.state = 396
                    self.arith_expr()

                elif token in [SignalFlowV2Parser.RIGHT_SHIFT]:
                    self.state = 397
                    self.match(SignalFlowV2Parser.RIGHT_SHIFT)
                    self.state = 398
                    self.arith_expr()

                else:
                    raise NoViableAltException(self)

                self.state = 403
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Arith_exprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Arith_exprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def term(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.TermContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.TermContext,i)


        def ADD(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.ADD)
            else:
                return self.getToken(SignalFlowV2Parser.ADD, i)

        def MINUS(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.MINUS)
            else:
                return self.getToken(SignalFlowV2Parser.MINUS, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_arith_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterArith_expr"):
                listener.enterArith_expr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitArith_expr"):
                listener.exitArith_expr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitArith_expr"):
                return visitor.visitArith_expr(self)
            else:
                return visitor.visitChildren(self)




    def arith_expr(self):

        localctx = SignalFlowV2Parser.Arith_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 78, self.RULE_arith_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 404
            self.term()
            self.state = 409
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.ADD or _la==SignalFlowV2Parser.MINUS:
                self.state = 405
                _la = self._input.LA(1)
                if not(_la==SignalFlowV2Parser.ADD or _la==SignalFlowV2Parser.MINUS):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                self.state = 406
                self.term()
                self.state = 411
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TermContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.TermContext, self).__init__(parent, invokingState)
            self.parser = parser

        def factor(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.FactorContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.FactorContext,i)


        def STAR(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.STAR)
            else:
                return self.getToken(SignalFlowV2Parser.STAR, i)

        def DIV(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.DIV)
            else:
                return self.getToken(SignalFlowV2Parser.DIV, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_term

        def enterRule(self, listener):
            if hasattr(listener, "enterTerm"):
                listener.enterTerm(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitTerm"):
                listener.exitTerm(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitTerm"):
                return visitor.visitTerm(self)
            else:
                return visitor.visitChildren(self)




    def term(self):

        localctx = SignalFlowV2Parser.TermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 80, self.RULE_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 412
            self.factor()
            self.state = 417
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.STAR or _la==SignalFlowV2Parser.DIV:
                self.state = 413
                _la = self._input.LA(1)
                if not(_la==SignalFlowV2Parser.STAR or _la==SignalFlowV2Parser.DIV):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                self.state = 414
                self.factor()
                self.state = 419
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FactorContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.FactorContext, self).__init__(parent, invokingState)
            self.parser = parser

        def factor(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.FactorContext,0)


        def ADD(self):
            return self.getToken(SignalFlowV2Parser.ADD, 0)

        def MINUS(self):
            return self.getToken(SignalFlowV2Parser.MINUS, 0)

        def NOT_OP(self):
            return self.getToken(SignalFlowV2Parser.NOT_OP, 0)

        def power(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.PowerContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_factor

        def enterRule(self, listener):
            if hasattr(listener, "enterFactor"):
                listener.enterFactor(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitFactor"):
                listener.exitFactor(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitFactor"):
                return visitor.visitFactor(self)
            else:
                return visitor.visitChildren(self)




    def factor(self):

        localctx = SignalFlowV2Parser.FactorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 82, self.RULE_factor)
        self._la = 0 # Token type
        try:
            self.state = 423
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.ADD, SignalFlowV2Parser.MINUS, SignalFlowV2Parser.NOT_OP]:
                self.enterOuterAlt(localctx, 1)
                self.state = 420
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NOT_OP))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                self.state = 421
                self.factor()

            elif token in [SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.ID, SignalFlowV2Parser.STRING, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.OPEN_BRACK, SignalFlowV2Parser.OPEN_BRACE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 422
                self.power()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class PowerContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.PowerContext, self).__init__(parent, invokingState)
            self.parser = parser

        def atom_expr(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Atom_exprContext,0)


        def POWER(self):
            return self.getToken(SignalFlowV2Parser.POWER, 0)

        def factor(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.FactorContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_power

        def enterRule(self, listener):
            if hasattr(listener, "enterPower"):
                listener.enterPower(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitPower"):
                listener.exitPower(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitPower"):
                return visitor.visitPower(self)
            else:
                return visitor.visitChildren(self)




    def power(self):

        localctx = SignalFlowV2Parser.PowerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 84, self.RULE_power)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 425
            self.atom_expr()
            self.state = 428
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.POWER:
                self.state = 426
                self.match(SignalFlowV2Parser.POWER)
                self.state = 427
                self.factor()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Atom_exprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Atom_exprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def atom(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.AtomContext,0)


        def trailer(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.TrailerContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.TrailerContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_atom_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterAtom_expr"):
                listener.enterAtom_expr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitAtom_expr"):
                listener.exitAtom_expr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitAtom_expr"):
                return visitor.visitAtom_expr(self)
            else:
                return visitor.visitChildren(self)




    def atom_expr(self):

        localctx = SignalFlowV2Parser.Atom_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 86, self.RULE_atom_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 430
            self.atom()
            self.state = 434
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.DOT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK))) != 0):
                self.state = 431
                self.trailer()
                self.state = 436
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class AtomContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.AtomContext, self).__init__(parent, invokingState)
            self.parser = parser

        def list_expr(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.List_exprContext,0)


        def tuple_expr(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Tuple_exprContext,0)


        def dict_expr(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Dict_exprContext,0)


        def ID(self):
            return self.getToken(SignalFlowV2Parser.ID, 0)

        def INT(self):
            return self.getToken(SignalFlowV2Parser.INT, 0)

        def FLOAT(self):
            return self.getToken(SignalFlowV2Parser.FLOAT, 0)

        def STRING(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.STRING)
            else:
                return self.getToken(SignalFlowV2Parser.STRING, i)

        def NONE(self):
            return self.getToken(SignalFlowV2Parser.NONE, 0)

        def TRUE(self):
            return self.getToken(SignalFlowV2Parser.TRUE, 0)

        def FALSE(self):
            return self.getToken(SignalFlowV2Parser.FALSE, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_atom

        def enterRule(self, listener):
            if hasattr(listener, "enterAtom"):
                listener.enterAtom(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitAtom"):
                listener.exitAtom(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitAtom"):
                return visitor.visitAtom(self)
            else:
                return visitor.visitChildren(self)




    def atom(self):

        localctx = SignalFlowV2Parser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 88, self.RULE_atom)
        self._la = 0 # Token type
        try:
            self.state = 451
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.OPEN_BRACK]:
                self.enterOuterAlt(localctx, 1)
                self.state = 437
                self.list_expr()

            elif token in [SignalFlowV2Parser.OPEN_PAREN]:
                self.enterOuterAlt(localctx, 2)
                self.state = 438
                self.tuple_expr()

            elif token in [SignalFlowV2Parser.OPEN_BRACE]:
                self.enterOuterAlt(localctx, 3)
                self.state = 439
                self.dict_expr()

            elif token in [SignalFlowV2Parser.ID]:
                self.enterOuterAlt(localctx, 4)
                self.state = 440
                self.match(SignalFlowV2Parser.ID)

            elif token in [SignalFlowV2Parser.INT]:
                self.enterOuterAlt(localctx, 5)
                self.state = 441
                self.match(SignalFlowV2Parser.INT)

            elif token in [SignalFlowV2Parser.FLOAT]:
                self.enterOuterAlt(localctx, 6)
                self.state = 442
                self.match(SignalFlowV2Parser.FLOAT)

            elif token in [SignalFlowV2Parser.STRING]:
                self.enterOuterAlt(localctx, 7)
                self.state = 444 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 443
                    self.match(SignalFlowV2Parser.STRING)
                    self.state = 446 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==SignalFlowV2Parser.STRING):
                        break


            elif token in [SignalFlowV2Parser.NONE]:
                self.enterOuterAlt(localctx, 8)
                self.state = 448
                self.match(SignalFlowV2Parser.NONE)

            elif token in [SignalFlowV2Parser.TRUE]:
                self.enterOuterAlt(localctx, 9)
                self.state = 449
                self.match(SignalFlowV2Parser.TRUE)

            elif token in [SignalFlowV2Parser.FALSE]:
                self.enterOuterAlt(localctx, 10)
                self.state = 450
                self.match(SignalFlowV2Parser.FALSE)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TrailerContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.TrailerContext, self).__init__(parent, invokingState)
            self.parser = parser

        def OPEN_PAREN(self):
            return self.getToken(SignalFlowV2Parser.OPEN_PAREN, 0)

        def CLOSE_PAREN(self):
            return self.getToken(SignalFlowV2Parser.CLOSE_PAREN, 0)

        def actual_args(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Actual_argsContext,0)


        def OPEN_BRACK(self):
            return self.getToken(SignalFlowV2Parser.OPEN_BRACK, 0)

        def subscript(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.SubscriptContext,0)


        def CLOSE_BRACK(self):
            return self.getToken(SignalFlowV2Parser.CLOSE_BRACK, 0)

        def DOT(self):
            return self.getToken(SignalFlowV2Parser.DOT, 0)

        def ID(self):
            return self.getToken(SignalFlowV2Parser.ID, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_trailer

        def enterRule(self, listener):
            if hasattr(listener, "enterTrailer"):
                listener.enterTrailer(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitTrailer"):
                listener.exitTrailer(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitTrailer"):
                return visitor.visitTrailer(self)
            else:
                return visitor.visitChildren(self)




    def trailer(self):

        localctx = SignalFlowV2Parser.TrailerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 90, self.RULE_trailer)
        self._la = 0 # Token type
        try:
            self.state = 464
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.OPEN_PAREN]:
                self.enterOuterAlt(localctx, 1)
                self.state = 453
                self.match(SignalFlowV2Parser.OPEN_PAREN)
                self.state = 455
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NOT_OP) | (1 << SignalFlowV2Parser.OPEN_BRACE))) != 0):
                    self.state = 454
                    self.actual_args()


                self.state = 457
                self.match(SignalFlowV2Parser.CLOSE_PAREN)

            elif token in [SignalFlowV2Parser.OPEN_BRACK]:
                self.enterOuterAlt(localctx, 2)
                self.state = 458
                self.match(SignalFlowV2Parser.OPEN_BRACK)
                self.state = 459
                self.subscript()
                self.state = 460
                self.match(SignalFlowV2Parser.CLOSE_BRACK)

            elif token in [SignalFlowV2Parser.DOT]:
                self.enterOuterAlt(localctx, 3)
                self.state = 462
                self.match(SignalFlowV2Parser.DOT)
                self.state = 463
                self.match(SignalFlowV2Parser.ID)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class SubscriptContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.SubscriptContext, self).__init__(parent, invokingState)
            self.parser = parser

        def test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.TestContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,i)


        def COLON(self):
            return self.getToken(SignalFlowV2Parser.COLON, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_subscript

        def enterRule(self, listener):
            if hasattr(listener, "enterSubscript"):
                listener.enterSubscript(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitSubscript"):
                listener.exitSubscript(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitSubscript"):
                return visitor.visitSubscript(self)
            else:
                return visitor.visitChildren(self)




    def subscript(self):

        localctx = SignalFlowV2Parser.SubscriptContext(self, self._ctx, self.state)
        self.enterRule(localctx, 92, self.RULE_subscript)
        self._la = 0 # Token type
        try:
            self.state = 474
            self._errHandler.sync(self);
            la_ = self._interp.adaptivePredict(self._input,54,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 466
                self.test()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 468
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NOT_OP) | (1 << SignalFlowV2Parser.OPEN_BRACE))) != 0):
                    self.state = 467
                    self.test()


                self.state = 470
                self.match(SignalFlowV2Parser.COLON)
                self.state = 472
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NOT_OP) | (1 << SignalFlowV2Parser.OPEN_BRACE))) != 0):
                    self.state = 471
                    self.test()


                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class List_exprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.List_exprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def OPEN_BRACK(self):
            return self.getToken(SignalFlowV2Parser.OPEN_BRACK, 0)

        def CLOSE_BRACK(self):
            return self.getToken(SignalFlowV2Parser.CLOSE_BRACK, 0)

        def test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.TestContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,i)


        def COMMA(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.COMMA)
            else:
                return self.getToken(SignalFlowV2Parser.COMMA, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_list_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterList_expr"):
                listener.enterList_expr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitList_expr"):
                listener.exitList_expr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitList_expr"):
                return visitor.visitList_expr(self)
            else:
                return visitor.visitChildren(self)




    def list_expr(self):

        localctx = SignalFlowV2Parser.List_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 94, self.RULE_list_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 476
            self.match(SignalFlowV2Parser.OPEN_BRACK)
            self.state = 485
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NOT_OP) | (1 << SignalFlowV2Parser.OPEN_BRACE))) != 0):
                self.state = 477
                self.test()
                self.state = 482
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==SignalFlowV2Parser.COMMA:
                    self.state = 478
                    self.match(SignalFlowV2Parser.COMMA)
                    self.state = 479
                    self.test()
                    self.state = 484
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 487
            self.match(SignalFlowV2Parser.CLOSE_BRACK)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Tuple_exprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Tuple_exprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def OPEN_PAREN(self):
            return self.getToken(SignalFlowV2Parser.OPEN_PAREN, 0)

        def CLOSE_PAREN(self):
            return self.getToken(SignalFlowV2Parser.CLOSE_PAREN, 0)

        def testlist(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestlistContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_tuple_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterTuple_expr"):
                listener.enterTuple_expr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitTuple_expr"):
                listener.exitTuple_expr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitTuple_expr"):
                return visitor.visitTuple_expr(self)
            else:
                return visitor.visitChildren(self)




    def tuple_expr(self):

        localctx = SignalFlowV2Parser.Tuple_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 96, self.RULE_tuple_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 489
            self.match(SignalFlowV2Parser.OPEN_PAREN)
            self.state = 491
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NOT_OP) | (1 << SignalFlowV2Parser.OPEN_BRACE))) != 0):
                self.state = 490
                self.testlist()


            self.state = 493
            self.match(SignalFlowV2Parser.CLOSE_PAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Dict_exprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Dict_exprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def OPEN_BRACE(self):
            return self.getToken(SignalFlowV2Parser.OPEN_BRACE, 0)

        def CLOSE_BRACE(self):
            return self.getToken(SignalFlowV2Parser.CLOSE_BRACE, 0)

        def test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.TestContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_dict_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterDict_expr"):
                listener.enterDict_expr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitDict_expr"):
                listener.exitDict_expr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitDict_expr"):
                return visitor.visitDict_expr(self)
            else:
                return visitor.visitChildren(self)




    def dict_expr(self):

        localctx = SignalFlowV2Parser.Dict_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 98, self.RULE_dict_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 495
            self.match(SignalFlowV2Parser.OPEN_BRACE)
            self.state = 512
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NOT_OP) | (1 << SignalFlowV2Parser.OPEN_BRACE))) != 0):
                self.state = 496
                self.test()
                self.state = 497
                self.match(SignalFlowV2Parser.COLON)
                self.state = 498
                self.test()
                self.state = 506
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,58,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 499
                        self.match(SignalFlowV2Parser.COMMA)
                        self.state = 500
                        self.test()
                        self.state = 501
                        self.match(SignalFlowV2Parser.COLON)
                        self.state = 502
                        self.test() 
                    self.state = 508
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,58,self._ctx)

                self.state = 510
                _la = self._input.LA(1)
                if _la==SignalFlowV2Parser.COMMA:
                    self.state = 509
                    self.match(SignalFlowV2Parser.COMMA)




            self.state = 514
            self.match(SignalFlowV2Parser.CLOSE_BRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TestlistContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.TestlistContext, self).__init__(parent, invokingState)
            self.parser = parser

        def test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.TestContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,i)


        def COMMA(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.COMMA)
            else:
                return self.getToken(SignalFlowV2Parser.COMMA, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_testlist

        def enterRule(self, listener):
            if hasattr(listener, "enterTestlist"):
                listener.enterTestlist(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitTestlist"):
                listener.exitTestlist(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitTestlist"):
                return visitor.visitTestlist(self)
            else:
                return visitor.visitChildren(self)




    def testlist(self):

        localctx = SignalFlowV2Parser.TestlistContext(self, self._ctx, self.state)
        self.enterRule(localctx, 100, self.RULE_testlist)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 516
            self.test()
            self.state = 521
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,61,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 517
                    self.match(SignalFlowV2Parser.COMMA)
                    self.state = 518
                    self.test() 
                self.state = 523
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,61,self._ctx)

            self.state = 525
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.COMMA:
                self.state = 524
                self.match(SignalFlowV2Parser.COMMA)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Actual_argsContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Actual_argsContext, self).__init__(parent, invokingState)
            self.parser = parser

        def argument(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.ArgumentContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.ArgumentContext,i)


        def COMMA(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.COMMA)
            else:
                return self.getToken(SignalFlowV2Parser.COMMA, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_actual_args

        def enterRule(self, listener):
            if hasattr(listener, "enterActual_args"):
                listener.enterActual_args(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitActual_args"):
                listener.exitActual_args(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitActual_args"):
                return visitor.visitActual_args(self)
            else:
                return visitor.visitChildren(self)




    def actual_args(self):

        localctx = SignalFlowV2Parser.Actual_argsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 102, self.RULE_actual_args)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 527
            self.argument()
            self.state = 532
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.COMMA:
                self.state = 528
                self.match(SignalFlowV2Parser.COMMA)
                self.state = 529
                self.argument()
                self.state = 534
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ArgumentContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.ArgumentContext, self).__init__(parent, invokingState)
            self.parser = parser

        def test(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,0)


        def ID(self):
            return self.getToken(SignalFlowV2Parser.ID, 0)

        def ASSIGN(self):
            return self.getToken(SignalFlowV2Parser.ASSIGN, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_argument

        def enterRule(self, listener):
            if hasattr(listener, "enterArgument"):
                listener.enterArgument(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitArgument"):
                listener.exitArgument(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitArgument"):
                return visitor.visitArgument(self)
            else:
                return visitor.visitChildren(self)




    def argument(self):

        localctx = SignalFlowV2Parser.ArgumentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 104, self.RULE_argument)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 537
            self._errHandler.sync(self);
            la_ = self._interp.adaptivePredict(self._input,64,self._ctx)
            if la_ == 1:
                self.state = 535
                self.match(SignalFlowV2Parser.ID)
                self.state = 536
                self.match(SignalFlowV2Parser.ASSIGN)


            self.state = 539
            self.test()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





