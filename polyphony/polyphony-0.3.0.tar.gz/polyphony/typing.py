import abc

__all__ = [
    'bit',
    'List',
    'Tuple',
]
__all__ += ['int' + str(i) for i in range(2, 129)]
__all__ += ['uint' + str(i) for i in range(2, 129)]


class GenericMeta(abc.ABCMeta):
    def __getitem__(self, i):
        return self.__class__(self.__name__, self.__bases__, dict(self.__dict__))


class List(list, metaclass=GenericMeta):
    pass


class Tuple(tuple, metaclass=GenericMeta):
    pass


bit = int
int2 = int
int3 = int
int4 = int
int5 = int
int6 = int
int7 = int
int8 = int
int9 = int
int10 = int
int11 = int
int12 = int
int13 = int
int14 = int
int15 = int
int16 = int
int17 = int
int18 = int
int19 = int
int20 = int
int21 = int
int22 = int
int23 = int
int24 = int
int25 = int
int26 = int
int27 = int
int28 = int
int29 = int
int30 = int
int31 = int
int32 = int
int33 = int
int34 = int
int35 = int
int36 = int
int37 = int
int38 = int
int39 = int
int40 = int
int41 = int
int42 = int
int43 = int
int44 = int
int45 = int
int46 = int
int47 = int
int48 = int
int49 = int
int50 = int
int51 = int
int52 = int
int53 = int
int54 = int
int55 = int
int56 = int
int57 = int
int58 = int
int59 = int
int60 = int
int61 = int
int62 = int
int63 = int
int64 = int
int65 = int
int66 = int
int67 = int
int68 = int
int69 = int
int70 = int
int71 = int
int72 = int
int73 = int
int74 = int
int75 = int
int76 = int
int77 = int
int78 = int
int79 = int
int80 = int
int81 = int
int82 = int
int83 = int
int84 = int
int85 = int
int86 = int
int87 = int
int88 = int
int89 = int
int90 = int
int91 = int
int92 = int
int93 = int
int94 = int
int95 = int
int96 = int
int97 = int
int98 = int
int99 = int
int100 = int
int101 = int
int102 = int
int103 = int
int104 = int
int105 = int
int106 = int
int107 = int
int108 = int
int109 = int
int110 = int
int111 = int
int112 = int
int113 = int
int114 = int
int115 = int
int116 = int
int117 = int
int118 = int
int119 = int
int120 = int
int121 = int
int122 = int
int123 = int
int124 = int
int125 = int
int126 = int
int127 = int
int128 = int

uint2 = int
uint3 = int
uint4 = int
uint5 = int
uint6 = int
uint7 = int
uint8 = int
uint9 = int
uint10 = int
uint11 = int
uint12 = int
uint13 = int
uint14 = int
uint15 = int
uint16 = int
uint17 = int
uint18 = int
uint19 = int
uint20 = int
uint21 = int
uint22 = int
uint23 = int
uint24 = int
uint25 = int
uint26 = int
uint27 = int
uint28 = int
uint29 = int
uint30 = int
uint31 = int
uint32 = int
uint33 = int
uint34 = int
uint35 = int
uint36 = int
uint37 = int
uint38 = int
uint39 = int
uint40 = int
uint41 = int
uint42 = int
uint43 = int
uint44 = int
uint45 = int
uint46 = int
uint47 = int
uint48 = int
uint49 = int
uint50 = int
uint51 = int
uint52 = int
uint53 = int
uint54 = int
uint55 = int
uint56 = int
uint57 = int
uint58 = int
uint59 = int
uint60 = int
uint61 = int
uint62 = int
uint63 = int
uint64 = int
uint65 = int
uint66 = int
uint67 = int
uint68 = int
uint69 = int
uint70 = int
uint71 = int
uint72 = int
uint73 = int
uint74 = int
uint75 = int
uint76 = int
uint77 = int
uint78 = int
uint79 = int
uint80 = int
uint81 = int
uint82 = int
uint83 = int
uint84 = int
uint85 = int
uint86 = int
uint87 = int
uint88 = int
uint89 = int
uint90 = int
uint91 = int
uint92 = int
uint93 = int
uint94 = int
uint95 = int
uint96 = int
uint97 = int
uint98 = int
uint99 = int
uint100 = int
uint101 = int
uint102 = int
uint103 = int
uint104 = int
uint105 = int
uint106 = int
uint107 = int
uint108 = int
uint109 = int
uint110 = int
uint111 = int
uint112 = int
uint113 = int
uint114 = int
uint115 = int
uint116 = int
uint117 = int
uint118 = int
uint119 = int
uint120 = int
uint121 = int
uint122 = int
uint123 = int
uint124 = int
uint125 = int
uint126 = int
uint127 = int
uint128 = int

