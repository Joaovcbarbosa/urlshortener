import { User } from '../../src/entities/user'
import { CreateCourse } from '../../src/use-cases/create-course'
import { CourseData } from '../../src/use-cases/data-types/course-data'
import { InMemoryCourseRepository } from '../doubles/in-memory-course-repository'

const authors = [
  new User('John Doe', 'john@email.com', 'password123'),
  new User('Mary Shaw', 'mary@email.com', 'password123')
]

describe('Create course use case', () => {
  it('should be able to create course with course info', async () => {
    const repo = new InMemoryCourseRepository()
    const usecase = new CreateCourse(repo)
    const request: CourseData = {
      reference: 'azure-devops',
      title: 'Continuous Delivery and DevOps with Azure DevOps 1: Source Control with Git',
      description: 'This course will teach you the fundamentals of Source Control and how to use this with Azure DevOps. You will learn how to work with Git, Pull Requests, Branch Policies, and implement Continuous Integration.',
      authors: authors
    }
    await usecase.perform(request)
    const courses: CourseData[] = await repo.list()
    expect(courses.length).toEqual(1)
    expect(courses[0].title).toEqual(request.title)
  })
})
