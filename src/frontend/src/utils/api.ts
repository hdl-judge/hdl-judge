import { post } from "./http_requests";

export class File {
	filename: string;
	content: string;
}

class Submission {
	toplevel_entity: string;
	files: object;
}

class SubmissionResponse {
	status: string;
	result: string;
    message: string;
}

export async function submitTest(items: File[]): Promise<SubmissionResponse> {
	let submission = new Submission();
	submission.toplevel_entity = "adder_tb";
    submission.files = items.filter(item => item.filename.endsWith(".vhdl"));

	return await (await post("/submit", submission)).json()
}