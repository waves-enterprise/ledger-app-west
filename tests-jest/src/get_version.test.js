test('Get version', async () => {
  const { __LEDGER__: ledger } = process
  expect(await ledger.api.getVersion()).toEqual([1, 0, 4])
})
