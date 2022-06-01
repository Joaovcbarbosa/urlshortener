export class ExistingElementError extends Error {
  public readonly name = 'ExistingElementError'
  constructor () {
    super('Element already exists.')
  }
}
