import pytest

from network_pytest.checks import stp_root


pytestmark = [pytest.mark.offline, pytest.mark.layer2]


def test_stp_root_matches_case_insensitively():
    assert stp_root("0010.aaaa.bbbb", "0010.AAAA.BBBB", 0).passed
    assert not stp_root("0010.aaaa.bbbb", "0020.cccc.dddd", 1).passed

