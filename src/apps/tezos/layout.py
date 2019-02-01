from trezor import ui
from trezor.messages import ButtonRequestType
from trezor.ui.text import Text
from trezor.utils import chunks, format_amount

from apps.common.confirm import require_confirm, require_hold_to_confirm
from apps.tezos.helpers import TEZOS_AMOUNT_DIVISIBILITY


async def require_confirm_tx(ctx, to, value):
    text = Text("Confirm sending", ui.ICON_SEND, icon_color=ui.GREEN)
    text.bold(format_tezos_amount(value))
    text.normal("to")
    text.mono(*split_address(to))
    return await require_confirm(ctx, text, ButtonRequestType.SignTx)


async def require_confirm_fee(ctx, value, fee):
    text = Text("Confirm transaction", ui.ICON_SEND, icon_color=ui.GREEN)
    text.normal("Amount:")
    text.bold(format_tezos_amount(value))
    text.normal("Fee:")
    text.bold(format_tezos_amount(fee))
    await require_hold_to_confirm(ctx, text, ButtonRequestType.SignTx)


async def require_confirm_origination(ctx, address):
    text = Text("Confirm origination", ui.ICON_SEND, icon_color=ui.ORANGE)
    text.normal("Address:")
    text.mono(*split_address(address))
    return await require_confirm(ctx, text, ButtonRequestType.SignTx)


async def require_confirm_origination_fee(ctx, balance, fee):
    text = Text("Confirm origination", ui.ICON_SEND, icon_color=ui.ORANGE)
    text.normal("Balance:")
    text.bold(format_tezos_amount(balance))
    text.normal("Fee:")
    text.bold(format_tezos_amount(fee))
    await require_hold_to_confirm(ctx, text, ButtonRequestType.SignTx)


async def require_confirm_delegation_baker(ctx, baker):
    text = Text("Confirm delegation", ui.ICON_SEND, icon_color=ui.BLUE)
    text.normal("Baker address:")
    text.mono(*split_address(baker))
    return await require_confirm(ctx, text, ButtonRequestType.SignTx)


async def require_confirm_set_delegate(ctx, fee):
    text = Text("Confirm delegation", ui.ICON_SEND, icon_color=ui.BLUE)
    text.normal("Fee:")
    text.bold(format_tezos_amount(fee))
    await require_hold_to_confirm(ctx, text, ButtonRequestType.SignTx)


async def require_confirm_register_delegate(ctx, address, fee):
    text = Text("Register delegate", ui.ICON_SEND, icon_color=ui.BLUE)
    text.bold("Fee: " + format_tezos_amount(fee))
    text.normal("Address:")
    text.mono(*split_address(address))
    await require_hold_to_confirm(ctx, text, ButtonRequestType.SignTx)


async def require_confirm_staking(ctx):
    text = Text("Confirm staking", ui.ICON_SEND, icon_color=ui.GREEN)
    text.bold("Confirm?")
    return await require_hold_to_confirm(ctx, text, ButtonRequestType.SignTx)


def show_staking_signature(signature, watermark):
    ui.display.clear()
    text = Text("Signed", ui.ICON_SEND, icon_color=ui.GREEN)
    text.bold("Type: " + get_operation(watermark))
    text.bold("Signature:")
    text.normal(signature)
    text.render()


async def no_pin_dialog(ctx):
    text = Text("Pin is not set", ui.ICON_WRONG, icon_color=ui.RED)
    text.normal("You need to set a pin to start staking")
    return await require_confirm(ctx, text, ButtonRequestType.Other)


def split_address(address):
    return chunks(address, 18)


def format_tezos_amount(value):
    formatted_value = format_amount(value, TEZOS_AMOUNT_DIVISIBILITY)
    return formatted_value + " XTZ"


def get_operation(wm):
    if wm is 1:
        return "Block"
    else:
        return "Endorsement"
