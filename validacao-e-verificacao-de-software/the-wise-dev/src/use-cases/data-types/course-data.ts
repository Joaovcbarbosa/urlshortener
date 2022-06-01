import { User } from "../../entities/user"

export interface CourseData {
  reference: string,
  title: string,
  description: string
  authors: User[]
}
