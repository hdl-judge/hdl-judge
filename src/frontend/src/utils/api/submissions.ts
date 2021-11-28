import {del, get, post} from "./http_requests";
import type {FileDto} from "./api";
import {getMossKey} from "../utils";

export async function saveSubmissionFiles(files: FileDto[], projectId: string): Promise<void> {
    await post("/save_submission_files", {
        project_id: parseInt(projectId, 10),
        files: files.map(x => ({
            name: x.filename,
            code: x.content,
            metadata: ""
        })),
    });
}

export async function removeSubmissionFile(id: number) {
    await del("/delete_value/submission_files", {
       id
    });
}

export async function getSubmissonFiles(projectId: number) {
    let files = await get("/get_files_to_student", { project_id: projectId });
    return files.map(x => ({
        filename: x.name,
        content: x.code,
        id: x.id,
    }));;
}

export async function getSubmissonFiles2(projectId: number, userId: number) {
    let files = await get("/get_values/submission_files");
    let filteredFiles = files
        .filter(x => x.project_id == projectId && x.created_by == userId)
        .map(x => ({
            filename: x.name,
            content: x.code,
            id: x.id,
        }));
    return filteredFiles;
}

export async function getAllProjectSubmissons(projectId: number) {
    let submissions = await get("/get_project_submissions", {"project_id": projectId});
    return submissions;
}

export async function sendSubmissionsToMoss(projectId: number) {
    let result = await get("/submit_all_codes_from_project_to_plagiarism", {"project_id": projectId});
    localStorage.setItem(getMossKey(projectId), result[0])
    return result;
}