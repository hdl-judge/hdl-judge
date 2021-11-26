import {del, get, post} from "./http_requests";
import type {File} from "./api";

export async function saveSubmissionFiles(files: File[], projectId: string): Promise<void> {
    await post("/save_submission_files", {
        project_id: parseInt(projectId, 10),
        files: files.map(x => ({
            name: x.filename,
            code: x.content,
            metadata: ""
        })),
    });
}

export async function saveSubmissionFiles2(files: File[], projectId: number): Promise<void> {
    for (let file of files) {
        await post("/create_submission_files", {
            name: file.filename,
            project_id: projectId,
            code: file.content,
            metadata: ""
        });
    }
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