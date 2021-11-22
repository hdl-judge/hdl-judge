import {del, get, post} from "./http_requests";
import type {File} from "./api";

export async function saveSubmissionFiles(files: File[], projectId: number): Promise<void> {
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


export async function getSubmissonFiles(projectId: number, userId: number) {
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