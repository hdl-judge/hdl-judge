import {post, get, del, postFormData} from "./http_requests";

export class FileDto {
	filename: string;
	content: string;
}

class SubmissionResponse {
	status: string;
	result: string;
    message: string;
    filename: string;
}

export async function login(username: string, password: string) {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    let result = await postFormData("/token", formData);
    return result;
}

export async function runTest(projectId: string): Promise<SubmissionResponse> {
	return await get("/submit", {project_id : parseInt(projectId, 10)})
}

export async function getAllProjects() {
    return await get("/get_values/projects");
}

export async function createProject(name: string, userId: number = 1) {
    await post("/create_project", {
        name,
        created_by: userId
    });
}

export async function removeProject(id: number) {
    await del("/delete_value/projects", {
       id
    });
}

export async function saveProjectFiles(files: FileDto[], projectId: string): Promise<void> {
    await post("/save_project_files", {
        project_id: parseInt(projectId, 10),
        files: files.map(x => ({
            name: x.filename,
            default_code: x.content,
        })),
    });
}

export async function getFilesFromProject(projectId: number) {
    let files = await get("/get_projects_files", { project_id: projectId });
    return files.map(x => ({
        filename: x.name,
        content: x.default_code,
        id: x.id,
    }));
}

export async function removeProjectFile(id: number) {
    await del("/delete_value/projects_files", {
       id
    });
}

export async function getUserData() {
    try {
        let result = await get("/users/me");
        return result;
    } catch {
        return false;
    }
}