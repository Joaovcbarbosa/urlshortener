export class UnexistingElementError extends Error {
  public readonly name = 'UnexistingElementError'
  constructor () {
    super('Element does not exist.')
  }
}
