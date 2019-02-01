from trezor import config
from trezor.messages.Failure import Failure
from trezor.messages.Success import Success
from trezor.pin import pin_to_int

from apps.common.request_pin import request_pin
from apps.tezos import helpers, layout


async def control_staking(ctx, msg):

    if not config.has_pin():
        await layout.no_pin_dialog(ctx)
        return Failure()

    if msg.staking is True:
        if not helpers.check_staking_confirmed():
            await layout.require_confirm_staking(ctx)
            helpers.set_staking_state(True)
        else:
            return Failure()
    else:
        if helpers.check_staking_confirmed():
            await helpers.prompt_pin()
            helpers.set_staking_state(False)
        else:
            return Failure()

    return Success()
