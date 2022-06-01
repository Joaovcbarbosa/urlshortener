import { CourseData } from '../../src/use-cases/data-types/course-data'
import { CourseRepository } from '../../src/use-cases/ports/course-repository'

export class InMemoryCourseRepository implements CourseRepository {
  private courses: CourseData[] = []

  async list (): Promise<CourseData[]> {
    return this.courses
  }

  async add (course: CourseData): Promise<void> {
    this.courses.push(course)
  }
}
