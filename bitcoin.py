#!/usr/bin/env python3
from electrum import (
  SimpleConfig,
  network,
  util,
  bitcoin,
)
import asyncio
import threading
from time import sleep

# Get the global network object started
loop = asyncio.get_event_loop()
stopping_fut = asyncio.Future()
loop_thread = threading.Thread(
    target=loop.run_until_complete,
    args=(stopping_fut,),
    name='EventLoop')
loop_thread.start()
n = network.Network(SimpleConfig())
n.start()


async def end_thread():
    stopping_fut.set_result(1)
asyncio.run_coroutine_threadsafe(end_thread(), loop).result()


class Bitcoin:
    # Simple decorator which starts new event loop and then kills it after
    def with_new_event_loop(func):
        async def end_thread(stopping_fut):
            stopping_fut.set_result(1)

        def func_wrapper(self, *args, **kwargs):
            self.loop, self.stopping_fut, self.loop_thread = \
                util.create_and_start_event_loop()
            retval = func(self, *args, **kwargs)
            asyncio.run_coroutine_threadsafe(
                end_thread(self.stopping_fut), self.loop).result()
            return retval
        return func_wrapper

    @with_new_event_loop
    def fee_estimates(self):
        sleep(3)
        try:
            fee_time_values = [
                (25, '~6hr'),
                (10, '~2hr'),
                (5, '~60min'),
                (2, '~20min'),
                (1, '~10min')]
            output = {}
            for i in fee_time_values:
                output[i[1]] = n.config.eta_target_to_fee(i[0])/1000
            return {'status': 'successful', 'data': output}
        except Exception as exception:
            return {'status': 'error', 'data': exception}


# Doesn't caush crash
b = Bitcoin()
output = b.fee_estimates()
print(output['data'])
