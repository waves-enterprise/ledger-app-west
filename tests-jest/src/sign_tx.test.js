import * as WeSdk from '@wavesenterprise/js-sdk'
import { CHAIN_ID } from '../constants'
import { sleep } from '../utils'

const weSdk = WeSdk.create({
  initialConfiguration: {
    ...WeSdk.MAINNET_CONFIG,
    nodeAddress: 'http://dummy',
    crypto: 'waves',
    networkByte: CHAIN_ID
  },
  fetchInstance: {}
})

test('Sign transfer transaction', async () => {
  const { __LEDGER__: ledger } = process

  const userId = 1

  const { publicKey } = await ledger.api.getAddressDataById(userId)
  const { address } = await ledger.api.getAddressDataById(2)

  const txData = {
    recipient: address,
    senderPublicKey: publicKey,
    amount: 10 * 10e7,
    fee: 10000000,
    attachment: '',
    timestamp: Date.now()
  }

  const tx = weSdk.API.Transactions.Transfer.V2(txData)

  const bytes = await tx.getSignatureBytes()

  ;(async () => {
    await sleep(500)

    // Review Transaction
    await ledger.button.right()

    // Amount
    await ledger.button.right()

    // Asset
    await ledger.button.right()

    // To
    await ledger.button.right()
    await ledger.button.right()

    // Fee
    await ledger.button.right()

    // Fee Asset
    await ledger.button.right()

    // From
    await ledger.button.right()
    await ledger.button.right()

    // Tx
    await ledger.button.right()
    await ledger.button.right()
    await ledger.button.right()

    // Approve
    await ledger.button.right()

    await ledger.button.both()
  })()

  const signature = await ledger.api.signTransferTx(userId, {
    type: 4, version: 2,
    data: Buffer.from(bytes)
  }, true)

  let isValid = false
  try {
    isValid = weSdk.crypto.isValidSignature(bytes, signature, publicKey)
  } catch (e) {}

  expect(isValid).toBeTruthy()
}, 15000)


test('Sign custom transaction', async () => {
  const { __LEDGER__: ledger } = process

  const userId = 1

  const { publicKey } = await ledger.api.getAddressDataById(userId)
  const { address } = await ledger.api.getAddressDataById(2)

  const txData = {
    recipient: address,
    senderPublicKey: publicKey,
    amount: 10 * 10e7,
    fee: 10000000,
    attachment: '',
    timestamp: Date.now()
  }

  const tx = weSdk.API.Transactions.Transfer.V2(txData)

  const bytes = await tx.getSignatureBytes()

  ;(async () => {
    await sleep(500)

    // Review Transaction
    await ledger.button.right()

    // Field1: test
    await ledger.button.right()

    await ledger.button.both()
  })()

  const signature = await ledger.api.sign(userId, Buffer.from(bytes), { field1: 'test' }, true)

  let isValid = false
  try {
    isValid = weSdk.crypto.isValidSignature(bytes, signature, publicKey)
  } catch (e) {}

  expect(isValid).toBeTruthy()
}, 15000)
