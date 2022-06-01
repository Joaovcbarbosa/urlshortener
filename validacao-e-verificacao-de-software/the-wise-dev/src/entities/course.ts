import { Lecture } from '.'
import { Either } from '../shared/either'
import { Container } from './container'
import { ExistingElementError } from './errors/existing-element-error'
import { InvalidPositionError } from './errors/invalid-position-error'
import { UnexistingElementError } from './errors/unexisting-element-error'
import { Module } from './module'
import { User } from './user'

type CourseElement = Module | Lecture

export class Course {
  private readonly elements: Container<CourseElement> = new Container<CourseElement>()
  public reference: string
  public title: string
  public description: string
  public authors: User[]

  constructor (reference: string, title: string, description: string, authors: User[]) {
    this.reference = reference
    this.title = title
    this.description = description
    this.authors = authors
  }

  get numberOfElements (): number {
    return this.elements.numberOfElements
  }

  add (element: CourseElement): Either<ExistingElementError, void> {
    return this.elements.add(element)
  }

  remove (element: CourseElement): Either<UnexistingElementError, void> {
    return this.elements.remove(element)
  }

  includes (element: CourseElement): boolean {
    return this.elements.includes(element)
  }

  move (element: CourseElement, position: number): Either<UnexistingElementError | InvalidPositionError, void> {
    return this.elements.move(element, position)
  }

  position (element: CourseElement): Either<UnexistingElementError, number> {
    return this.elements.position(element)
  }

  moveLecture (lecture: Lecture, from: Module | Course, toModule: Module, position: number): void {
    from.remove(lecture)
    toModule.add(lecture)
    const currentLecturePosition = toModule.position(lecture).value
    if (currentLecturePosition !== position) toModule.move(lecture, position)
  }

  equals (other: Course): boolean {
    return this.reference === other.reference
  }
}
