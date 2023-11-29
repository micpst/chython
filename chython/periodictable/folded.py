# -*- coding: utf-8 -*-
#
#  Copyright 2023 Ramil Nugmanov <nougmanoff@protonmail.com>
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
from typing import Dict, Optional, Tuple

from chython.periodictable import Element


class FoldedGroup(Element):
    def __init__(self, number: int):
        super().__init__()
        self._number = number + 118

    @property
    def atomic_symbol(self) -> str:
        return f"T{self._number}"

    @property
    def atomic_number(self) -> Optional[int]:
        if self is None:
            return None
        return self._number

    @property
    def isotopes_distribution(self) -> Dict:
        return {}

    @property
    def isotopes_masses(self) -> Dict:
        return {}

    @property
    def atomic_radius(self) -> float:
        return 0.0

    def copy(self) -> "FoldedGroup":
        copy = super().copy()
        copy._number = self._number
        return copy

    @property
    def _common_valences(self) -> Tuple:
        return (0,)

    @property
    def _valences_exceptions(self) -> Tuple:
        return ()
