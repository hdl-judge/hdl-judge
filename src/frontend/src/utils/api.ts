import { post } from "./http_requests";

const WAITTIME = 200;

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

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

export async function submitTest(items: File[]): Promise<SubmissionResponse> {
	let submission = new Submission();
	submission.toplevel_entity = "adder";
    submission.files = items.filter(item => item.filename.endsWith(".vhdl") || item.filename.endsWith(".json"));

	return await (await post("/submit", submission)).json()
}

let exercises = [
    { id: 1, name: "Somador" },
    { id: 2, name: "Pipeline - Estágio 1"},
];

export async function getAllExercises() {
    await sleep(WAITTIME);
    return exercises;
}

export async function createExercise(name: string) {
    await sleep(WAITTIME);
    exercises.push({ id: Math.max(...exercises.map(x => x.id))+1, name });
    return 200;
}

export async function removeExercise(id: number) {
    await sleep(WAITTIME);
    exercises = exercises.filter(x => x.id != id);
    return 200;
}