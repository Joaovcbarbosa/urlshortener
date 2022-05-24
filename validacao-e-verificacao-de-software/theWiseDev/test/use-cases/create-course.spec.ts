import { CreateCourse } from '../../src/use-cases/create-course';
import { CourseData } from '../../src/use-cases/data-types/course-data';
import { InMemoryCourseRepository } from '../doubles/in-memory-course-repository';

describe('Create course use case', () => {
  it('Should be able to create course with course info', async () => {
    const repository = new InMemoryCourseRepository()
    const useCase = new CreateCourse(repository);
    const request: CourseData = {
    reference: 'azure-devops',
    title: 'Continuous Delivery and DevOps with Azure DevOps: Source Control with Git', 
    description: 'This course will teach you the fundamentals of Source Control and how to use this with Azure DevOps. You will learn how to work with Git, Pull Requests, Branch Policies, and implement Continuous Integration.'
    };
    await useCase.perform(request);
    const courses: CourseData[] = await repository.list();
    expect(courses.length).toEqual(1);
    expect(courses[0].title).toEqual(request.title)
  })
});