import { HttpRequest } from "../../../test/presentation/ports/http-request";

export class CreateCourseController {
    constructor(
        private readonly createCourseUseCase: UseCase 
    ) {}

    async handle(request: HttpRequest): Promise<HttpResponse>{
        await this.createCourseUseCase.perform(request)
    return {
        statusCode: 201,
        body: request.body
    }}
}