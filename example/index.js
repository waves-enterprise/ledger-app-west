/* package.json
{
  "name": "example",
  "version": "0.0.1",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "",
  "license": "ISC",
  "dependencies": {
    "@ledgerhq/hw-transport-node-hid": "^6.20.0",
    "@wavesenterprise/js-sdk": "^3.2.7",
    "@wavesenterprise/west-ledger": "^0.1.0"
  }
}
*/

const TransportNodeHid = require('@ledgerhq/hw-transport-node-hid').default
const { WestLedger } = require('@wavesenterprise/west-ledger')
const WeSdk = require('@wavesenterprise/js-sdk')

;(async () => {
  const networkCode = 'V'.charCodeAt(0)
  const ledger = new WestLedger(
    TransportNodeHid,
    networkCode,
    {
      debug: true,
    },
  )
  try {
    await ledger.connect()

    console.log(`\n\nGET VERSION\n`)
    const version = await ledger.getVersion()
    console.log('Version:', version)


    console.log(`\n\nGET WALLET DATA\n`)
    const USER_ID = 1
    const user = await ledger.getUserDataById(USER_ID)
    console.log(user)


    console.log(`\n\nVERIFY ADDRESS\n`)
    const resp = await ledger.getWalletPublicKeyAndAddress(user.path, true)
    console.warn(resp)


    console.log(`\n\nSIGN TX\n`)
    const weSdk = WeSdk.create({
      initialConfiguration: {
        ...WeSdk.MAINNET_CONFIG,
        nodeAddress: 'https://carter.welocal.dev/node-0',
        crypto: 'waves',
        networkByte: 'V'.charCodeAt(0),
      },
      fetchInstance: {},
    })

    const address = '3NrkgkuM3k7urnoSD9wAhGUzdaSVgzAqapN'

    const tx = weSdk.API.Transactions.Transfer.V2({
      recipient: address, // Send tokens to the same address
      senderPublicKey: user.publicKey,
      amount: 10 * 10e7,
      fee: 10000000,
      attachment: '',
      timestamp: Date.now(),
    })

    const bytes = await tx.getSignatureBytes()

    const signature = await ledger.signTransaction(USER_ID, {
      dataType: 4, dataVersion: 2,
      dataBuffer: Buffer.from(bytes),
    })

    const signedTx = {
      ...tx.getBody(),
      proofs: [signature],
    }

    console.log(`\n\nTX:`, JSON.stringify(signedTx))

    console.log(`\n\nSIGNATURE:`, signature)

    let isValid = false
    try {
      isValid = weSdk.crypto.isValidSignature(bytes, signature, user.publicKey)
    } catch (e) {}
    console.log(`\n\nVALID:`, isValid)

    await ledger.disconnect()
  } catch (e) {
    console.error(e)
  }
})()
