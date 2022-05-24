import { Either } from '../shared/either'
import { Container } from './container'
import { ExistingElementError } from './errors/existing-element-error'
import { InvalidPositionError } from './errors/invalid-position-error'
import { UnexistingElementError } from './errors/unexisting-element-error'
import { Lecture } from './lecture'
import { Element } from './part'

export class Module implements Element {
  private readonly lectures: Container<Lecture> = new Container<Lecture>()
  public readonly title: string
  constructor (title: string) {
    this.title = title
  }

  get numberOfLectures (): number {
    return this.lectures.numberOfElements
  }

  add (lecture: Lecture): Either<ExistingElementError, void> {
    return this.lectures.add(lecture)
  }

  includes (lecture: Lecture): boolean {
    return this.lectures.includes(lecture)
  }

  move (lecture: Lecture, position: number): Either<UnexistingElementError | InvalidPositionError, void> {
    return this.lectures.move(lecture, position)
  }

  position (lecture: Lecture): Either<UnexistingElementError, number> {
    return this.lectures.position(lecture)
  }

  remove (lecture: Lecture): Either<UnexistingElementError, void> {
    return this.lectures.remove(lecture)
  }

  equals (module: Module): boolean {
    return this.title === module.title
  }
}
