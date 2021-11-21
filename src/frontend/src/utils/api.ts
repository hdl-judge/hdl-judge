import {post, get, del, postFormData} from "./http_requests";

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

export async function login(username: string, password: string) {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    let result = await postFormData("/token", formData);
    return result;
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

export async function getUserData() {
    try {
        let result = await get("/users/me");
        return result;
    } catch {
        return false;
    }
}