test('Bad CLA', async () => {
  const { __LEDGER__: ledger } = process
  await expect(ledger.api.custom(0x01, 0x02)).rejects.toMatchObject({ statusText: 'CLA_NOT_SUPPORTED' })
})

test('Bad INS', async () => {
  const { __LEDGER__: ledger } = process
  await expect(ledger.api.custom(0x80, 0x01)).rejects.toMatchObject({ statusText: 'INS_NOT_SUPPORTED' })
})

test('Wrong P1 P2', async () => {
  const { __LEDGER__: ledger } = process
  await expect(ledger.api.custom(0x80, 0x02, 0x01, 0x02)).rejects.toMatchObject({ statusCode: 0x6A86 })
})
