import { CourseData } from "./data-types/course-data";
import { CourseRepository } from "./ports/course-repository";

export class CreateCourse {
  constructor (private repo: CourseRepository) {}
  async perform(request: CourseData): Promise<void> {
    this.repo.add(request);
  }
}