import { Lecture } from '../../src/entities'
import { ExistingElementError } from '../../src/entities/errors/existing-element-error'
import { UnexistingElementError } from '../../src/entities/errors/unexisting-element-error'
import { Link } from '../../src/entities/link'
import { Material } from '../../src/entities/material'
import { Pdf } from '../../src/entities/pdf'

describe('Lecture', () => {
  it('should be able to add further material to lectures', () => {
    const lecture: Lecture = new Lecture('Branching', 'https://youtube.com/1234')
    const branchingPdf: Material = new Pdf('Branching', 'https://storage/branching.pdf')
    lecture.add(branchingPdf)
    expect(lecture.includes(branchingPdf)).toBeTruthy()
  })

  it('should be able to remove further material from lectures', () => {
    const lecture: Lecture = new Lecture('Branching', 'https://youtube.com/1234')
    const branchingPdf: Material = new Pdf('Branching', 'https://storage/branching.pdf')
    lecture.add(branchingPdf)
    lecture.remove(branchingPdf)
    expect(lecture.includes(branchingPdf)).toBeFalsy()
  })

  it('should not be able to remove unexisting material', () => {
    const lecture: Lecture = new Lecture('Branching', 'https://youtube.com/1234')
    const branchingPdf: Material = new Pdf('Branching', 'https://storage/branching.pdf')
    const error = lecture.remove(branchingPdf).value as Error
    expect(error).toBeInstanceOf(UnexistingElementError)
  })

  it('should be able to add further links to lectures', () => {
    const lecture: Lecture = new Lecture('Branching', 'https://youtube.com/1234')
    const branchingLink: Material = new Link('Branching', 'http://page.com/branching.html')
    lecture.add(branchingLink)
    expect(lecture.includes(branchingLink)).toBeTruthy()
  })

  it('should not be able to add existing material to lectures', () => {
    const lecture: Lecture = new Lecture('Branching', 'https://youtube.com/1234')
    const branchingPdf: Material = new Pdf('Branching', 'https://storage/branching.pdf')
    lecture.add(branchingPdf)
    const error = lecture.add(branchingPdf).value
    expect(lecture.includes(branchingPdf)).toBeTruthy()
    expect(error).toBeInstanceOf(ExistingElementError)
  })

  it('should not be able to determine position of unexisting material', () => {
    const lecture: Lecture = new Lecture('Branching', 'https://youtube.com/1234')
    const branchingPdf: Material = new Pdf('Branching', 'https://storage/branching.pdf')
    const error = lecture.position(branchingPdf).value as Error
    expect(error).toBeInstanceOf(UnexistingElementError)
  })

  it('should be able to move further materials', () => {
    const lecture: Lecture = new Lecture('Branching', 'https://youtube.com/1234')
    const branchingPdf: Material = new Pdf('Branching pdf', 'https://storage/branching.pdf')
    const branchingLink: Material = new Link('Branching link', 'http://page.com/branching.html')

    lecture.add(branchingPdf)
    lecture.add(branchingLink)

    lecture.move(branchingPdf, 2)

    expect(lecture.position(branchingLink).value).toEqual(1)
    expect(lecture.position(branchingPdf).value).toEqual(2)
  })
})
