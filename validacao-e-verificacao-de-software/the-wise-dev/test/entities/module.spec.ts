import { Lecture, Module } from '../../src/entities'
import { ExistingElementError } from '../../src/entities/errors/existing-element-error'
import { InvalidPositionError } from '../../src/entities/errors/invalid-position-error'
import { UnexistingElementError } from '../../src/entities/errors/unexisting-element-error'

describe('Module', () => {
  it('should be able to add lectures to modules', () => {
    const module = new Module('Fundamentals')
    const lecture: Lecture = new Lecture('Branching', 'https://youtube.com/1234')
    module.add(lecture)
    expect(module.includes(lecture)).toBeTruthy()
  })

  it('should not be able to have two lectures with same name in a module', () => {
    const module = new Module('Fundamentals')
    const lecture: Lecture = new Lecture('Branching', 'https://youtube.com/1234')
    const otherLecture: Lecture = new Lecture('Branching', 'https://youtube.com/3456')
    module.add(lecture)
    const error = module.add(otherLecture).value
    expect(module.includes(lecture)).toBeTruthy()
    expect(module.numberOfLectures).toEqual(1)
    expect(error).toBeInstanceOf(ExistingElementError)
  })

  it('should be able to rearrange the order of lectures', () => {
    const module = new Module('Fundamentals')
    const branching: Lecture = new Lecture('Branching', 'https://youtube.com/branching')
    const commiting: Lecture = new Lecture('Commiting', 'https://youtube.com/commiting')
    const pushing: Lecture = new Lecture('Pushing', 'https://youtube.com/pushing')

    module.add(branching)
    module.add(commiting)
    module.add(pushing)

    module.move(branching, 3)

    expect(module.position(commiting).value).toBe(1)
    expect(module.position(pushing).value).toBe(2)
    expect(module.position(branching).value).toBe(3)
  })

  it('should not be able to move unexisting lecture', () => {
    const module = new Module('Fundamentals')
    const branching: Lecture = new Lecture('Branching', 'https://youtube.com/branching')
    const commiting: Lecture = new Lecture('Commiting', 'https://youtube.com/commiting')
    const pushing: Lecture = new Lecture('Pushing', 'https://youtube.com/pushing')

    module.add(branching)
    module.add(commiting)
    const error = module.move(pushing, 1).value as Error
    expect(error).toBeInstanceOf(UnexistingElementError)
  })

  it('should handle exceeding position while rearranging', () => {
    const module = new Module('Fundamentals')
    const branching: Lecture = new Lecture('Branching', 'https://youtube.com/branching')
    const commiting: Lecture = new Lecture('Commiting', 'https://youtube.com/commiting')
    const pushing: Lecture = new Lecture('Pushing', 'https://youtube.com/pushing')

    module.add(branching)
    module.add(commiting)
    module.add(pushing)

    const error = module.move(branching, 10).value as Error
    expect(error).toBeInstanceOf(InvalidPositionError)

    expect(module.position(branching).value).toBe(1)
    expect(module.position(commiting).value).toBe(2)
    expect(module.position(pushing).value).toBe(3)
  })

  it('should handle negative position while rearranging', () => {
    const module = new Module('Fundamentals')
    const branching: Lecture = new Lecture('Branching', 'https://youtube.com/branching')
    const commiting: Lecture = new Lecture('Commiting', 'https://youtube.com/commiting')
    const pushing: Lecture = new Lecture('Pushing', 'https://youtube.com/pushing')

    module.add(branching)
    module.add(commiting)
    module.add(pushing)

    const error = module.move(branching, 0).value as Error
    expect(error).toBeInstanceOf(InvalidPositionError)

    expect(module.position(branching).value).toBe(1)
    expect(module.position(commiting).value).toBe(2)
    expect(module.position(pushing).value).toBe(3)
  })

  it('should be able to remove a lecture', () => {
    const module = new Module('Fundamentals')
    const branching: Lecture = new Lecture('Branching', 'https://youtube.com/branching')
    module.add(branching)
    module.remove(branching)
    expect(module.numberOfLectures).toEqual(0)
  })

  it('should be able to handle trying to remove an unexisting lecture', () => {
    const module = new Module('Fundamentals')
    const branching: Lecture = new Lecture('Branching', 'https://youtube.com/branching')
    const commiting: Lecture = new Lecture('Commiting', 'https://youtube.com/commiting')
    module.add(commiting)
    const error = module.remove(branching).value as Error
    expect(error).toBeInstanceOf(UnexistingElementError)
    expect(module.numberOfLectures).toEqual(1)
  })

  it('should not be able to determine position of unexisting lecture', () => {
    const module = new Module('Fundamentals')
    const lecture: Lecture = new Lecture('Branching', 'https://youtube.com/1234')
    const error = module.position(lecture).value as Error
    expect(error).toBeInstanceOf(UnexistingElementError)
  })
})
