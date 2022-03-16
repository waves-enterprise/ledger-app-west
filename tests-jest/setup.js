import { default as TransportNodeSpeculos } from '@ledgerhq/hw-transport-node-speculos'
import { WestSpeculos } from '@wavesenterprise/west-ledger'
import { APDU_PORT, BUTTON_DELAY, BUTTON_PORT, CHAIN_ID } from './constants'

module.exports = async (globalObj) => {
  const ledger = new WestSpeculos(
    TransportNodeSpeculos,
    CHAIN_ID,
    {
      buttonPort: BUTTON_PORT,
      apduPort: APDU_PORT,
      buttonDelay: BUTTON_DELAY,
    },
  )

  process.__LEDGER__ = ledger
  await ledger.connect()
}
