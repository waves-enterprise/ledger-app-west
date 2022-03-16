test('Get app name', async () => {
  const { __LEDGER__: ledger } = process
  expect(await ledger.api.getAppName()).toEqual('Waves Enterprise')
})
