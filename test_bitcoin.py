import pytest
from time import sleep
from bitcoin import Bitcoin

b = Bitcoin()


class TestBTCFeeEstimates:
    def test_btc_fee_estimate(self):
        sleep(1)
        output = b.fee_estimates()
        print(output['data'])
        assert output['status'] == 'successful'
