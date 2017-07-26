# This file is part of Maker Keeper Framework.
#
# Copyright (C) 2017 reverendus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import asyncio

import pytest

from api.util import synchronize, int_to_bytes32, bytes_to_int, bytes_to_hexstring, hexstring_to_bytes


async def async_return(result):
    return result


async def async_exception():
    await asyncio.sleep(0.1)
    raise Exception("Exception to be passed further down")


def test_synchronize_should_return_empty_list_for_no_futures():
    assert synchronize([]) == []


def test_synchronize_should_return_results_of_all_async_calls():
    assert synchronize([async_return(1)]) == [1]
    assert synchronize([async_return(1), async_return(2)]) == [1, 2]
    assert synchronize([async_return(1), async_return(2), async_return(3)]) == [1, 2, 3]


def test_synchronize_should_pass_exceptions():
    with pytest.raises(Exception):
        synchronize([async_return(1), async_exception(), async_return(3)])


def test_int_to_bytes32():
    assert int_to_bytes32(0) == bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                       0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                       0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                       0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    assert int_to_bytes32(1) == bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                       0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                       0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                       0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01])

    assert int_to_bytes32(512) == bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                         0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                         0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                         0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00])
    
    assert int_to_bytes32(2**256-1) == bytes([0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                                              0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                                              0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                                              0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff])


def test_bytes_to_int():
    assert bytes_to_int(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                               0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                               0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                               0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])) == 0

    assert bytes_to_int(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                               0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                               0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                               0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01])) == 1

    assert bytes_to_int(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                               0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                               0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                               0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01])) == 257

    assert bytes_to_int(bytes([0x00])) == 0

    assert bytes_to_int(bytes([0x01, 0x01])) == 257

    assert bytes_to_int(bytes([0x00, 0x01, 0x01])) == 257

    assert bytes_to_int(bytes([0x00, 0x00, 0x01, 0x01])) == 257

    assert bytes_to_int(bytes([0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                               0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                               0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                               0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff])) == 2**256-1


def test_bytes_to_int_from_string():
    assert bytes_to_int('\x00') == 0
    assert bytes_to_int('\x01') == 1
    assert bytes_to_int('\x01\x01') == 257
    assert bytes_to_int('\x00\x01\x01') == 257
    assert bytes_to_int('\x00\x00\x01\x01') == 257


def test_bytes_to_hexstring():
    assert bytes_to_hexstring(bytes([0x00])) == '0x00'
    assert bytes_to_hexstring(bytes([0x01, 0x02, 0x03])) == '0x010203'
    assert bytes_to_hexstring(bytes([0xff, 0xff])) == '0xffff'


def test_hexstring_to_bytes():
    assert hexstring_to_bytes('0x00') == bytes([0x00])
    assert hexstring_to_bytes('0x010203') == bytes([0x01, 0x02, 0x03])
    assert hexstring_to_bytes('0xffff') == bytes([0xff, 0xff])
