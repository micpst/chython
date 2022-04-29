# -*- coding: utf-8 -*-
#
#  Copyright 2022 Ramil Nugmanov <nougmanoff@protonmail.com>
#  This file is part of chython.
#
#  chython is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, see <https://www.gnu.org/licenses/>.
#
from chython import smiles, smarts, Transformer
from chython.reactor import deprotection
from itertools import product


def test_deprotection():
    qs = set()
    ts = set()
    for x in dir(deprotection):
        for r in getattr(deprotection, x[9:]):
            if len(r) > 2:  # has test
                q, p, t, a, *bs = r
                t = smiles(t)
                t.canonicalize()
                q = smarts(q)
                qs.add(q)
                ts.add(t)
                a = smiles(a)
                a.canonicalize()
                # test match
                assert q < t, f'{q} !< {t}'
                o = next(Transformer(q, smarts(p))(t))
                assert o == a, f'{o} != {a}'
                for b in bs:
                    b = smiles(b)
                    b.canonicalize()
                    assert not q < b, f'{q} < {b}'

    # test rule-test is unique pair
    assert len(qs) == len(ts)

    m = 0
    for q, t in product(qs, ts):
        m += q < t

    # test selectivity of rules
    assert len(qs) == m
