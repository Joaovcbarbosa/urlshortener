import { CourseData } from '../data-types/course-data'

export interface CourseRepository {
  list (): Promise<CourseData[]>
  add (course: CourseData): Promise<void>
}
