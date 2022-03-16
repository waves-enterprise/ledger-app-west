test('Get address details', async () => {
  const { __LEDGER__: ledger } = process
  const { publicKey, address, id, path } = await ledger.api.getAddressDataById(1)

  expect(publicKey).toEqual('FcN7XKSSMVhorKrxjdJ2DZdkFCCewcHA7SY3ZU1tA4GV')
  expect(address).toEqual('3NjPt5DqWrPc9KrTRYj8Srwh7oEnM9XZvdj')
  expect(id).toEqual(1)
  expect(path).toEqual('44\'/5741565\'/0\'/0\'/1\'')
})
