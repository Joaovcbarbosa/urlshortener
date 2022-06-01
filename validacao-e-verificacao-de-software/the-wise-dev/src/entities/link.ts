import { Material } from './material'

export class Link implements Material {
  url: string
  readonly title: string

  constructor (title: string, url: string) {
    this.title = title
    this.url = url
  }

  equals (link: Link): boolean {
    return this.title === link.title
  }
}
