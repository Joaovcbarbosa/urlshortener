export class InvalidPositionError extends Error {
  public readonly name = 'InvalidPositionError'
  constructor () {
    super('Invalid position.')
  }
}
