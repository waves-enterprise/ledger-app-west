const path = '44\'/5741565\'/0\'/0\'/1\''
const { __LEDGER__: ledger } = process

test('Get publicKey and address silently', async () => {
  const { __LEDGER__: ledger } = process
  const { publicKey, address } = await ledger.api.getWalletPublicKeyAndAddress(path)
  expect(publicKey).toEqual('FcN7XKSSMVhorKrxjdJ2DZdkFCCewcHA7SY3ZU1tA4GV')
  expect(address).toEqual('3NjPt5DqWrPc9KrTRYj8Srwh7oEnM9XZvdj')
})

test('Get publicKey and address with verification', async () => {
  (async () => {
    await ledger.button.right()
    await ledger.button.right()
    await ledger.button.right()
    await ledger.button.both()
  })().then()
  const { publicKey, address } = await ledger.api.getWalletPublicKeyAndAddress(path, true)
  expect(publicKey).toEqual('FcN7XKSSMVhorKrxjdJ2DZdkFCCewcHA7SY3ZU1tA4GV')
  expect(address).toEqual('3NjPt5DqWrPc9KrTRYj8Srwh7oEnM9XZvdj')
})
