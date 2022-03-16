module.exports = async () => {
  await process.__LEDGER__.disconnect()
  process.exit(0)
}
