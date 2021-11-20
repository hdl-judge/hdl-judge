import { post, get, del } from "./http_requests";

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

	return await post("/submit", submission)
}

export async function getAllExercises() {
    return await get("/get_values/projects");
}

export async function createExercise(name: string, userId: number = 1) {
    await post("/create_project", {
        name,
        created_by: userId
    });
}

export async function removeExercise(id: number) {
    await del("/delete_value/projects", {
       id
    });
}

export async function saveProjectFiles(files: File[], projectId: number, userId: number = 1): Promise<void> {
    for (let file of files) {
        await post("/create_projects_files", {
            name: file.filename,
            created_by: userId,
            project_id: projectId,
            default_code: file.content,
        });
    }
}

export async function getFilesFromProject(projectId: number) {
    let files = await get("/get_values/projects_files");
    let filteredFiles = files
        .filter(x => x.project_id == projectId)
        .map(x => {
            let file = new File();
            file.filename = x.name;
            file.content = x.default_code;
            return file;
        });
    return filteredFiles;
}