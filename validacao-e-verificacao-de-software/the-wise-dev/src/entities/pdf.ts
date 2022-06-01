import { Material } from './material'

export class Pdf implements Material {
  url: string
  readonly title: string

  constructor (title: string, url: string) {
    this.title = title
    this.url = url
  }

  equals (pdf: Pdf): boolean {
    return this.title === pdf.title
  }
}
