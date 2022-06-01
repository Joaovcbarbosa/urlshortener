import { CourseData } from './data-types/course-data'
import { CourseRepository } from './ports/course-repository'

export class CreateCourse {
  // eslint-disable-next-line no-useless-constructor
  constructor (private repo: CourseRepository) {}
  async perform (request: CourseData): Promise<void> {
    this.repo.add(request)
  }
}
